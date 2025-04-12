from processing import data

image_url = "https://www.sportringen.se/wp-content/uploads/2025/01/982861_7332413041749_Clique_H20_F_750b5e085b.jpg"

#vektorisera input bilden:
vector = data.vectorize(image_url) 

#jämför med alla vektorer och ta fram de mest liknande bilderna:
similar_images = data.find_similar(vector)

print(similar_images)