import dateparser
import re


def parse_date(date_raw: str) -> dateparser.date:
    return dateparser.parse(date_raw, settings={'TIMEZONE': 'UTC'}, date_formats=["%d %m %Y"])


def parse_remote_type(remote_raw: str) -> str:
    type = ''
    if re.findall(r"(гібридна|office/remote|на ваш вибір)", remote_raw, re.IGNORECASE):
        type = 'hybrid'
    elif re.findall(r"тільки віддалено|віддалена робота|remote|дистанційна робота", remote_raw, re.IGNORECASE):
        type = 'remote'
    elif re.findall(r"В офісі/на місці", remote_raw, re.IGNORECASE):
        type = 'in-office'

    return type


def parse_region(region_raw: str) -> str:
    return re.sub('\s*шукаємо', ', шукаємо', re.sub(',.*', '', re.sub(',\s*шукаємо', ' шукаємо', region_raw)))


def parse_seniority(title_raw: str) -> str:
    levels = []
    if re.findall(r"(junior|assistant|intern|trainee|entry|молодший|без досвіду)", title_raw, re.IGNORECASE):
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


def parse_employment_type(employment_type: str) -> str:
    type = ''
    if re.findall(r"часткова зайнятість|неповна зайнятість", employment_type, re.IGNORECASE):
        type = 'part-time'
    elif re.findall(r"повна зайнятість", employment_type, re.IGNORECASE):
        type = 'full-time'

    return type