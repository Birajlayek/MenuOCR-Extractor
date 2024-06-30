import requests
from bs4 import BeautifulSoup
import os

def scrape_menu_images(base_url, headers):
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Assume menu images are within <img> tags with class 'menu-image'
    image_tags = soup.find_all('img', class_='menu-image')
    
    os.makedirs('menu_images', exist_ok=True)
    
    for idx, img_tag in enumerate(image_tags):
        img_url = img_tag['src']
        img_data = requests.get(img_url).content
        with open(f'menu_images/menu_{idx}.jpg', 'wb') as handler:
            handler.write(img_data)
    
    return len(image_tags)

# Example usage
if __name__ == "__main__":
    base_url = 'https://www.shutterstock.com/search/food-menu'  # Change this URL to the actual URL you want to scrape
    headers = {'User-Agent': 'Mozilla/5.0'}
    num_images = scrape_menu_images(base_url, headers)
    print(f"Scraped {num_images} menu images.")
