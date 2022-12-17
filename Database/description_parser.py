import json

import spacy
from deep_translator import GoogleTranslator
# load default skills data base
from skillNer.general_params import SKILL_DB
# import skill extractor
from skillNer.skill_extractor_class import SkillExtractor
from spacy.matcher import PhraseMatcher


# loading description data from json
def get_description(record):

    description = record["description"]

    return description

def translation(initial_data):
    '''
    :param initial_data: initial description to parse
    :return: description translated to english
    '''
    translator = GoogleTranslator(source='auto',target='en')
    english_text = translator.translate(initial_data)
    return english_text

def skills_extraction(text, nlp):
    '''
    :param text:
    :return:
    '''
    # init params of skill extractor
    # spacy.cli.download("en_core_web_lg")

    # init skill extractor
    skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
    # extract skills from job_description
    skills_dict = skill_extractor.annotate(text)
    # print(skills_dict)
    dict_skill = {"Hard Skill": [], "Soft Skill": []}
    for k in skills_dict['results']:
        skills = skills_dict['results'][k]
        temp_skills_id = []
        for el in skills:
            if el['skill_id'] not in temp_skills_id:
                temp_skills_id.append(el['skill_id'])

                with open("skill_db_relax_20.json") as file:
                    skills_db = json.load(file)
                    type = skills_db[el['skill_id']]["skill_type"]
                    dict_skill[type].append(el['doc_node_value'])

    return dict_skill

def skills_extractor(job):
    nlp = spacy.load("en_core_web_lg")
    desc = get_description(job)
    desc_translated = translation(desc)
    skills = skills_extraction(desc_translated, nlp)
    job.update(skills)
    # print(job)


# if __name__ == "__main__":
    # skills_extractor()

