import requests
from bs4 import BeautifulSoup
import time
import json


def parse_giftery(section):
    fff=f"https://www.giftery.ru/giftcards/{section}?perPage=96&page=1"
    r = requests.get(fff)
    soup = BeautifulSoup(r.text, 'html.parser')
    card_block = soup.find("div","uk-grid uk-child-width-1-1 uk-child-width-1-2@s uk-child-width-1-3@l uk-child-width-1-1 uk-child-width-1-2@s catalog__list-mode-list")
    cards_on_page = card_block.findAll("a", class_="gift-card-v2 catalog__list-item gift-card-v2--fill-size gift-card-v2--hover gift-card-v2--shadow")
    list=[]
    for card in cards_on_page:
        dict1={}
        name = card.find("div", "gift-card-v2__title").text
        nominal = card.find("div", class_="gift-card-v2__denominations-value").text
        nominal1 = nominal.replace("\xa0", " ")
        link = card.get("href")
        res = requests.get(f"https://www.giftery.ru{link}")
        soup1 = BeautifulSoup(res.text, 'html.parser')
        time.sleep(1)
        description = soup1.find("div", class_="page-detail-card-brief__content").text
        dict1["Наименование карты"] = name
        dict1["Описание"] = description
        dict1["Номинал"] = nominal1
        dict1["Ссылка"] = f"https://www.giftery.ru{link}"
        list.append(dict1)

    with open("giftcards.txt","w",encoding="utf-8") as f:
        f.write(f"Список подарочных карт, доступных для приобретения в Интермагазине Giftery ")
        json.dump(list,f, ensure_ascii=False, indent=4)