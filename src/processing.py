from bs4 import BeautifulSoup
import connection as c
import torch
import requests
from PIL import Image
from io import BytesIO
from transformers import CLIPProcessor, CLIPModel


model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

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

                    image_url = product.get("src")

                    vector = data.get_image_embedding_from_url(image_url, processor, model, device)

                    #i listan product_info i index 0 finns produktens namn, i index 1 finns produktens beskrivning
                    if len(product_info) >=2:
                        data.insert(product, vector, product_info[0], product_info[1]) # src is the imageURL and alt is the product description

                    if len(product_info) == 1:
                        data.insert(product, vector, product_info[0], "")
                        
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
            embedding FLOAT8[],
            name TEXT,
            description TEXT
        );                    
        """)
    
    def insert(product:dict, vector, name:str, desc:str):
        c.cursor.execute("""
        INSERT INTO products (imageURL, embedding, name, description)
        VALUES (%s, %s, %s, %s);
        """, (product.get("src"), vector, name, desc))
    

    def find_similar(vector) -> list:
        c.cursor.execute("""
            SELECT imageURL 
            FROM products 
            WHERE embedding <-> '%s' < 0.5
            ORDER BY embedding <-> '%s'
            LIMIT 5;
        """, vector, vector)

        similar_images = c.cursor.fetchall() #detta ger utseende av ex: [(1.jpg, ), (2.jpg, ), (3.jpg, )] därför loopar vi genom den och förbättrar output

        for i in range(0,len(similar_images)):
            similar_images[i] = similar_images[i][0]

        return similar_images
    


    def get_single_image_embedding(image, processor, model, device):
        inputs = processor(images=image, return_tensors="pt").to(device)
        with torch.no_grad():
            embeddings = model.get_image_features(**inputs)
        return embeddings.cpu().numpy().flatten()

    # Main function: takes an image URL
    def get_image_embedding_from_url(image_url, processor, model, device):
        try:
            response = requests.get(image_url, timeout=10)
            image = Image.open(BytesIO(response.content)).convert("RGB")
            embedding = data.get_single_image_embedding(image, processor, model, device)
            return embedding
        except Exception as e:
            print(f"Error processing image from {image_url}: {e}")
            return None






    