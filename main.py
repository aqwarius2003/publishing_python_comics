import requests

def save_image(url, save_path, payload=None):
    response = requests.get(url, params=payload)
    response.raise_for_status()
    with open(save_path, 'wb') as file:
        file.write(response.content)


def download_random_comic(number):
    url = f'https://xkcd.com/{number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic_details = response.json()
    image_url = comic_details['img']
    image_name = f'image_{number}.png'
    save_image(image_url, image_name)

if __name__ == '__main__':
    download_random_comic(22)