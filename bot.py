import shutil
import logging
import config
import os
from aiogram import Bot, Dispatcher, executor, types
from audio_processor import AudioProcessor
from image_processor import ImageProcessor

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)


def log_info(message):
    logging.info(
        f'[{message.date}] Recieved message <{message.content_type}> from {message.from_user.username} [id:{message.from_user.id}]')


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    """
    Sends user start message with a short description
    """
    await bot.send_message(message.from_user.id,
                           f'Привет, @{message.from_user.username} 👋 \n\n'
                           f'Это бот для тестового задания компании ID R&D')


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    """
    Sends user help message with description of the Error Level Analysis methodology
    """
    await bot.send_message(message.from_user.id,
                           'который умеет : 1. Сохранять аудиосообщения из диалогов в базу данных (СУБД или на диск) по идентификаторам пользователей.\n'
                           '2. Конвертирует все аудиосообщения в формат wav с частотой дискретизации 16kHz.'
                           'Формат записи: uid —> [audio_message_0, audio_message_1, ..., audio_message_N].\n'
                           '3. Определяет есть ли лицо на отправляемых фотографиях или нет, сохраняет только те, где оно есть')


@dp.message_handler(content_types=['photo'])
async def photo_analysis(message: types.Message):
    log_info(message)
    downloaded_file_path = os.path.join('TEMP',
                                        f'{message.from_user.username}-{message.from_user.id}_{message.date.strftime("%d%m%y_%H-%M-%S")}.jpg')
    await message.photo[-1].download(destination_file=downloaded_file_path,
                                     make_dirs=True)
    img_processor = ImageProcessor(downloaded_file_path)
    img_processor.detect_faces()

    if img_processor.faces:
        if not os.path.exists('photos_with_face'):
            os.mkdir('photos_with_face')
        processed_file_path = os.path.join('photos_with_face',
                                            f'{message.from_user.username}-{message.from_user.id}_{message.date.strftime("%d%m%y_%H-%M-%S")}.jpg')
        os.replace(downloaded_file_path, processed_file_path)
    shutil.rmtree('TEMP')


@dp.message_handler(content_types=['voice'])
async def audio_processing(message: types.Message):
    log_info(message)
    downloaded_file_path = os.path.join('TEMP', 'audio_message_temp')
    if os.path.exists(str(message.from_user.id)) and os.listdir(
            str(message.from_user.id)):
        last_file = os.listdir(str(message.from_user.id))[-1][:-4]
        order_number = int(last_file.split('_')[-1]) + 1
        resampled_file_path = os.path.join(str(message.from_user.id),
                                           f'audio_message_{order_number}.wav')
    else:
        resampled_file_path = os.path.join(str(message.from_user.id),
                                           'audio_message_0.wav')
    await message.voice.download(
        destination_file=downloaded_file_path + '.ogg', make_dirs=True)
    AudioProcessor.save_as_wav(input_file_path=downloaded_file_path,
                               output_file_path=resampled_file_path)
    shutil.rmtree('TEMP')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
