
from flask import Flask, render_template, jsonify, request, abort
from database import add_application_to_db, load_jobs_from_db, load_job_from_db, add_application_to_db

app = Flask(__name__)

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

  


# to connect to the server
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)




