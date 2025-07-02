from pprint import pprint
import collections
import pandas
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dotenv import load_dotenv


def get_text(age):
    last_number = age % 10
    prelast_number = age // 10 % 10
    if 9 >= last_number >= 5 or last_number == 0:
        text = "лет"
    elif last_number == 1:
        if prelast_number == 1:
            text = "лет"
        else:
            text = "год"
    elif 2 <= last_number <= 4:
        if prelast_number == 1:
            text = "лет"
        else:
            text = "года"
    return text


def main():
    load_dotenv()
    excel_data_df = pandas.read_excel(
        os.getenv("WINE_XLSX", "wine3.xlsx"), na_values=["N/A", "NA"], keep_default_na=False
    ).to_dict("records")
    now = datetime.datetime.now()
    now_year = now.year
    year_foundation = 1920
    age = now_year - year_foundation
    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )
    dict_of_lists = collections.defaultdict(list)
    for wine in excel_data_df:
        dict_of_lists[wine["Категория"]].append(wine)
    pprint(dict_of_lists)
    template = env.get_template("template.html")

    rendered_page = template.render(age=age, text=get_text(age), wines=dict_of_lists)

    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
