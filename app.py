import json
from utils import fetch_skills_detail
from flask import g, Flask, request
import spacy
from spacy.matcher import PhraseMatcher
from skillNer.skill_extractor_class import SkillExtractor
import logging
from logging.handlers import RotatingFileHandler
import time

LOG_FILE = "logs/api_requests.log"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3

handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=MAX_LOG_SIZE,
    backupCount=BACKUP_COUNT
)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)
handler.setFormatter(formatter)

logger = logging.getLogger("parse_skills_api")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False

def truncate(value, max_length=500):
    if not value:
        return value
    value = str(value)
    return value[:max_length] + ("... [truncated]" if len(value) > max_length else "")

with open('buckets/skill_db_relax_20.json') as json_file:
    SKILL_DB = json.load(json_file)

nlp = spacy.load('en_core_web_lg')
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

def annotate_sentences(sentences):
    annotations = skill_extractor.annotate(sentences)
    return annotations

app = Flask(__name__)

@app.before_request
def log_request():
    g.start_time = time.time()

    if request.is_json:
        payload = request.get_json()
        job_desc = payload.get("job_description", "")

        logger.info(
            "REQUEST | %s %s | job_description=%s",
            request.method,
            request.path,
            truncate(job_desc)
        )
    else:
        logger.info(
            "REQUEST | %s %s | Non-JSON request",
            request.method,
            request.path
        )

@app.after_request
def log_response(response):
    start_time = getattr(g, "start_time", None)
    duration = round(time.time() - start_time, 3) if start_time else "NA"

    response_payload = response.get_data(as_text=True)

    logger.info(
        "RESPONSE | %s | status=%s | time=%ss | payload=%s",
        request.path,
        response.status_code,
        duration,
        truncate(response_payload)
    )

    return response

@app.route('/parse_raw_skills', methods=['POST'])
def parse_raw_skills():
    '''
    Parses skills from a job description.
    '''
    # skill_extractor = getattr(g, '_skill_extractor', None)

    # Read 'job_description' from the JSON body
    data = request.get_json()
    sentences = data.get('job_description', '')

    annotations = annotate_sentences(sentences)
    return json.dumps(annotations, default=str)

@app.route('/parse_skills', methods=['POST'])
def parse_skills():
    '''
    Parses skills and fetches detailed skill information.
    '''
    # skill_extractor = getattr(g, '_skill_extractor', None)

    # Read 'job_description' from the JSON body
    data = request.get_json()
    sentences = data.get('job_description', '')

    raw_annotations = annotate_sentences(sentences)
    parsed_skills = fetch_skills_detail(raw_annotations)
    
    return json.dumps(parsed_skills, default=str)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5065"), debug=True)