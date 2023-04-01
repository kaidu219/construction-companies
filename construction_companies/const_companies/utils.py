from functools import lru_cache
import json
import os
from django.conf import settings
import requests
from bs4 import BeautifulSoup as bs

def capstroy_parsing():
    url = 'https://www.capstroy.kg/'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    objects = soup.find_all('div', class_='projectItemCard')

    object_dict = {}
    counter = 1
    for i in objects:
        temp_list = {}
        temp_list['title'] = i.find('span', class_='projectTitle').text.strip()
        temp_list['description'] = i.find('span', class_='projectState').text.strip()
        temp_list['address'] = i.find('span', class_='projectStreet').text.strip()
        image = i.find('figure', class_='projectItemCardImage')
        temp_list['images'] = image['style'].strip('background-image:url(')[:-1]
        temp_list['link'] = url + i.find('a')['href'][1:]
        object_dict[counter] = temp_list
        counter += 1
    return {'CAPSTROY_INFO': object_dict}


def imarat_context():
    url_main = 'https://imaratstroy.kg'
    urls = [
        f"{url_main}/ru/zhilaja_nedvizhimost/zavershennye_obekty",
        f"{url_main}/ru/zhilaja_nedvizhimost/stroyaschiesya_obekty",
    ]
    object_dict = {}
    counter = 1

    for url in urls:
        response = requests.get(url)
        soup = bs(response.text, "lxml")
        objects = soup.find_all('div', 'obj-list-item')
        objects_list = [object for object in objects]

        for object in objects_list:
            temp_dict = {}
            temp_dict['title'] = object.find('h2').text
            temp_dict['description'] = object.find('div', class_='descr').text
            temp_dict['address'] = object.find('div', class_='col-lg-6 adres').text
            temp_dict['image'] = url_main + object.find('img')['src']
            temp_dict['link'] = url_main + object.find('a')['href']
            object_dict[counter] = temp_dict
            counter += 1
    
    return {'BUILDING_INFO': object_dict}


def kggroup_parsing():
    url = 'http://kg-group.kg/#objects'
    url_main = 'http://kg-group.kg'
    dict_obj = {}
    counter = 1

    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    objects = soup.find_all('div', class_='col-xl-3 col-lg-3 col-md-6')
    for object in objects:
        temp_dict = {}
        temp_dict['title'] = object.find('h6').text
        temp_dict['description'] = object.find('p').text
        temp_dict['image'] = url_main + object.find('img')['src']
        temp_dict['link'] = url_main + object.find('a')['href']
        dict_obj[counter] = temp_dict
        counter += 1
    return {'KGGROUP_INFO': dict_obj}
    

def ihlas_parsing():
    url = 'https://ihlas.kg/portfolio/'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    builders = soup.find_all('article')

    dict_obj = {}
    counter = 1
    for object in builders:
        temp_dict = {}
        temp_dict['title'] = object.find('h3').text
        temp_dict['address'] = object.find('div', class_='inner portfaddrinner').text.strip()
        temp_dict['description'] = object.find('div', class_='projecttag').text
        link_image = object.find('a', class_='image')
        temp_dict['image'] = url[:-11]+link_image['style'].strip('background-image:')[5:-1]
        temp_dict['link'] = url+link_image['href']
        dict_obj[counter] = temp_dict
        counter += 1
    return {'IHLAS_INFO': dict_obj}


def royal_parsing():
    url = 'https://royal.kg/objects/'
    dict_obj = {}
    counter = 1
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    builders = soup.find_all('div', class_='item')
    for object in builders:
        temp_dict = {}
        temp_dict['title'] = object.find('h4').text
        temp_dict['address'] = object.find('div', class_='address').text.strip()
        temp_dict['description'] = object.find('div', class_='hidden-block').text.strip()
        temp_dict['image'] = object.find('img')['data-original']
        temp_dict['link'] = object.find('a')['href']
        dict_obj[counter] = temp_dict
        counter += 1
    return {'ROYAL_INFO': dict_obj}

def insert_data_file():
    with open(os.path.join(settings.BASE_DIR, 'storage.json'), 'w') as storage:
        context = {
            **imarat_context(), **kggroup_parsing(),
            **ihlas_parsing(), **royal_parsing(), 
            **capstroy_parsing()
        }
        storage.write(json.dumps(context))
