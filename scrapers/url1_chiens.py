from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd


def scrap_dog_data (nb_page):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    df = pd.DataFrame()
    for i in range(1,nb_page+1):
        url = f'https://sn.coinafrique.com/categorie/chiens?page={i}'
        driver.get(url)
        resp = driver.page_source
        soup = bs(resp,'html.parser')
        containers = soup.find_all('div', class_='col s6 m4 l3')
        data = []
        for container in containers:
            try:
                nom = container.find('a', class_='card-image ad__card-image waves-block waves-light').get('title', 'Nom non disponible')
                prix = container.find('p', class_='ad__card-price').text.strip()
                adresse = container.find('p', class_='ad__card-location').find('span').get_text(strip=True)
                image_url = container.find('img', class_='ad__card-img')['src']
                dico = {
                    'nom': nom,
                    'prix': prix,
                    'adresse': adresse,
                    'image_url': image_url
                }
                data.append(dico)
            except:
                pass
    DF = pd.DataFrame(data)
    df = pd.concat([df, DF], axis=0).reset_index(drop=True)  
    return df

