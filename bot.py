import aiogram
from aiogram import Bot, Dispatcher, executor, types
import logging
import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    """
    Sends to user start message with a short description
    """

    await bot.send_message(message.from_user.id, f'Hi, @{message.from_user.username} 👋 \n\n'
                                                 f'Welcome to @AIPhotoCheck_bot!\n\n'
                                                 f'Send me any picture in .jpg format to analysis it with Error Level Analysis (ELA).\n'
                                                 f'To learn more about ELA use /help command or read: https://en.wikipedia.org/wiki/Error_level_analysis')


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    """
    Sends to user help message with description of the Error Level Analysis methodology
    """
    await bot.send_message(message.from_user.id, f'Error Level Analysis (ELA) permits identifying areas within an image that are at different compression levels. '
                                                 f'With JPEG images, the entire picture should be at roughly the same level. '
                                                 f'If a section of the image is at a significantly different error level, then it likely indicates a digital modification.\n\n'
                                                 f'⚠ Note: send picture as an uncompressed file for best results.')


@dp.message_handler(content_types=['document', 'photo'])
async def photo_analysis(message: types.Message):
    """
    Receives photo or uncompressed file, saves it and process with ELA.
    In final sends 2 photos (ELA only and ELA blended with original image) to user
    """
    pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
