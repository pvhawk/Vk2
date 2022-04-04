import requests
import json
from pprint import pprint
from progress.bar import IncrementalBar


class VK_photo:
    def __init__(self, token: str):
        self.token = token

    def get_vk_user_photo(self, owner_id: str, count_photo: int):
        URL = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'access_token': self.token,  # токен и версия api являются обязательными параметрами во всех запросах к vk
            'v': '5.131',
            'count': str(count_photo),
            'extended': '1'
        }
        self.photo_base = []
        res = requests.get(URL, params=params)
        for photo in range(count_photo):
            self.photo_base.append({'file_name': f"{res.json()['response']['items'][photo]['likes']['count']}.jpg", 'size': res.json()['response']['items'][photo]['sizes'][-1]['type'], 'url': res.json()['response']['items'][photo]['sizes'][-1]['url']})
        return self.photo_base

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

    def upload_file_to_url(self, file_list, owner_id: str):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        # print(len(file_list))
        bar = IncrementalBar('Downloads', max=len(file_list))

        for photo in file_list:
            url_photo = photo['url']
            filename = photo['file_name']
            name_ph = (f'{owner_id}/{filename}')
            params = {"path": name_ph, "url": url_photo}
            response = requests.post(upload_url, headers=headers, params=params)

            response.raise_for_status()
            if response.status_code == 202:
                bar.next()
                # print("Success")

        bar.finish()



if __name__ == '__main__':

    with open('token.txt', 'r') as file_object:
        token = file_object.read().strip()

    with open('token_ya.txt', 'r') as file_object:
        token_ya = file_object.read().strip()

    count_photo = 5
    owner_id = '254800'

    vk_photo = VK_photo(token)

    photo_base = vk_photo.get_vk_user_photo(owner_id, count_photo)
    # pprint(photo_base)

    uploader = YaUploader(token_ya)

    uploader.create_folder(owner_id)
    result = uploader.upload_file_to_url(photo_base, owner_id)
    photo_json = []

    for photo in photo_base:
        photo.pop("url")
        photo_json.append(photo)

    # pprint(photo_json)
    with open('Photo_json.txt', 'w') as outfile:
        json.dump(photo_json, outfile)



