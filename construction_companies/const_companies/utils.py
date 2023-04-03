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

    # парсим объекты компании
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

    # парсим контакты компании
    contacts = {}
    url_contacts = url + 'contacts'
    response_c = requests.get(url_contacts)
    soup_c = bs(response_c.text, 'lxml')
    address = soup_c.find('div', class_='contacts_section_two_text_desc').text.strip()
    contacts['address'] = address
    number = soup_c.find('div', class_='contacts_section_two_text_desc_num').text.strip().split('\n\n\n')
    contacts['number'] = number
    schedule = soup_c.find_all('div', class_='contacts_section_two_text_desc_num')
    schedule_l = [i.text.strip().split('\n') for i in schedule][1]
    contacts['schedule'] = schedule_l
    contacts['link'] = url
    object_dict['contacts'] = contacts

    # парсим информацию о компании
    about_company = {}
    response_a = requests.get(url+"about")
    soup_a = bs(response_a.text, 'lxml')
    title = soup_a.find('p', class_='title text-dark text-left top-in-view').text.strip()
    text = soup_a.find('span', class_='about_section2_desc mt-4').text.strip()
    about_company['title'] = title
    about_company['text'] = text
    object_dict['about_company'] = about_company

    # считаем кол-во объектов
   
    object_dict['counter'] = counter_objects(object_dict)

    return {'CAPSTROY_INFO': object_dict}


def imarat_context():
    url_main = 'https://imaratstroy.kg'
    urls = [
        f"{url_main}/ru/zhilaja_nedvizhimost/zavershennye_obekty",
        f"{url_main}/ru/zhilaja_nedvizhimost/stroyaschiesya_obekty",
    ]
    object_dict = {}
    counter = 1
    # парсим объекты компании
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
    
    # парсим контакты компании
    response_c = requests.get(url_main)
    soup_c = bs(response_c.text, 'lxml')
    contact = {}
    address = soup_c.find('div', class_='menu-phone').text.split('\n')[3]
    contact['address'] = address
    numbers = soup_c.find('div', class_='menu-phone').text.split('\n')[4]
    contact['numbers'] = numbers
    contact['link'] = url_main
    object_dict['contact'] = contact

    # парсим информацию о компании
    url_about = 'https://imaratstroy.kg/ru/o_nashej_kompanii/o_nas'
    response_a = requests.get(url_about)
    soup_a = bs(response_a.text, 'lxml')
    about_company = {}
    title = soup_a.find('div', class_='cont').text.split('\n')[1][:44]
    text = soup_a.find('div', class_='cont').text.split('\n')[1][44:]
    about_company['title'] = title
    about_company['text'] = text
    object_dict['about_company'] = about_company

    # считаем кол-во объектов
    object_dict['counter'] = counter_objects(object_dict)

    return {'BUILDING_INFO': object_dict}


def kggroup_parsing():
    url = 'http://kg-group.kg/#objects'
    url_main = 'http://kg-group.kg'
    dict_obj = {}
    counter = 1

    # парсим объекты компании
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

    # парсим контакты компании
    url_cont = 'http://kg-group.kg/#contacts'
    response_c = requests.get(url_cont)
    soup_c = bs(response_c.text, 'lxml')
    contact = {}
    address = soup_c.find('div', class_='contact_info').text.strip().split('\n')[0]
    number = soup_c.find('div', class_='contact_info').text.strip().split('\n')[1:-1]
    numbers = [i.lstrip() for i in number]
    contact['address'] = address
    contact['numbers'] = numbers
    contact['link'] = url_main
    dict_obj['contact'] = contact

    # парсим информации о компании
    url_about = 'http://kg-group.kg/#video'
    response_a = requests.get(url_about)
    soup_a = bs(response_a.text, 'lxml')
    about = {}
    title = soup_a.find('section', id='video').text.strip().split('\n')[0]
    text_s = soup_a.find('section', id='video').text.strip().split('\n')[6:-56]
    text = (', ').join([i.strip() for i in text_s])
    about['title'] = title
    about['text'] = text
    dict_obj['about'] = about

    # считаем кол-во объектов
    dict_obj['counter'] = counter_objects(dict_obj)

    return {'KGGROUP_INFO': dict_obj}
    

def ihlas_parsing():
    url_main = 'https://ihlas.kg/'
    url = 'https://ihlas.kg/portfolio/'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    builders = soup.find_all('article')

    # парсим все объекты компании
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
    
    # парсим контакты компании
    url_contact = url_main + 'contact/'
    response_c = requests.get(url_contact)
    soup_c = bs(response_c.text, 'lxml')
    contact = {}
    address_l = soup_c.find('address').text.strip().split('\n')
    address = (' ').join([i.strip() for i in address_l])
    number = soup_c.find_all('a', class_='phone-link teltex')
    numbers = [i.get('href')[4:] for i in number]
    contact['address'] = address
    contact['number'] = numbers
    contact['link'] = url_main
    dict_obj['contact'] = contact

    # парсим информацию о компании 
    url_about = url_main + 'about/'
    responce_a = requests.get(url_about)
    soup_a = bs(responce_a.text, 'lxml')
    about = {}
    general = soup_a.find_all('p')
    about['title'] = general[1].text
    about['text'] = general[2].text
    dict_obj['about'] = about

    # считаем кол-во объектов
    dict_obj['counter'] = counter_objects(dict_obj)

    return {'IHLAS_INFO': dict_obj}


def royal_parsing():
    url_main = 'https://royal.kg/'
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

    # парсим контакты компании
    response_c = requests.get(url_main)
    soup_c = bs(response_c.text, 'lxml')
    contact = {}
    cont = soup_c.find('ul', class_='right').text.strip().split('\n')
    contact['address'] = cont[0]
    contact['number'] = cont[1:-1]
    contact['link'] = url_main
    dict_obj['contact'] = contact

    # парсим информацию о компании
    url_about = url_main + 'about-us/'
    response_a = requests.get(url_about)
    soup_a = bs(response_a.text, 'lxml')
    about = {}
    text = soup_a.find('div', class_='description').text.strip()
    about['text'] = text
    dict_obj['about'] = about

    # считаем кол-во объектов
    dict_obj['counter'] = counter_objects(dict_obj)

    return {'ROYAL_INFO': dict_obj}

def insert_data_file():
    with open(os.path.join(settings.BASE_DIR, 'storage.json'), 'w') as storage:
        context = {
            **imarat_context(), **kggroup_parsing(),
            **ihlas_parsing(), **royal_parsing(), 
            **capstroy_parsing()
        }
        storage.write(json.dumps(context))

def counter_objects(global_dict: dict)->int:
    counter = 0
    for k in global_dict.keys():
        if str(k).isdigit():
            counter += 1
    return counter