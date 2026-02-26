import sqlite3


def get_connection():
    return sqlite3.connect("scraped_data.db")

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE animals_data(nom,price,adresse,image_url)''')
    conn.commit()
    conn.close()
    