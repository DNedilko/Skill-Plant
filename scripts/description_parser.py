import itertools
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
        translator = GoogleTranslator(source='auto', target='en')
        english_text = translator.translate(initial_data)
    except:
        return ''

    return english_text

def skills_extraction(text, db):
    '''
    :param text:
    :return:
    '''
    empty1 = itertools.repeat(' ', 5)
    empty2 = itertools.repeat(' ', 5)
    dict_skill = {"Hard Skill":[],"Soft Skill":[]} # ,"Soft Skill Ukr": [], "Hard Skill Ukr":[]}

    appended = 0
    for skill in db["Hard Skill"]:
        try:
            skill = skill.lower()
        except:
            skill = str(skill)
        if skill in text.lower():
            dict_skill["Hard Skill"].append(skill)
            dict_skill["Hard Skill"] = set(dict_skill["Hard Skill"])
            appended += 1
            if appended > 5: break

    appended = 0
    for skill in db["Soft Skill"]:
        try:
            skill = skill.lower()
        except:
            skill = str(skill)
        if skill in text.lower():
            dict_skill["Soft Skill"].append(skill)
            dict_skill["Soft Skill"] = set(dict_skill["Soft Skill"])
            appended += 1
            if appended > 5: break

    dict_skill["Hard Skill"].extend(empty1)
    dict_skill["Soft Skill"].extend(empty2)

    # for skill in db["Soft Skill Ukr"]:
    #     if skill.lower() in text.lower():
    #         dict_skill["Soft Skill Ukr"].append(skill.lower())
    #         appended+=1
    #         if appended>5: break


    return dict_skill

def skills_extractor(job, skills_db):

    desc = get_description(job)
    desc_translated = translation(desc)
    skills = skills_extraction(desc_translated, skills_db)

    return skills


# if __name__ == "__main__":
#
#     with open("../skills_data.json") as file:
#         skills_db = json.load(file)
#
#     text = ";".join([str(t) for t in skills_db["Hard Skill"]])
#     skills_db["Hard Skill Ukr"] = list(translation(text).split(";"))
#
#     print("done")
