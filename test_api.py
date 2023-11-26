import requests
import re

job_description = """
dummy jd with skills python, machine learning, sql, data analysis and ability to manage
"""

url = "http://127.0.0.1:5065/parse_skills"
# url = "http://127.0.0.1:5065/parse_raw_skills"
job_description = re.sub("[^A-Za-z0-9]"," ",job_description)

querystring = {
    "job_description": str(job_description)
}
payload = ""
headers = {'Content-Type': 'application/json'}

resp = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(resp.text)