# Readme

This script is used to extract information about books from the following website using Python:
http://books.toscrape.com/

### Installation

1. Make sure to install the virtual environment by running:\
   '''python
   python -m venv env
   '''
2. To activate it on Windows:\
   '''python
   source env\Scripts\activate.bat
   '''
3. To activate it on Mac:\
   '''python
   source env/bin/activate
   '''
4. Install the dependencies using the requirements.txt file:\
   '''python
   pip install -r requirements.txt
   '''
5. Finally, run the script by typing in the terminal:\
   '''python
   Python main.py
   '''

### Explication

**save_products_img(category, title, url)**\
This function downloads the image associated with a book using its URL and saves it in a specific folder corresponding to the book's category.

**get_product_infos(url)**\
This function retrieves the information about a book from its URL. It returns a list containing the following information:

- Product page URL
- Universal product code
- Book title
- Price (including tax)
- Price (excluding tax)
- Availability
- Book description
- Category
- Book rating
- URL of the associated image

**get_all_categories_links()**\
This function collects the links of all book categories available on the website.

**get_page_products_links(url, products_links)**\
This function cellects the links of all books on a page and stores them in the "products_links" list.

**get_all_products_category_links(category_url)**\
This function collects all book links for a given category by browsing through the different pages of the category.

**write_csv_file(products_links, path)**\
This function takes as input the list of book links and the path where the CSV file containing the book information will be created. It retrieves the information for each book using the "get_product_infos" function and writes it in the CSV file. It also downloads the image of each book using the "save_products_img" function.

**extract_all_books_by_category()**\
This function uses all the functions above to extract all books information in all categories and store them in separate CSV files.

### Output :

.
└── data
├── category_1
│ ├── category_1.csv
│ └── img
├── category_2
│ ├── category_2.csv
│ └── img
└── category_n
├── category_n.csv
└── img
