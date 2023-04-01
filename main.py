import requests
from bs4 import BeautifulSoup
import csv
import os


def get_page_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


# collecter les informations d'un produit
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


# collecter les liens de toutes les catégories
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


# collecter les liens de tous les produits d'une page
def get_page_products_links(url, products_links):
    soup = get_page_soup(url)
    heads = soup.find_all("h3")
    for head in heads:
        link = head.find("a").get("href")
        # link = link.replace("index.html", "")

        products_links.append(link.replace("../../..", "https://books.toscrape.com/catalogue"))


# collecter tous produit d'une catégorie
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
    csvfile.close()


# Télécharger tous produits
def extract_all_books_by_category():
    categories_links = get_all_categories_links()
    for category_link in categories_links:
        [name, link] = category_link
        products_links = get_all_products_category_links(link)
        path = f"./data/{name}"
        try:
            os.makedirs(path)
            write_csv_file(products_links, path + f"/{name}.csv")
        except:
            raise Exception("Impossible de créer le dossier")


extract_all_books_by_category()
