import json
import spacy
from deep_translator import GoogleTranslator

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

def skills_extraction(text, db):
    '''
    :param text:
    :return:
    '''
    dict_skill = {"Hard Skill":[],"Soft Skill":[]}
    appended = 0
    for skill in db["Hard Skill"]:
        if skill.lower() in text.lower():
            dict_skill["Hard Skill"].append(skill.lower())
            appended+=1
            if appended > 5: break
    appended = 0
    for skill in db["Soft Skills"]:
        if skill.lower() in text.lower():
            dict_skill["Soft Skill"].append(skill.lower())
            appended+=1
            if appended>5: break


    return dict_skill

def skills_extractor(job):

    with open("C:/Users/dnedi/PycharmProjects/Skill-Plant/scripts/skills_data.json") as file:
        skills_db = json.load(file)
    desc = get_description(job)
    desc_translated = translation(desc)
    skills = skills_extraction(desc_translated, skills_db)
    job.update(skills)
    # print(job)


# if __name__ == "__main__":
    # skills_extractor()

