# Readme

Ce script est utilisé pour extraire des informations sur les livres du site suivant en utilisant Python.
http://books.toscrape.com/

### Installation

1. Assurez vous d'installer l'environnement virtuel:
   '''python -m venv env'''
2. Pour l'activer sur Windows:
   '''source env\Scripts\activate.bat'''
3. Pour l'activer sur Mac:
   '''source env/bin/activate'''
4. Installez les dependances utilisant le fichier requirements.txt:
   '''pip install -r requirements.txt'''
5. Finalement, exécutez le script en tapant dans le terminat:
   '''Python main.py'''

### Explication

**save_products_img(category, title, url)**
Cette fonction télécharge l'image associée à un livre en utilisant son URL et la sauvegarde dans un dossier spécifique correspondant à la catégorie du livre.

**get_product_infos(url)**
Cette fonction récupère les informations d'un livre à partir de son URL. Elle retourne une liste contenant les informations suivantes :

- URL de la page produit
- Code produit universel
- Titre du livre
- Prix TTC
- Prix HT
- Disponibilité
- Description du livre
- Catégorie
- Évaluation du livre
- URL de l'image associée

**get_all_categories_links()**
Cette fonction récupère les liens de toutes les catégories de livres disponibles sur le site.

**get_page_products_links(url, products_links)**
Cette fonction récupère les liens de tous les livres sur une page et les stocke dans la liste "products_links".

**get_all_products_category_links(category_url)**
Cette fonction récupère tous les liens de livres pour une catégorie donnée en parcourant les différentes pages de la catégorie.

**write_csv_file(products_links, path)**
Cette fonction prend en entrée la liste des liens de livres et le chemin où le fichier CSV contenant les informations des livres sera créé. Elle récupère les informations de chaque livre en utilisant la fonction "get_product_infos" et les stocke dans le fichier CSV. Elle télécharge également l'image de chaque livre en utilisant la fonction "save_products_img".

**extract_all_books_by_category()**
Cette fonction utilise toutes les fonctions ci-dessus pour extraire les informations sur tous les livres de toutes les catégories et les stocker dans des fichiers CSV séparés.
