
from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import add_user_to_db, get_user_from_db, load_jobs_from_db, load_job_from_db, add_application_to_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

app = Flask(__name__, static_url_path='/static', static_folder='static')


@app.route("/signup", methods=["GET", "POST"])
def signup():
    message = None
    error = None

    if request.method == "POST":
        try:
            # Get form data
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            # Add validation checks here (e.g., password confirmation)

            # If validation passes, proceed to add user to the database
            # You can add this logic here

            # If user is successfully added, set the message and redirect
            message = "Signup successful. Please login."
            return redirect(url_for('login', message=message))
        except Exception as e:
            # Capture and handle specific exceptions
            error = f"Signup failed: {str(e)}"
            print(f"Signup failed: {str(e)}")

    return render_template("signup.html", message=message, error=error)




@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = get_user_from_db(username)
        if user and check_password_hash(user['password_hash'], password):
            session['username'] = username  # Set up user session
            return redirect(url_for('hello_world'))
        else:
            error = 'Invalid username or password'

    return render_template("login.html", error=error)



@app.route("/logout")
def logout():
    session.pop('username', None)  # Remove the username from session
    return redirect(url_for('hello_world'))



@app.route("/")
def hello_world():
    jobs = load_jobs_from_db()
    return render_template('home.html', jobs=jobs)

@app.route("/api/jobs")
def list_jobs():
    return jsonify(load_jobs_from_db())
  
@app.route("/job/<id>")
def show_job(id):
    job = load_job_from_db(id)
    if job is not None:
        return render_template("jobpage.html", job=job)
    else:
        return render_template("jobpage.html", error="Job not found"), 404

@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id):
    data = request.form
    job = load_job_from_db(id)
    add_application_to_db(id, data)
    return render_template("application_submitted.html", application=data, job=job)  

@app.route("/api/job/<id>")
def show_job_json(id):
    job = load_job_from_db(id)

    if job is None:
        # If job with the given id is not found, return a 404 Not Found response
        abort(404)

    return jsonify(job)

@app.route("/opportunities")
def opportunities():
    return render_template("opportunities.html")

  


# to connect to the server
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)




