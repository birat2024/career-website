
from flask import Flask, render_template, jsonify

app = Flask(__name__)

JOBS = [
  {
    'id': 1,
    'title': 'Data Analyst',
    'location': 'Boston, MA',
    'salary': '$150,000'
  },

  {
    'id': 2,
    'title': 'Data Scientist',
    'location': 'Quincy, MA',
    'salary' : '$200,000'
  },

  {
    'id': 3,
    'title': 'Frontend Engineer',
    'location': 'Dallas, TX',
    'salary' : '$100,000'
  },
  
  {
    'id': 4,
    'title': 'Backend Engineer',
    'location': 'Murphy, TX',
    
  }
]
  

@app.route("/")
def hello_world():
  return render_template('home.html', jobs=JOBS)
@app.route("/api/jobs")
def list_jobs():
  return jsonify(JOBS)

# to connecg to the server
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
  



