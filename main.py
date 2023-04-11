import requests
from bs4 import BeautifulSoup
import csv
import os
import re
from tqdm import tqdm
import logging

# Configs
logging.basicConfig(
    filename="logs.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)


def get_page_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


# Download book's cover (img)
def save_products_img(category, title, url):
    img = requests.get(url)

    file_extension = url[-3:]
    path = f"./data/{category}/img"
    if not os.path.exists(path):
        os.makedirs(path)

    file_name = " ".join(re.findall("[A-Za-z0-9]+", title)).replace(" ", "_")

    with open(f"{path}/{file_name}.{file_extension}", "wb") as file:
        file.write(img.content)


# Collect a single product infos
def get_product_infos(url):
    soup = get_page_soup(url)

    category = soup.find_all("a")[3].string
    image_url = soup.find_all("img")[0].get("src").replace("../..", "http://books.toscrape.com")

    product_page_url = url
    title = soup.find("h1").string

    more_info = soup.find_all("td")
    universal_product_code = more_info[0].string
    price_excluding_tax = more_info[2].string
    price_including_tax = more_info[3].string
    number_available = more_info[5].string
    review_rating = more_info[6].string
    try:
        product_description = soup.find("div", id="product_description").find_next_sibling("p").string
    except AttributeError:
        product_description = "N/A"

    product = [
        product_page_url,
        universal_product_code,
        title,
        price_including_tax,
        price_excluding_tax,
        number_available,
        product_description,
        category,
        review_rating,
        image_url,
    ]

    return product


# collect all links for a single caegory
def get_all_categories_links():
    soup = get_page_soup("http://books.toscrape.com/")
    category_bloc = soup.find("ul", class_="nav-list").find("ul")
    links_tags = category_bloc.find_all("a")
    links = []
    for tag in links_tags:
        category = []
        link = tag.get("href").replace("index.html", "")
        name = tag.string.strip()
        links.append([name, "https://books.toscrape.com/" + link])
    return links


# collect all book's link for a single page
def get_page_products_links(url, products_links):
    soup = get_page_soup(url)
    heads = soup.find_all("h3")
    for head in heads:
        link = head.find("a").get("href")
        # link = link.replace("index.html", "")

        products_links.append(link.replace("../../..", "https://books.toscrape.com/catalogue"))


# collect all products (books) infos for a single category
def get_all_products_category_links(category_url):
    products_links = []
    page_number = 2
    get_page_products_links(category_url, products_links)
    soup = get_page_soup(category_url)
    try:
        next = soup.find("li", class_="next").find("a").get("href")
    except:
        next = False
    while next:
        next_page_url = category_url + "page-" + f"{page_number}" + ".html"
        get_page_products_links(next_page_url, products_links)
        page_number += 1
        soup = get_page_soup(next_page_url)
        try:
            next = soup.find("li", class_="next").find("a").get("href")
        except:
            next = False

    return products_links


# writing products infos in a csv file
def write_csv_file(products_links, path):
    csvfile = open(path, "w", encoding="utf-8")
    c = csv.writer(csvfile)
    c.writerow(
        [
            "product_page_url",
            "universal_product_code",
            "title",
            "price_including_tax",
            "price_excluding_tax",
            "number_available",
            "product_description",
            "category",
            "review_rating",
            "image_url",
        ]
    )
    for product_link in products_links:
        product = get_product_infos(product_link)
        c.writerow(product)
        [product_page_url, universal_product_code, title, *mid, category, review_rating, img_url] = product
        logging.info(f"working on {product_link}")
        save_products_img(category, title, img_url)
    csvfile.close()


# Downloading all products (or main function)
def extract_all_books_by_category():
    categories_links = get_all_categories_links()
    for category_link in tqdm(categories_links, unit="catégorie"):
        [name, link] = category_link
        products_links = get_all_products_category_links(link)
        path = f"./data/{name}"
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            write_csv_file(products_links, path + f"/{name}.csv")
        except:
            # raise Exception(f"Cannot write file {path}")
            logging.error(f"Cannot create file {path}")


extract_all_books_by_category()
