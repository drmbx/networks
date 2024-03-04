import sys
from bs4 import BeautifulSoup
import requests
import csv


def online_split(all_onl):
    all_current = []
    all_max = []
    for text in all_onl:
        parts = text.split('/')
        all_current.append(parts[0])
        all_max.append(parts[1])
    return all_current, all_max


def parse(pages_amount):
    names = []
    cur_online = []
    max_online = []
    statuses = []
    for page_num in range(pages_amount):
        url = "https://minecraftservers.org/index/" + str(page_num + 1)
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

    return zip(names, cur_online, max_online, statuses)


def to_csv(data):
    with open('info.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Current online", "Max online", "Status"])
        for row in data:
            writer.writerow(row)


if len(sys.argv) == 1:
    to_csv(parse(5))
else:
    to_csv(parse(int(sys.argv[1])))
