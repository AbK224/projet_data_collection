from bs4 import BeautifulSoup as bs
from requests import get
import pandas as pd


def scrap_dog_others (nb_page):
    df = pd.DataFrame()
    for i in range(1,nb_page+1):
        url = f'https://sn.coinafrique.com/categorie/autres-animaux?page={i}'
        resp = get(url)
        soup = bs(resp.content,'html.parser')
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
    df = pd.concat([df, DF], axis=0).reset_index(drop=True) # 
    return df

