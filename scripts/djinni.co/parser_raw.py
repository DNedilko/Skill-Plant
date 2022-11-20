import dateparser
import re

def parse_date(date_raw: str) -> dateparser.date:
    return dateparser.parse(date_raw, settings={'TIMEZONE': 'UTC'}, date_formats=["%d %m %Y"])


def parse_remote_type(remote_raw: str) -> str:
    type = ''
    if re.findall(r"тільки віддалено", remote_raw, re.IGNORECASE):
        type = 'remote'
    elif re.findall(r"тільки офіс", remote_raw, re.IGNORECASE):
        type = 'in-office'
    elif re.findall(r"(гібридна робота|office/remote|на ваш вибір)", remote_raw, re.IGNORECASE):
        type = 'hybrid'

    return type

def parse_region(region_raw: str) -> [str, str]:
    raw = re.sub('\\n', ' ', region_raw)

    cities = ''
    cities_groups = re.findall('\([^)]+\)', raw)
    if cities_groups:
        for group in cities_groups:
            cities += group + ', '
        cities = re.sub(',\s*$', '', cities).replace('(', '').replace(')', '').strip()

    countries = re.sub('\([^)]+\)', '', raw).strip()

    return cities, countries


def parse_seniority(title_raw: str) -> str:
    levels = []
    if re.findall(r"(junior|assistant|intern|trainee|entry)", title_raw, re.IGNORECASE):
        levels.append('entry-level')
    if re.findall(r"tech lead", title_raw, re.IGNORECASE):
        levels.append('tech-lead')
    elif re.findall(r"team lead|lead", title_raw, re.IGNORECASE):
        levels.append('team-lead')
    if re.findall(r"(middle|mid-level|\smid\s)", title_raw, re.IGNORECASE):
        levels.append('mid-level')
    if re.findall(r"(senior|sen-level|\ssen\s|president|director|head of)", title_raw, re.IGNORECASE):
        levels.append('senior-level')

    if levels:
        return ', '.join(levels)
    else:
        return ''
