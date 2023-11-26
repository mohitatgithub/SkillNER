import json

def fetch_skills_detail(raw_resp):
    """
    postprocess parse_raw_skills api response and return only relevant details from response
    """
    skill_ids1 = [skill_data['skill_id'] for skill_data in raw_resp['results']['full_matches']]
    skill_ids2 = [skill_data['skill_id'] for skill_data in raw_resp['results']['ngram_scored']]
    skill_ids = skill_ids1 + skill_ids2

    skill_details_list = []
    for skill_id in skill_ids:
        skill_details = {
            'skill_name':data[skill_id]['skill_name'],
            'skill_type':data[skill_id]['skill_type']
            }
        skill_details_list.append(skill_details)
    
    updated_res = {
        "text": raw_resp['text'],
        "results": skill_details_list
    }

    return updated_res


#def load_skills_dict():
with open("buckets/skills_processed.json", "r") as read_file:
    data = json.load(read_file)
