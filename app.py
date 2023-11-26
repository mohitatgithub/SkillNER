import json
from utils import fetch_skills_detail

from flask import g, Flask, request
import spacy
from spacy.matcher import PhraseMatcher

#from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor

with open('buckets/skill_db_relax_20.json') as json_file:
    SKILL_DB = json.load(json_file)

nlp = spacy.load('en_core_web_lg')

skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)


def annotate_sentences(sentences):

    annotations = skill_extractor.annotate(sentences)

    return annotations


app = Flask(__name__)

@app.route('/parse_raw_skills', methods=['POST'])
def parse_raw_skills():
    '''
    passes skills froma job description
    '''

    skill_extractor = getattr(g, '_skill_extractor', None)

    sentences = str(request.args.get('job_description'))

    annotations = annotate_sentences(sentences)

    return json.dumps(annotations, default=str)


@app.route('/parse_skills', methods=['POST'])
def parse_skills():

    skill_extractor = getattr(g, '_skill_extractor', None)

    sentences = str(request.args.get('job_description'))

    raw_annotations = annotate_sentences(sentences)

    parsed_skills = fetch_skills_detail(raw_annotations)
    
    return json.dumps(parsed_skills, default=str)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5065"), debug=True)
