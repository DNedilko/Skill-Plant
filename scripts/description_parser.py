import itertools
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
    try:
        translator = GoogleTranslator(source='auto',target='en')
        english_text = translator.translate(initial_data)
        return english_text
    except:
        print(initial_data)
        return ''


def skills_extraction(text, db):
    '''
    :param text:
    :return:
    '''
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


    return dict_skill

def skills_extractor(job,skills_db):


    desc = get_description(job)

    desc_translated = translation(desc)

    skills = skills_extraction(desc_translated, skills_db)
    print("Skills   ", skills)
    job.update(skills)
    # print(job)


if __name__ == "__main__":

    with open("C:/Users/dnedi/PycharmProjects/Skill-Plant/scripts/skills_data.json") as file:
        skills_db = json.load(file)

    text = ";".join([str(t) for t in skills_db["Hard Skill"]])
    skills_db["Hard Skill Ukr"] = list(translation(text).split(";"))

    print("done")
