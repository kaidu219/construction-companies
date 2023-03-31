import requests
from bs4 import BeautifulSoup as bs
import lxml

def capstroy_parsing():
    url = 'https://www.capstroy.kg/'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    objects = soup.find_all('div', class_='projectItemCard')
    objects_list = [i for i in objects]

    objects_dict = {}
    counter = 1
    for i in objects_list:
        temp_dict = {}
        temp_dict['title'] = i.find('span', class_='projectTitle').text.strip()
        temp_dict['description'] = i.find('span', class_='projectState').text.strip()
        temp_dict['address'] = i.find('span', class_='projectStreet').text.strip()
        image = soup.select_one('figure.projectItemCardImage')
        temp_dict['image'] = image['style'].strip('background-image:url(')[:-1]
        objects_dict[counter] = temp_dict
        counter += 1
    
    print(objects_dict)
    return objects_dict


urls = ["https://imaratstroy.kg/ru/zhilaja_nedvizhimost/zavershennye_obekty","https://imaratstroy.kg/ru/zhilaja_nedvizhimost/stroyaschiesya_obekty"]
object_dict = {}
counter = 1

for url in urls:
    response = requests.get(url)
    soup = bs(response, "lxml")
    object = soup.find_all('div', 'obj-list-item')
    

