<<<<<<< HEAD
import itertools
import json
import spacy
from deep_translator import GoogleTranslator
=======
import json

import spacy
from deep_translator import GoogleTranslator
# load default skills data base
from skillNer.general_params import SKILL_DB
# import skill extractor
from skillNer.skill_extractor_class import SkillExtractor
from spacy.matcher import PhraseMatcher

>>>>>>> eeae81e (added description parser to djinni and changed abit database position load)

# loading description data from json
def get_description(record):

    description = record["description"]

    return description

def translation(initial_data):
    '''
    :param initial_data: initial description to parse
    :return: description translated to english
    '''
<<<<<<< HEAD
    try:
        translator = GoogleTranslator(source='auto',target='en')
        english_text = translator.translate(initial_data)
        return english_text
    except:
        print(initial_data)
        return ''


def skills_extraction(text, db):
=======
    translator = GoogleTranslator(source='auto',target='en')
    english_text = translator.translate(initial_data)
    return english_text

def skills_extraction(text, nlp):
>>>>>>> eeae81e (added description parser to djinni and changed abit database position load)
    '''
    :param text:
    :return:
    '''
<<<<<<< HEAD
    empty1 = itertools.repeat(' ',5)
    empty2 = itertools.repeat(' ', 5)
    dict_skill = {"Hard Skill":[],"Soft Skill":[]} # ,"Soft Skill Ukr": [], "Hard Skill Ukr":[]}

    appended = 0
    for skill in db["Hard Skill"]:
        try:
            if skill.lower() in text.lower():
                dict_skill["Hard Skill"].append(skill.lower())
                appended+=1
                if appended > 5: break
        except:
            print(f'CHECK SKILL: {skill}')
    appended = 0
    for skill in db["Soft Skill"]:
        try:
            if skill.lower() in text.lower():
                    dict_skill["Soft Skill"].append(skill.lower())
                    appended+=1
                    if appended>5: break
        except:
            print(f'CHECK SKILL: {skill}')

    dict_skill["Hard Skill"].extend(empty1)
    dict_skill["Soft Skill"].extend(empty2)

    # for skill in db["Soft Skill Ukr"]:
    #     if skill.lower() in text.lower():
    #         dict_skill["Soft Skill Ukr"].append(skill.lower())
    #         appended+=1
    #         if appended>5: break
=======
    # init params of skill extractor
    # spacy.cli.download("en_core_web_lg")

    # init skill extractor
    skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
    # extract skills from job_description
    skills_dict = skill_extractor.annotate(text)
    # print(skills_dict)
    stop_s = 0
    stop_h = 0
    dict_skill = {"Hard Skill": [], "Soft Skill": []}
    for k in skills_dict['results']:
        skills = skills_dict['results'][k]
        temp_skills_id = []
        for el in skills:
            if el['skill_id'] not in temp_skills_id:
                temp_skills_id.append(el['skill_id'])

                with open(".../skill_db_relax_20.json") as file:
                    skills_db = json.load(file)
                    type = skills_db[el['skill_id']]["skill_type"]
                    if type == "Hard Skill" and stop_h<=5:
                        dict_skill[type].append(el['doc_node_value'])
                        stop_h+=1
                    elif stop_s<=5 :
                        dict_skill[type].append(el['doc_node_value'])
                        stop_s+=1
>>>>>>> eeae81e (added description parser to djinni and changed abit database position load)


    return dict_skill

<<<<<<< HEAD
def skills_extractor(job,skills_db):


    desc = get_description(job)

    desc_translated = translation(desc)

    skills = skills_extraction(desc_translated, skills_db)
    print("Skills   ", skills)
=======
def skills_extractor(job, nlp):
    desc = get_description(job)
    desc_translated = translation(desc)
    skills = skills_extraction(desc_translated, nlp)
>>>>>>> eeae81e (added description parser to djinni and changed abit database position load)
    job.update(skills)
    # print(job)


<<<<<<< HEAD
if __name__ == "__main__":

    with open("C:/Users/dnedi/PycharmProjects/Skill-Plant/scripts/skills_data.json") as file:
        skills_db = json.load(file)

    text = ";".join([str(t) for t in skills_db["Hard Skill"]])
    skills_db["Hard Skill Ukr"] = list(translation(text).split(";"))

    print("done")
=======
# if __name__ == "__main__":
    # skills_extractor()

>>>>>>> eeae81e (added description parser to djinni and changed abit database position load)
