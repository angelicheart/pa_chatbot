import os
import logging
import json
from random import choice

from google.cloud import dialogflow
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import telegram_token, project_id, users
import keyboards as nav


bot = Bot(token=telegram_token)
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account-file.json"

session_client = dialogflow.SessionsClient()
session_id = 'sessions'
language_code = 'ru'
session = session_client.session_path(project_id, session_id)


def read_data():
    with open('data.json', encoding='utf-8') as file:
        d = json.load(file)
    return d


data = read_data()


def add_json(new_data, category, filename='data.json'):
    with open(filename, 'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        file_data[category].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4, ensure_ascii=False)


def get_rand_data(s):
    data_rand = choice(data[s])
    string = ''
    string += f'📌 {data_rand["name"]}\n{data_rand["description"]}\n\n\n'
    return string


@dp.message_handler(commands=['start', 'menu'])
async def start(message: types.Message):
    await message.answer('Привет, {0.first_name}'.format(message.from_user), reply_markup=nav.welcome_keyboard)


def category_check(cat):
    if cat == '💵 Стажировки/вакансии':
        return 'vacancies'

    elif cat == '⏰ Дедлайны учебных активностей':
        return 'deadlines'

    elif cat == '📗 Отработка долгов':
        return 'debts'

    elif cat == '🗞 Расписание учебных и внеучебных мероприятий':
        return 'timetable'


class FormAdd(StatesGroup):
    category = State()
    name = State()
    description = State()


class FormRemove(StatesGroup):
    category = State()
    name = State()


@dp.message_handler(lambda message: message.chat.id in users, commands=['add', 'добавить'])
async def cmd_add_start(message: types.Message):
    await FormAdd.category.set()
    markup = nav.add_remove
    await message.reply("Выберите категорию", reply_markup=markup)


@dp.message_handler(lambda message: message.chat.id in users, commands=['remove', 'удалить'])
async def cmd_remove_start(message: types.Message):
    await FormRemove.category.set()
    markup = nav.add_remove
    await message.reply("Выберите категорию", reply_markup=markup)


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('Cancelled.', reply_markup=nav.welcome_keyboard)


# remove state
@dp.message_handler(state=FormRemove.category)
async def process_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data_remove:
        data_remove['category'] = message.text

    await FormRemove.next()
    await message.reply("Введите название объекта", reply_markup=types.ReplyKeyboardRemove())
    await data_output(category_check(data_remove['category']), message)


@dp.message_handler(state=FormRemove.name)
async def process_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data_remove:
        data_remove['name'] = message.text

    global data
    temp = category_check(data_remove['category'])
    data[temp] = [x for x in data[temp] if x['name'] not in data_remove['name']]

    with open('data.json', 'w', encoding='utf-8') as data_file:
        json.dump(data, data_file, indent=4, ensure_ascii=False)

    await bot.send_message(message.from_user.id, "Объект успешно удален", reply_markup=nav.welcome_keyboard)
    data = read_data()
    await state.finish()


# add state
@dp.message_handler(state=FormAdd.category)
async def process_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data_add:
        data_add['category'] = message.text

    await FormAdd.next()
    await message.reply("Введите название объекта", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=FormAdd.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data_add:
        data_add['name'] = message.text

    await FormAdd.next()
    await message.reply("Введите описание объекта")


@dp.message_handler(state=FormAdd.description)
async def process_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data_add:
        data_add['description'] = message.text

    obj = {"name": data_add['name'],
           "description": data_add['description']}

    add_json(obj, category_check(data_add['category']))

    await bot.send_message(message.from_user.id, "Объект успешно добавлен", reply_markup=nav.welcome_keyboard)
    global data
    data = read_data()
    await state.finish()


@dp.message_handler()
async def menu(message: types.Message):
    if message.text == '📚 Категории':
        await bot.send_message(message.from_user.id, '📚 Категории', reply_markup=nav.category_keyboard)

    elif message.text == '🔝 Главное меню':
        await bot.send_message(message.from_user.id, '🔝 Главное меню', reply_markup=nav.welcome_keyboard)

    elif message.text == '👥 Социальные сети кафедры':
        await socials(message)

    elif message.text == '💵 Стажировки/вакансии':
        await data_output('vacancies', message)

    elif message.text == '⏰ Дедлайны учебных активностей':
        await data_output('deadlines', message)

    elif message.text == '📗 Отработка долгов':
        await data_output('debts', message)

    elif message.text == '🗞 Расписание учебных и внеучебных мероприятий':
        await data_output('timetable', message)

    elif message.text == '❓ Задать вопрос':
        await bot.send_message(message.from_user.id, 'Вы можете задать вопрос боту, который перенаправит вас на\
                                                     одну из категорий')

    else:
        await dialogflow_prompter(message)


async def dialogflow_prompter(message: types.Message):
    text_input = dialogflow.TextInput(text=message.text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)

    if response.query_result.fulfillment_text == 'socials':
        await bot.send_message(message.from_user.id, f"Возможно вы имели ввиду:", reply_markup=nav.inlineSocials)

    elif response.query_result.fulfillment_text == 'work':
        await bot.send_message(message.from_user.id, f"Возможно вы имели ввиду:\n{get_rand_data('vacancies')}",
                               reply_markup=nav.inlineWork)

    elif response.query_result.fulfillment_text == 'debt':
        await bot.send_message(message.from_user.id, f"Возможно вы имели ввиду:\n{get_rand_data('debts')}",
                               reply_markup=nav.inlineDebt)

    elif response.query_result.fulfillment_text == 'deadlines':
        await bot.send_message(message.from_user.id, f"Возможно вы имели ввиду:\n{get_rand_data('deadlines')}",
                               reply_markup=nav.inlineDeadline)

    elif response.query_result.fulfillment_text == 'timetable':
        await bot.send_message(message.from_user.id, f"Возможно вы имели ввиду:\n{get_rand_data('timetable')}",
                               reply_markup=nav.inlineTimetable)

    else:
        await bot.send_message(message.from_user.id, response.query_result.fulfillment_text)


@dp.callback_query_handler(text=['socials', 'vacancies', 'debts', 'deadlines', 'timetable'])
async def response_button(call: types.CallbackQuery):
    if call.data == 'socials':
        await socials(call)
    await data_output(call.data, call)


async def data_output(a, message):
    string = ''
    for i in data[a]:
        string += f'📌 {i["name"]}\n{i["description"]}\n\n\n'
    if string != '':
        await bot.send_message(message.from_user.id, string)
    else:
        await bot.send_message(message.from_user.id, 'Категория пуста')


async def socials(message):
    await bot.send_message(message.from_user.id, f'👥 Социальные сети кафедры\n<a href="https://vk.com/">VK</a>'
                                                 '\n<a href="https://www.instagram.com/">IG</a>', parse_mode="HTML")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
