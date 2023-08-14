from config import TOKEN, GROUP_ID
import filters
import logging
from aiogram import *

from filters import IsAdminFilter

logging.basicConfig(level=logging.INFO) #log lvl

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

dp.filters_factory.bind(IsAdminFilter)

@dp.message_handler(content_types=['new_chat_members'])
async def on_user_joined(message: types.Message):
    await message.delete()

@dp.message_handler(is_admin=True, commands=['ban'], commands_prefix='!/')
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply('Эта команда должна быть ответом на сообщение.')
        return

    await message.bot.delete_message(GROUP_ID, message.message_id)
    await message.bot.kick_chat_member(chat_id=GROUP_ID, user_id=message.reply_to_message.from_user.id)

    await message.reply_to_message.reply('Пользователь заблокирован.')

@dp.message_handler(commands=['chatid'])
async def chatid(message: types.Message):
    await bot.send_message(message.chat.id,
                           text=f'Chat ID: {message.chat.id}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)