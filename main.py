import asyncio
import logging
import os
import telegram
from random import randint
import requests
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def save_image(url, save_path, payload=None):
    """Сохраняет в корневую папку изображение из URL"""
    response = requests.get(url, params=payload)
    response.raise_for_status()
    with open(save_path, 'wb') as file:
        # raise ValueError('Ошибка при сохранении файла')
        file.write(response.content)


def choosing_random_comic(number):
    """Выбирает случайный комикс-картинку и комментарий к ней """
    url = f'https://xkcd.com/{number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic_details = response.json()
    image_url = comic_details['img']
    comment = comic_details['alt']
    image_name = f'image_{number}.png'
    logger.info(f"Выбран комикс №{number} с комментарием: {comment}")
    return image_url, image_name, comment


def get_random_comic_number():
    """Возвращает номер случайного комикса исходя из возможного диапазона"""
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    max_comic_number = response.json()['num']
    return randint(1, max_comic_number)


async def send_comic(token_tg, chat_id, image_name, comment):
    """Отправляет комикс в чат."""
    bot = telegram.Bot(token_tg)
    with open(image_name, 'rb') as photo:
        # raise ValueError('Ошибка с публикацией')
        await bot.send_photo(chat_id=chat_id, photo=photo, caption=comment)


def main() -> None:
    load_dotenv()
    token_tg = os.environ['TG_TOKEN']
    id_chat = os.environ['ID_CHAT']

    number = get_random_comic_number()
    image_url, image_name, comment = choosing_random_comic(number)

    try:
        save_image(image_url, image_name)
        logger.info(f"Скачан комикс №{number}")
        asyncio.run(send_comic(token_tg, id_chat, image_name, comment))
        logger.info(f'Комикс №{number} отправлен')
    except requests.RequestException as e:
        logger.error(f"Ошибка при скачивании изображения: {e}")
    except ValueError as e:
        logger.error(f"Искусственная ошибка: {e}")
    finally:
        if os.path.exists(image_name):
            os.remove(image_name)
            logger.error(f"Временный файл {image_name} удален")


if __name__ == '__main__':
    main()
