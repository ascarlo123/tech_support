import telebot
from config import TOKEN
from telebot import types

API_TOKEN = TOKEN
bot = telebot.TeleBot(API_TOKEN)

# Список часто задаваемых вопросов и ответов
faq = {
    "Как оформить заказ?": "Для оформления заказа, пожалуйста, выберите интересующий вас товар и нажмите кнопку 'Добавить в корзину', затем перейдите в корзину и следуйте инструкциям для завершения покупки.",
    "Как узнать статус моего заказа?": "Вы можете узнать статус вашего заказа, войдя в свой аккаунт на нашем сайте и перейдя в раздел 'Мои заказы'. Там будет указан текущий статус вашего заказа.",
    "Как отменить заказ?": "Если вы хотите отменить заказ, пожалуйста, свяжитесь с нашей службой поддержки как можно скорее. Мы постараемся помочь вам с отменой заказа до его отправки.",
    "Что делать, если товар пришел поврежденным?": "При получении поврежденного товара, пожалуйста, сразу свяжитесь с нашей службой поддержки и предоставьте фотографии повреждений. Мы поможем вам с обменом или возвратом товара.",
    "Как связаться с вашей технической поддержкой?": "Вы можете связаться с нашей технической поддержкой через телефон на нашем сайте или написать нам в чат-бота.",
    "Как узнать информацию о доставке?": "Информацию о доставке вы можете найти на странице оформления заказа на нашем сайте. Там указаны доступные способы доставки и сроки."
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Часто задаваемые вопросы")
    btn2 = types.KeyboardButton("Задать вопрос")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}!\nЯ Телеграмм-бот для технической поддержки интернет-магазина 'Все на свете'.".format(message.from_user), reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Часто задаваемые вопросы")
def send_faq_questions(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for question in faq.keys():
        markup.add(types.KeyboardButton(question))
    
    bot.send_message(message.chat.id, "Выберите вопрос:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in faq.keys())
def send_faq_answer(message):
    answer = faq[message.text]
    bot.send_message(message.chat.id, answer)

@bot.message_handler(func=lambda message: message.text == "Задать вопрос")
def ask_question(message):
    bot.send_message(message.chat.id, "Пожалуйста, напишите ваш вопрос, и мы постараемся на него ответить.")

if __name__ == '__main__':
    bot.polling()
