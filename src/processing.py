from bs4 import BeautifulSoup
import requests
import connection as c

#ATT GÖRA: skapa en funktion som tar en bild som argument och vektoriserar den. Returnera vektorn.

class web:

    #räkna ut antalet sidor med produkter
    def amount_of_pages():
        web_page = requests.get("https://www.myrorna.se/shop/")
        soup = BeautifulSoup(web_page.text, "html.parser")
        page_idx = soup.find_all("a", class_="page-numbers")
        
        last_page_idx = page_idx[len(page_idx)-2] #i detta index finns sista sidan
        last_page_idx = int(last_page_idx.text.strip())

        return last_page_idx


    def scrape():
        nr_of_pages = web.amount_of_pages()
        print("Cooking...")

        # skrapa varje sida
        for current_page in range(1, nr_of_pages+1):
            web_page = requests.get("https://www.myrorna.se/shop/sida/" + str(current_page) + "/")
            soup = BeautifulSoup(web_page.text, "html.parser")
            products = soup.find_all("img", attrs={"class": "auction-image"})

            for product in products:
                try:
                    product_info = product.get("alt").split(", ",1)
                    #i listan product_info i index 0 finns produktens namn, i index 1 finns produktens beskrivning
                    if len(product_info) >=2:
                        data.insert(product, product_info[0], product_info[1]) # src is the imageURL and alt is the product description

                    if len(product_info) == 1:
                        data.insert(product, product_info[0], "")
                        
                except:
                    pass

            c.conn.commit()
            print("\r{}%".format(round(current_page*100/nr_of_pages),1),end="", flush=True) #printa procent statusen av skrapningen
        
        #stäng uppkopplingen till databasen
        c.cursor.close()
        c.conn.close()
        print("\nData has been inserted to the database!")

class data:

    #SQL query för att radera all data och skapa en ny table för ny data
    def clean_table():
        c.cursor.execute("""
        DROP TABLE IF EXISTS products;

        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            imageURL TEXT,
            name TEXT,
            info TEXT
        );                    
        """)
    
    def insert(product:dict, name:str, desc:str):
        c.cursor.execute("""
        INSERT INTO products (imageURL, name, info)
        VALUES (%s, %s, %s);
        """, (product.get("src"), name, desc))
    

    def find_similar(vector) -> list:
        c.cursor.execute("""
            SELECT imageURL 
            FROM products 
            WHERE vectorIMG <-> '%s' < 0.5
            ORDER BY vectorIMG <-> '%s'
            LIMIT 5;
        """, vector, vector)

        similar_images = c.cursor.fetchall() #detta ger utseende av ex: [(1.jpg, ), (2.jpg, ), (3.jpg, )] därför loopar vi genom den och förbättrar output

        for i in range(0,len(similar_images)):
            similar_images[i] = similar_images[i][0]

        return similar_images
    