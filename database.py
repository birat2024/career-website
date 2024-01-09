from sqlalchemy import create_engine, text
import os

db_connection_string = os.environ['DB_CONNECTION_STRING']

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














    
