from sqlalchemy import create_engine, text
import os

db_connection_string = os.environ['DB_CONNECTION_STRING']


try:
  # Create an engine and test the connection
  engine = create_engine(db_connection_string)
  connection = engine.connect()
  print("Database connection established successfully.")
  connection.close()
except Exception as e:
  print(f"Error connecting to the database: {str(e)}")

engine = create_engine(
    db_connection_string,
    connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    }
)

def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM jobs"))
    jobs = []
    columns = result.keys()  # Get the column names from the result set

    for row in result:
        job_dict = {column: value for column, value in zip(columns, row)}
        jobs.append(job_dict)

  return jobs


def load_job_from_db(id):
  with engine.connect() as conn:
      result = conn.execute(
          text("SELECT * FROM jobs WHERE id = :val"),
          {"val": id}
      )

      row = result.fetchone()
      if row is not None:
          # Use result.keys() to get the column names
          job_dict = {key: getattr(row, key) if getattr(row, key) is not None else "" for key in result.keys()}
          return job_dict
      else:
          return None


def add_application_to_db(job_id, data):
  with engine.connect() as conn:
      query = text("""
          INSERT INTO applications 
          (job_id, full_name, email, linkedin_url, education, work_experience, resume_url)
          VALUES 
          (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)
      """)

      conn.execute(query, {
          'job_id': job_id,
          'full_name': data['full_name'], 
          'email': data['email'], 
          'linkedin_url': data['linkedin_url'],
          'education': data['education'], 
          'work_experience': data['work_experience'], 
          'resume_url': data['resume_url']
      })

def add_user_to_db(username, hashed_password, email, first_name, last_name):
  try:
      with engine.connect() as conn:
          query = text("""
              INSERT INTO users (username, password_hash, email, first_name, last_name)
              VALUES (:username, :password_hash, :email, :first_name, :last_name)
          """)

          conn.execute(query, {
              'username': username,
              'password_hash': hashed_password,
              'email': email,
              'first_name': first_name,
              'last_name': last_name
          })

  except Exception as e:
      # Log the error for debugging
      print(f"Error inserting user: {str(e)}")


def get_user_from_db(username):
  with engine.connect() as conn:
      query = text("SELECT * FROM users WHERE username = :username")
      result = conn.execute(query, {'username': username})
      user = result.fetchone()
      if user:
          user_dict = {key: getattr(user, key) for key in user.keys()}
          return user_dict
      return None













    
