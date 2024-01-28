import os
import re
import asyncio
import requests
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types

config = load_dotenv('.env')

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message, state, raw_state):
    await message.reply("Готов к работе!")


@dp.message_handler(commands=['message'])
async def process_message(message: types.Message):
    res = requests.get(f'http://127.0.0.1:5555/')
    await message.answer(res.text)


@dp.message_handler(commands=['post_info'])
async def process_post_info(message: types.Message):
    res = requests.post(f'http://127.0.0.1:5555/post')
    res_data = res.json()
    id = res_data['id']
    timestamp = res_data['timestamp']
    await message.answer(f'id: {id}'
                         '\n'
                         f'timestamp: {timestamp}')


@dp.message_handler(commands=['dog_by_breed'])
async def process_get_breed(message: types.Message):
    breed = re.split('\W+', message.text.removeprefix('/dog_by_breed').strip().lower())[0]
    res = requests.get(f'http://127.0.0.1:5555/dog', params={'kind':breed})
    if res.status_code == 200:
        res_data = res.json()
        msg = '\n'.join(f"{dog['pk']} {dog['name']} ({dog['kind']})" for dog in res_data)
        await message.answer(msg)
    else:
        await message.answer('Собаки с такой пародой нет в базе')


@dp.message_handler(commands=['dog_post_info'])
async def process_dog_post_info(message: types.Message):
    name, pk, kind = re.split('\W+', message.text.removeprefix('/dog_post_info').strip())
    print(name, pk, kind)
    res = requests.post(f'http://127.0.0.1:5555/dog', json={'name':name, 'pk':int(pk), 'kind':kind})
    if res.status_code == 200:
        res_data = res.json()
        msg ='Информация внесена в базу:' '\n' + f"{res_data['pk']} {res_data['name']} ({res_data['kind']})"
        await message.answer(msg)
    else:
        await message.answer('Неверный формат данных')


@dp.message_handler(commands=['dog_info_pk'])
async def process_dog_info_pk(message: types.Message):
    pk = int(re.split('\W+', message.text.removeprefix('/dog_info_pk').strip().lower())[0])
    res = requests.get(f'http://127.0.0.1:5555/dog/{pk}')
    if res.status_code == 200:
        res_data = res.json()
        msg =f"{res_data['pk']} {res_data['name']} ({res_data['kind']})"
        await message.answer(msg)
    else:
        await message.answer('Собаки с таким pk нет в базе')


@dp.message_handler(commands=['dog_update_info'])
async def process_dog_info_pk(message: types.Message):
    current_pk, name, pk, kind = re.split('\W+', message.text.removeprefix('/dog_update_info').strip())
    print(current_pk, name, pk, kind)
    res = requests.patch(f'http://127.0.0.1:5555/dog/{current_pk}', json={'name':name, 'pk':int(pk), 'kind':kind})
    if res.status_code == 200:
        res_data = res.json()
        msg =f"{res_data['pk']} {res_data['name']} ({res_data['kind']})"
        await message.answer(msg)
    else:
        await message.answer('Неверный формат данных')
    
if __name__ == '__main__':
    
    executor.start_polling(dp, skip_updates=False)