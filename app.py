from flask import Flask, render_template, request, redirect, url_for, session, send_file, make_response, flash
from werkzeug.utils import secure_filename
import os
import difflib

app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
users = {}  # In-memory store; won't persist after restart
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    if 'user' not in session:
        user_from_cookie = request.cookies.get('username')
        if user_from_cookie in users:
            session['user'] = user_from_cookie
        else:
            return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember')

        if username in users and users[username] == password:
            session['user'] = username
            resp = make_response(redirect(url_for('home')))
            if remember:
                resp.set_cookie('username', username, max_age=60*60*24*7)  # 7 days
            return resp
        else:
            flash('Invalid credentials. Please try again.', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('signup'))

        if username not in users:
            users[username] = password
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('User already exists!', 'error')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    resume_name = session.get('last_resume', None)
    last_score = session.get('last_score', None)

    return render_template('dashboard.html', resume_name=resume_name, last_score=last_score)

@app.route('/match', methods=['POST'])
def match():
    if 'user' not in session:
        return redirect(url_for('login'))

    resume = request.files.get('resume')
    job_description = request.form.get('job_desc')

    if not resume or not job_description:
        flash('Both resume file and job description are required.', 'error')
        return redirect(url_for('home'))

    filename = secure_filename(resume.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    resume.save(filepath)

    try:
        with open(filepath, 'r', errors='ignore') as f:
            resume_text = f.read()
    except Exception as e:
        flash(f"Error reading resume file: {str(e)}", 'error')
        return redirect(url_for('home'))

    matcher = difflib.SequenceMatcher(None, resume_text.lower(), job_description.lower())
    score = round(matcher.ratio() * 100, 2)

    # Store recent match info in session for dashboard
    session['last_resume'] = filename
    session['last_score'] = f"{score}%"

    result_text = (
        f"Match Score: {score}%\n\n"
        f"Resume:\n{resume_text[:500]}...\n\n"
        f"Job Description:\n{job_description[:500]}..."
    )

    result_filename = f"match_result_{session['user']}.txt"
    result_path = os.path.join(RESULT_FOLDER, result_filename)

    try:
        with open(result_path, 'w') as f:
            f.write(result_text)
    except Exception as e:
        flash(f"Error saving result file: {str(e)}", 'error')
        return redirect(url_for('home'))

    flash('Matching completed successfully!', 'success')

    # ✅ Make sure score is passed and used in result.html
    return render_template('result.html', score=score, download_link=url_for('download', filename=result_filename))

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(RESULT_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
