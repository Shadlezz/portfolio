import requests
from bs4 import BeautifulSoup
import re
import pandas as pd



def get_html(url):
    r = requests.get(url)
    return r.text

def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    rows = soup.find_all('tr', class_='clickable-row')
    rows_for_hrefs = str(rows)
    ids = []
    floor_plans = []
    floors = []
    areas = []
    statuses = []
    prices = []
    types = []
    terraces = []

    links = re.findall(r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", rows_for_hrefs)
    links = [str[:-2] for str in links]

    for row in rows:
        columns = row.find_all('td')
        id = columns[0].text
        floor_plan = columns[1].text
        floor = columns[2].text
        area = columns[4].text
        status = columns[5].text
        price = columns[6].text
        type = columns[3].text




        ids.append(id)
        floor_plans.append(floor_plan)
        floors.append(floor)
        areas.append(area)
        statuses.append(status)
        prices.append(price)
        types.append(type)

    for link in links:
        html = str(get_html(link))
        try:
            terrace = re.findall(r'Terasa\:\D*(\d+,\d+)', html)
            terraces.append(terrace)
        except:
            pass



    df = pd.DataFrame(
        {'ID': ids, 'floor_plan': floor_plans, 'floor': floors, 'area': areas, 'status': statuses, 'price': prices, 'type': types, 'terrace': terraces
         })

    df.to_excel(r'B:\Games\Web-Projects\test1\test.xlsx', encoding='utf-8-sig')



def main():
    url = 'https://www.italska8.cz/byty'
    get_data(get_html(url))




if __name__ == '__main__':
    main()