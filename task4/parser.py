import sys
from bs4 import BeautifulSoup
import requests
import json


def online_split(all_onl):
    all_current = []
    all_max = []
    for text in all_onl:
        parts = text.split('/')
        all_current.append(parts[0])
        all_max.append(parts[1])
    return all_current, all_max


def parse(url):
    names = []
    cur_online = []
    max_online = []
    statuses = []

    page = requests.get(url)
    root = BeautifulSoup(page.text, "html.parser")

    all_names = root.find_all('a', href=lambda value: '/server/' in value)
    all_names = all_names[::4]
    all_names_text = list(map(lambda a: a.text, all_names))
    names.extend(all_names_text)

    all_online = root.find_all(class_="value")
    all_online = all_online[::4]
    all_online_list = list(map(lambda a: a.text, all_online))
    all_current_online, all_max_online = online_split(all_online_list)
    cur_online.extend(all_current_online)
    max_online.extend(all_max_online)

    all_statuses = root.find_all(class_="value online")
    all_statuses_text = list(map(lambda a: a.text, all_statuses))
    all_statuses_text = all_statuses_text[::2]
    statuses.extend(all_statuses_text)

    parsed_data = zip(names, cur_online, max_online, statuses)

    json_data = []
    for row in parsed_data:
        json_data.append({
            "name": row[0],
            "current online": row[1],
            "max online": row[2],
            "status": row[3]
        })
    return json.dumps(json_data)


print(parse("https://minecraftservers.org/index/2"))
