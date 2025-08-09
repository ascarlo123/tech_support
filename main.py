import telebot
from config import TOKEN
from telebot import types
import sqlite3
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Присвоение токена бота
API_TOKEN = TOKEN
bot = telebot.TeleBot(API_TOKEN)

# Идентификаторы администраторов
ADMIN_ID = [7155079148]  # Замените на реальные идентификаторы администраторов

# Функция для создания таблицы
def create_table():
    connection = sqlite3.connect('tech_support.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT,
            question TEXT
        )
    ''')
    connection.commit()
    connection.close()

# Вызов функции создания таблицы
create_table()

# Частые вопросы
faq = {
    "Как оформить заказ?": "Для оформления заказа, пожалуйста, выберите интересующий вас товар и нажмите кнопку 'Добавить в корзину', затем перейдите в корзину и следуйте инструкциям для завершения покупки.",
    "Как узнать статус моего заказа?": "Вы можете узнать статус вашего заказа, войдя в свой аккаунт на нашем сайте и перейдя в раздел 'Мои заказы'. Там будет указан текущий статус вашего заказа.",
    "Как отменить заказ?": "Если вы хотите отменить заказ, пожалуйста, свяжитесь с нашей службой поддержки как можно скорее. Мы постараемся помочь вам с отменой заказа до его отправки.",
    "Что делать, если товар пришел поврежденным?": "При получении поврежденного товара, пожалуйста, сразу свяжитесь с нашей службой поддержки и предоставьте фотографии повреждений. Мы поможем вам с обменом или возвратом товара.",
    "Как связаться с вашей технической поддержкой?": "Вы можете связаться с нашей технической поддержкой через телефон на нашем сайте или написать нам в чат-бота.",
    "Как узнать информацию о доставке?": "Информацию о доставке вы можете найти на странице оформления заказа на нашем сайте. Там указаны доступные способы доставки и сроки."
}

# Функция для добавления вопроса в базу данных
def add_question(nickname, question):
    connection = sqlite3.connect('tech_support.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Questions (nickname, question) VALUES (?, ?)', (nickname, question))
    connection.commit()
    connection.close()

# Команда старт
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Часто задаваемые вопросы🔍")
    btn2 = types.KeyboardButton("Задать вопрос❓")
    btn3 = types.KeyboardButton("Наш сайт🌐")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}!\nЯ Телеграмм-бот для технической поддержки интернет-магазина 'Все на свете🌟'.".format(message.from_user), reply_markup=markup)

# Функция для отображения главного меню без приветствия
def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Часто задаваемые вопросы🔍")
    btn2 = types.KeyboardButton("Задать вопрос❓")
    btn3 = types.KeyboardButton("Наш сайт🌐")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)

# Кнопка часто задаваемые вопросы
@bot.message_handler(func=lambda message: message.text == "Часто задаваемые вопросы🔍")
def send_faq_questions(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for question in faq.keys():
        markup.add(types.KeyboardButton(question))
    markup.add(types.KeyboardButton("⬅️ Назад"))  # Добавляем кнопку "Назад"
    bot.send_message(message.chat.id, "Выберите вопрос:", reply_markup=markup)

# Обработка нажатия кнопки "Назад"
@bot.message_handler(func=lambda message: message.text == "⬅️ Назад")
def go_back(message):
    show_main_menu(message)  # Возвращаемся к главному меню

# Проверка на наличие вопросов 
@bot.message_handler(func=lambda message: message.text in faq.keys())
def send_faq_answer(message):
    answer = faq[message.text]
    bot.send_message(message.chat.id, answer)

# Кнопка задать вопрос
@bot.message_handler(func=lambda message: message.text == "Задать вопрос❓")
def ask_question(message):
    bot.send_message(message.chat.id, "Пожалуйста, напишите ваш вопрос, и мы постараемся на него ответить.", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, process_question)

@bot.message_handler(func=lambda message: message.text == "Наш сайт🌐")
def our_site(message):
    bot.send_message(message.chat.id, "У нас нету сайта((9")

# Добавление вопроса в базу данных
def add_question(nickname, question):
    connection = sqlite3.connect('tech_support.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Questions (nickname, question) VALUES (?, ?)', (nickname, question))
    connection.commit()
    connection.close()

# Сообщение после добавления вопроса
def process_question(message):
    if not hasattr(message, 'text') or not message.text:
        return bot.send_message(message.chat.id, "Запрос не является текстовым, проверьте ваш вопрос.")
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    question = message.text.strip()
    
    if not question:
        bot.send_message(message.chat.id, "Ваш вопрос не может быть пустым. Пожалуйста, напишите его снова.")
        return
    
    add_question(user_id, question)
    bot.send_message(message.chat.id, "Ваш вопрос отправлен! Мы ответим на него в ближайшее время.📨")
    
    # Уведомляем администраторов о новом вопросе
    for admin_id in ADMIN_ID:
        bot.send_message(admin_id, f"Новый вопрос от {first_name} (ID: {user_id}): {question}")

# Команда для администратора для ответа на вопросы
@bot.message_handler(commands=['reply'])
def reply_to_question(message):
    if message.chat.id in ADMIN_ID:  # Проверка, является ли пользователь администратором
        connection = sqlite3.connect('tech_support.db')
        cursor = connection.cursor()
        cursor.execute('SELECT id, nickname, question FROM Questions')
        questions = cursor.fetchall()
        connection.close()

        if not questions:
            bot.send_message(message.chat.id, "Нет вопросов для ответа.")
            return

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for q in questions:
            question_text = f"ID: {q[0]}, {q[1]}: {q[2]}"
            markup.add(types.KeyboardButton(question_text))
        markup.add(types.KeyboardButton("⬅️ Назад"))  # Кнопка "Назад"
        bot.send_message(message.chat.id, "Выберите вопрос, чтобы ответить:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "У вас нет прав для этой команды.")

# Обработка выбора вопроса для ответа
@bot.message_handler(func=lambda message: message.text.startswith("ID:"))
def handle_reply(message):
    question_id = int(message.text.split(",")[0].split(":")[1].strip())
    bot.send_message(message.chat.id, "Введите ваш ответ:")
    bot.register_next_step_handler(message, lambda msg: send_reply(msg, question_id))

# Функция для отправки ответа пользователю
def send_reply(message, question_id):
    answer = message.text.strip()
    if not answer:
        bot.send_message(message.chat.id, "Ответ не может быть пустым. Пожалуйста, введите его снова.")
        return
    
    connection = sqlite3.connect('tech_support.db')
    cursor = connection.cursor()
    cursor.execute('SELECT nickname FROM Questions WHERE id = ?', (question_id,))
    result = cursor.fetchone()
    connection.close()

    if result:
        user_id = result[0]
        logging.info(f"Attempting to send message to user ID: {user_id}")
        try:
            # Отправляем ответ пользователю
            bot.send_message(user_id, f"Ответ на ваш вопрос: {answer}")
            bot.send_message(message.chat.id, "Ответ отправлен пользователю.")
        except Exception as e:
            logging.error(f"Failed to send message to user ID {user_id}: {e}")
    else:
        bot.send_message(message.chat.id, "Вопрос не найден.")

if __name__ == '__main__':
    bot.polling()
