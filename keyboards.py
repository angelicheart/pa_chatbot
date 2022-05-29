from aiogram.types import \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


welcome_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row('📚 Категории', '❓ Задать вопрос')
welcome_keyboard.row('🗓 Учебный план', '🌎 Полезные ссылки')

menuButton = KeyboardButton('🔝 Главное меню')

add_remove = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
add_remove.add("💵 Стажировки/вакансии")
add_remove.add("⏰ Дедлайны учебных активностей")
add_remove.add("📗 Отработка долгов")
add_remove.add("🗞 Расписание мероприятий")


category_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
category_keyboard.row('👥 Социальные сети кафедры', '💵 Стажировки/вакансии')
category_keyboard.row('⏰ Дедлайны учебных активностей', '📗 Отработка долгов')
category_keyboard.row('🗞 Расписание мероприятий', menuButton)

button1 = InlineKeyboardButton(text="👥 Социальные сети кафедры", callback_data="socials")
inlineSocials = InlineKeyboardMarkup().add(button1)

button2 = InlineKeyboardButton(text="💵 Стажировки/вакансии", callback_data="vacancies")
inlineWork = InlineKeyboardMarkup().add(button2)

button3 = InlineKeyboardButton(text="📗 Отработка долгов", callback_data="debts")
inlineDebt = InlineKeyboardMarkup().add(button3)

button4 = InlineKeyboardButton(text="⏰ Дедлайны учебных активностей", callback_data="deadlines")
inlineDeadline = InlineKeyboardMarkup().add(button4)

button5 = InlineKeyboardButton(text="🗞 Расписание мероприятий", callback_data="timetable")
inlineTimetable = InlineKeyboardMarkup().add(button5)

numb1 = InlineKeyboardButton(text="1", callback_data="1")
numb2 = InlineKeyboardButton(text="2", callback_data="2")
numb3 = InlineKeyboardButton(text="3", callback_data="3")
numb4 = InlineKeyboardButton(text="4", callback_data="4")

num = InlineKeyboardMarkup().add(numb1, numb2)
num.add(numb3, numb4)
