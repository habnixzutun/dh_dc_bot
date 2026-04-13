from bs4 import BeautifulSoup
from requests import get
from dotenv import load_dotenv
import datetime
from pprint import pprint

def get_kw(date: datetime.date) -> int:
    calender = date.isocalendar()
    return calender.week


def get_week_source(date: datetime.date = None) -> BeautifulSoup | None:
    url = "https://www.sw-ka.de/de/hochschulgastronomie/speiseplan/mensa_erzberger/"
    if date is not None:
        url += f"?kw={get_kw(date)}"

    response = get(url)
    if not response.ok:
        return None
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def get_week_data(soup: BeautifulSoup) -> dict:
    data = {}
    div = soup.find_all("div", {"class": "canteen-day"})
    for i, day in enumerate(div, start=1):
        day_data = {}
        for j, food_choice in enumerate(day.find_all("tr", {"class": "mensatype_rows"}), start=1):
            food_choice_data = []
            for option in food_choice.find_all("tr"):
                if option.get("class") is None:
                    continue
                description = option.find("b").contents[0]
                price = option.find("span", {"class": "bgp price_1"}).contents
                if not price:
                    continue
                else:
                    price = price[0]
                food_choice_data.append((description, price))
            day_data[f"Option {j}"] = food_choice_data
        data[i] = day_data
    return data

def main():
    soup = get_week_source(datetime.date.today() + datetime.timedelta(weeks=0))
    pprint(get_week_data(soup))


if __name__ == '__main__':
    load_dotenv()
    main()