from processing import data, web

#LÄS FÖRST INNAN DU KÖR KODEN!
#Kör endast om du ska webskrapa hela myrornas hemsida (ca 30-60min)
#annars ersätts databasen med ofullständig data

try:
    data.clean_table()
    web.scrape()

except Exception as e:
    print(f"{e}")   