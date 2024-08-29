import requests
import logging
from dotenv import load_dotenv
import os
from random import randint
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext


# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def save_image(url, save_path, payload=None):
    """Сохраняет в корневую папку изображение из URL"""
    try:
        response = requests.get(url, params=payload)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response.content)
        logger.info(f"Изображение успешно сохранено: {save_path}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при качивании комикса с URL {url}: {e}")
    except Exception as e:
        logger.error(f"Ошибка при сохранении изображения: {e}")


def download_random_comic():
    """Скачивает случайный комикс-картинку и комментарий к ней """
    try:
        number = get_random_comic_number()
        url = f'https://xkcd.com/{number}/info.0.json'
        response = requests.get(url)
        response.raise_for_status()
        comic_details = response.json()
        image_url = comic_details['img']
        comment = comic_details['alt']
        image_name = f'image_{number}.png'
        save_image(image_url, image_name)
        logger.info(f"Скачан комикс №{number} с комментарием: {comment}")
        return image_name, comment
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')


def get_random_comic_number():
    """Возвращает номер случайного комикса исходя из возможного диапазона"""
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    max_comic_number = response.json()['num']
    return randint(1, max_comic_number)


async def publish_to_tg_chat(update: Update, context: CallbackContext, image_name: str, comment: str):
    """Отправляет случайный комикс в чат и удаляет файл после отправки."""
    chat_id = update.effective_chat.id
    with open(image_name, 'rb') as photo:
        status_publish = await context.bot.send_photo(chat_id=chat_id, photo=image_name, caption=comment)
    if status_publish:
        os.remove(image_name)
        logger.error(f"Фото {image_name} удалено")
    else:
        logger.error(f"Ошибка при отправке комикса {image_name}")


async def handle_send_comic(update: Update, context: CallbackContext) -> None:
    image_name, comment = download_random_comic()
    await publish_to_tg_chat(update, context, image_name, comment)


def main() -> None:
    load_dotenv()
    token_tg = os.environ['TG_TOKEN']
    dp = ApplicationBuilder().token(token_tg).build()
    # dp = updater.dispatcher

    dp.add_handler(CommandHandler('send_me_comic', handle_send_comic))


    dp.run_polling()


if __name__ == '__main__':
    main()
