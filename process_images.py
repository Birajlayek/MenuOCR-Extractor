import pytesseract
from PIL import Image
import re
import sqlite3
import os

def process_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    
    items_prices = extract_items_prices(text)
    return items_prices

def extract_items_prices(text):
    items_prices = []
    lines = text.split('\n')
    
    for line in lines:
        match = re.match(r'(.+)\s+(\d+\.?\d*)', line.strip())
        if match:
            item = match.group(1).strip()
            price = float(match.group(2).strip())
            items_prices.append((item, price))
    
    return items_prices

def create_database():
    conn = sqlite3.connect('menus.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            price REAL
        )
    ''')
    conn.commit()
    conn.close()

def store_items_prices(items_prices):
    conn = sqlite3.connect('menus.db')
    cursor = conn.cursor()
    
    for item, price in items_prices:
        cursor.execute('''
            INSERT INTO menu_items (item_name, price)
            VALUES (?, ?)
        ''', (item, price))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    image_dir = 'menu_images'
    
    for filename in os.listdir(image_dir):
        if filename.endswith('.jpg'):
            image_path = os.path.join(image_dir, filename)
            items_prices = process_image(image_path)
            store_items_prices(items_prices)
            print(f"Processed and stored items from {filename}: {items_prices}")
