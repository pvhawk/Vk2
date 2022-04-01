import time
import requests
import os
# импортируем pprint для более комфортного вывода информации
from pprint import pprint

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def create_folder(self, folder_name):
        create_folder_url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params = {"path": folder_name}
        response = requests.put(create_folder_url, headers=headers, params=params)
        pprint(response.json())
        return response.json()

    def upload_file_to_url(self, file_list):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()

        for photo in file_list:
            pprint(photo)
            url_photo = photo['url']
            filename = photo['file_name']
            name_ph = (f'pvhawk2/{filename}')
            params = {"path": name_ph, "url": url_photo}
            response = requests.post(upload_url, headers=headers, params=params)
            response.raise_for_status()
            if response.status_code == 202:
                print("Success")



if __name__ == '__main__':

    with open('token.txt', 'r') as file_object:
        token = file_object.read().strip()

    with open('token_ya.txt', 'r') as file_object:
        token_ya = file_object.read().strip()

    count_photo = 25

    URL = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': '640428',
        'album_id': 'profile',
        'access_token': token,  # токен и версия api являются обязательными параметрами во всех запросах к vk
        'v': '5.131',
        'count': str(count_photo),
        'extended': '1'
    }
    photo_base = []
    res = requests.get(URL, params=params)
    for photo in range(count_photo):
        photo_base.append({'file_name': f"{res.json()['response']['items'][photo]['likes']['count']}.jpg", 'size': res.json()['response']['items'][photo]['sizes'][-1]['type'], 'url': res.json()['response']['items'][photo]['sizes'][-1]['url']})

    uploader = YaUploader(token_ya)
    uploader.create_folder('pvhawk2')
    result = uploader.upload_file_to_url(photo_base)

