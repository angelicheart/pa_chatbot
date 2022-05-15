from aiogram.types import \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


welcome_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row('📚 Категории', '❓ Задать вопрос')

menuButton = KeyboardButton('🔝 Главное меню')

add_remove = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
add_remove.add("💵 Стажировки/вакансии")
add_remove.add("⏰ Дедлайны учебных активностей")
add_remove.add("📗 Отработка долгов")
add_remove.add("🗞 Расписание учебных и внеучебных мероприятий")


category_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
category_keyboard.row('👥 Социальные сети кафедры', '💵 Стажировки/вакансии')
category_keyboard.row('⏰ Дедлайны учебных активностей', '📗 Отработка долгов')
category_keyboard.row('🗞 Расписание учебных и внеучебных мероприятий', menuButton)

button1 = InlineKeyboardButton(text="👥 Социальные сети кафедры", callback_data="socials")
inlineSocials = InlineKeyboardMarkup().add(button1)

button2 = InlineKeyboardButton(text="💵 Стажировки/вакансии", callback_data="vacancies")
inlineWork = InlineKeyboardMarkup().add(button2)

button3 = InlineKeyboardButton(text="📗 Отработка долгов", callback_data="debts")
inlineDebt = InlineKeyboardMarkup().add(button3)

button4 = InlineKeyboardButton(text="⏰ Дедлайны учебных активностей", callback_data="deadlines")
inlineDeadline = InlineKeyboardMarkup().add(button4)

button5 = InlineKeyboardButton(text="🗞 Расписание учебных и внеучебных мероприятий", callback_data="timetable")
inlineTimetable = InlineKeyboardMarkup().add(button5)
