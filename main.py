import telebot
from telebot import types

bot = telebot.TeleBot ('')

user_data = {}  # словарь для хранения состояния игры

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Приветствую тебя! Давай проверим твое знание в медицине, напиши /game и мы начнем.")

@bot.message_handler(commands=['game'])
def start_game(message):
    chat_id = message.chat.id
    user_data[chat_id] = {"current_kadr": "kadr1"}
    markup = create_keyboard(kadr1_options, chat_id)
    bot.send_message(chat_id, "Начнем игру!\nПри посещении галереи Вы заметили, как упала женщина примерно 65-70 лет.", reply_markup=markup)

def create_keyboard(options, chat_id):
    markup = types.InlineKeyboardMarkup()
    for i, option in enumerate(options):
        callback_data = f"{user_data[chat_id]['current_kadr']}:{i}"
        print(f"Создана callback_data: {callback_data}") # Добавлено для отладки
        markup.add(types.InlineKeyboardButton(text=option, callback_data=f"{user_data[chat_id]['current_kadr']}:{i}"))
    return markup


kadr1_options = [
    "1)Уйти в другую сторону", #конец игры, предложить сыграть ещё раз.
    "2)Позвать на помощь и вместе пойти к пострадавшей", #переход на следущий кадр
    "3)Указать прохожему на упавшую женщину и пройти в другую сторону самому", #конец игры, предложить сыграть ещё раз
    "4)Вызвать скорую помощь" #переход вызова и концу игры. 
]

kadr2_1_options = [
    "1)Уйти в другую сторону", #конец игры, предложить сыграть ещё раз
    "2)Попытаться привести в чувства, похлопывая по щекам", #переход на следущий кадр
    "3)Вызвать скорую помощь" #конец игры, предложить сыграть ещё раз
]

kadr4_options = [
    "1)Покинуть место происшествия", #конец игры, предложить сыграть ещё раз
    "2)Оценить дыхание и пульс и вызвать скорую помощь", #переход на следущий кадр
    "3)Вызвать скорую помощь" #конец игры, предложить сыграть ещё раз
]

kadr6_options = [
    "1)Покинуть место происшествия", #конец игры, предложить сыграть ещё раз
    "2)Начать сердечно-легочную реанимацию и вызвать СМП", #переход на следущий кадр 
    "3)Вызвать скорую помощь", # конец игры, предложить сыграть ещё раз
    "4)Начать искусственное дыхание «рот в рот», вызвать СМП" #отправка сообщения что результата нет, конец игры, предложить сыграть ещё раз.
]

kadr7_options = [
    "1)Продолжить СЛР до появления результата", #
    "2)Вызвать скорую помощь повторно", #
    "3)Позвать на помощь окружающих", #
    "4)Остановить СЛР и отправиться на поиск квалифицированной помощи" #
]

kadr8_options = [
    "1)Антеро-латеральная позиция",
    "2)Латеро-латеральное позиция",
    "3)Передне-задняя позиция"
]

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    print(f"Полученные данные: {call.data}")
    chat_id = call.message.chat.id
    data = call.data.split(':')
    current_kadr = data[0]
    choice = int(data[1])

    # Начало игры и возврат к нему
    if current_kadr == "kadr1":
        if choice == 0:
            message = "Человек умер.\n\nХорошо, что это только проверка твоих знаний, давай ещё раз!\n\nПри посещении галереи Вы заметили, как упала женщина примерно 65-70 лет."
            user_data[chat_id]["current_kadr"] = "kadr1" #Возврат на кадр 1
            bot.send_message(chat_id, message, reply_markup=create_keyboard(kadr1_options, chat_id))
        elif choice == 1:
            user_data[chat_id]["current_kadr"] = "kadr2_1"  # обновляем текущий кадр
            bot.send_message(chat_id, "Вы кричите - «На помощь, помогите кто-нибудь»; Подходит прохожий и спрашивает «Что случилось?» - Идете с прохожим к женщине", reply_markup=create_keyboard(kadr2_1_options, chat_id))  # переход на 2_1
        elif choice == 2:
            message = "Человек умер.\n\nХорошо, что это только проверка твоих знаний, давай ещё раз!\n\nПри посещении галереи Вы заметили, как упала женщина примерно 65-70 лет."
            user_data[chat_id]["current_kadr"] = "kadr1" #Возврат на кадр 1
            bot.send_message(chat_id, message, reply_markup=create_keyboard(kadr1_options, chat_id))
        elif choice == 3:
            message = "Вы набирает 112 на телефон – Отвечает диспетчер, вы - называете место происшествия (галерея?), пол и возраст пострадавшей (женщина, примерно 70 лет), что случилось (упала, обездвижена). Ответ диспетчера – к вам выехали."
            bot.send_message(chat_id, "Игра окончена!\n\nЕсли вы хотите увидеть другой результат или проверить свои знания то сыграйте ещё раз /game")  # Сообщение об окончании игры.

    # Кадр переходящий от choice == 1.
    elif current_kadr == "kadr2_1":
        if choice == 0:
            message = "Человек умер.\n\nХорошо, что это только проверка твоих знаний, давай ещё раз!\n\nПри посещении галереи Вы заметили, как упала женщина примерно 65-70 лет."
            user_data[chat_id]["current_kadr"] = "kadr1" #Возврат на кадр 1
            bot.send_message(chat_id, message, reply_markup=create_keyboard(kadr1_options, chat_id))
        elif choice == 1:
            user_data[chat_id]["current_kadr"] = "kadr4"  # обновляем текущий кадр
            bot.send_message(chat_id, "Пострадавшая молчит и не двигается.\nВаши действия.", reply_markup=create_keyboard(kadr4_options, chat_id))  # переход на кадр 4
        elif choice == 2:
            message = "Вы набираете 112 на телефоне – Отвечает диспетчер, вы - называет место происшествия (галерея?), пол и возраст пострадавшей (женщина, примерно 70 лет), что случилось (упала, обездвижена). Ответ диспетчера – к вам выехали."
            bot.send_message(chat_id, "Игра окончена!\n\nЕсли вы хотите увидеть другой результат или проверить свои знания то сыграйте ещё раз /game")  # Сообщение об окончании игры.

    # Кадр переходящий от choice == 1
    elif current_kadr == "kadr4":
        if choice == 0:
            message = "Человек умер.\n\nХорошо, что это только проверка твоих знаний, давай ещё раз!\n\nПри посещении галереи Вы заметили, как упала женщина примерно 65-70 лет."
            user_data[chat_id]["current_kadr"] = "kadr1" #Возврат на кадр 1
            bot.send_message(chat_id, message, reply_markup=create_keyboard(kadr1_options, chat_id))
        elif choice == 1:
            user_data[chat_id]["current_kadr"] = "kadr6"  # обновляем текущий кадр
            bot.send_message(chat_id, "Демонстрация (вид сбоку) – выдвижение нижней челюсти, 10-сек оценка дыхания и пульса на магистральных артериях (сонные). В это время помощник вызывает СМП и называет место происшествия (галерея?) пол и возраст пострадавшей (женщина, примерно 70 лет), что случилось (упала, обездвижена). Ответ диспетчера – к вам выехали.", reply_markup=create_keyboard(kadr6_options, chat_id)) # переход на кадр 6
        elif choice == 2:
            message = "Вы набираете 112 на телефон – Отвечает диспетчер, вы - называете место происшествия (галерея?), пол и возраст пострадавшей (женщина, примерно 70 лет), что случилось (упала, обездвижена). Ответ диспетчера – к вам выехали."
            bot.send_message(chat_id, "Игра окончена!\n\nЕсли вы хотите увидеть другой результат или проверить свои знания то сыграйте ещё раз /game")  # Сообщение об окончании игры.

    # Кадр переходящий от choice == 1
    elif current_kadr == "kadr6":
        if choice == 0:
            message = "Человек умер.\n\nХорошо, что это только проверка твоих знаний, давай ещё раз!\n\nПри посещении галереи Вы заметили, как упала женщина примерно 65-70 лет."
            user_data[chat_id]["current_kadr"] = "kadr1" #Возврат на кадр 1
            bot.send_message(chat_id, message, reply_markup=create_keyboard(kadr1_options, chat_id))
        elif choice == 1:
            user_data[chat_id]["current_kadr"] = "kadr7"  # обновляем текущий кадр
            bot.send_message(chat_id, "Демонстрация СЛР – 30/2, вид сбоку + бегущая линия с точками для попадания в ритм СЛР (мб музыкальное сопровождение) – запомнить количество попаданий в ритм. В это время помощник осуществляет 2 вдоха", reply_markup=create_keyboard(kadr7_options, chat_id)) # переход на кадр 7
        elif choice == 2:
            message = "Вы набираете 112 на телефоне – Отвечает диспетчер, вы - называете место происшествия (галерея?), пол и возраст пострадавшей (женщина, примерно 70 лет), что случилось (упала, обездвижена). Ответ диспетчера – к вам выехали."
            bot.send_message(chat_id, "Игра окончена!\n\nЕсли вы хотите увидеть другой результат или проверить свои знания то сыграйте ещё раз /game")  # Сообщение об окончании игры.
        elif choice == 3:
            message = "При отсутствии признаков дыхания и кровообращения необходима качественно и количественно замещать обе утраченные функции. При выполнении только одного маневра (искусственное дыхание или только непрямой массаж сердца) – эффективность и результативность СЛР стремится к 0. К сожалению, на фоне не эффективной СЛР постаравшаяся скончалась, не дождавшись приезда СМП.\n\nИгра окончена.\n\nПри посещении галереи Вы заметили, как упала женщина примерно 65-70 лет."
            user_data[chat_id]["current_kadr"] = "kadr1" #Возврат на кадр 1
            bot.send_message(chat_id, message, reply_markup=create_keyboard(kadr1_options, chat_id))
            
    #Кадр 7
    elif current_kadr == "kadr7":
        if choice == 0:
            user_data[chat_id]["current_kadr"] = "kadr8"  # обновляем текущий кадр
            bot.send_message(chat_id, "Продолжающаяся СЛР", reply_markup=create_keyboard(kadr8_options, chat_id)) #Переход на кадр 8
        elif choice == 1:
            bot.send_message(chat_id, "Повторный вызов СМП!\n\nВозможен только через 20 минут от первоначального вызова (среднее время ожидания по Москве). Не рекомендуется чаще звонить в СМП. Лучше сосредоточиться на проведении СЛР\nРешение хорошее,даем вам ещё время на обдуми.", reply_markup=create_keyboard(kadr7_options, chat_id))
            user_data[chat_id]["current_kadr"] = "kadr7" #Возврат на кадр 7
        elif choice == 2:
            bot.send_message(chat_id, "Вы кричите - «На помощь, помогите кто-нибудь!»,\n Подходят прохожие. Начинают снимать происходящее на телефон, дают бесполезные советы. Кто-то просто кричит рядом. Сцена длится 1 минуту. Прерывается приездом СМП и прорыванием СМП через толпу.\n\nХороший результат, вы сделали все, что в ваших силах и ответили верно на мои вопросы.\nПоздравляю!\n\nСыграем ещё? /game и мы начнем.")
        elif choice == 3:
            message =  "Человек умер.\nНеплохое решение, но лучше было бы продолжить делать СЛР! Давай ещё раз!\n\nПри посещении галереи Вы заметили, как упала женщина примерно 65-70 лет."
            user_data[chat_id]["current_kadr"] = "kadr1" #Возврат на кадр 1 
            bot.send_message(chat_id, message, reply_markup=create_keyboard(kadr1_options, chat_id))
          

    #Кадр 8
    elif current_kadr == "kadr8":
        if choice == 0:
            message = "Демонстрация положения электродов и демонстрация применения АНД (с учетом продолжения СЛР). Оживление пострадавшей. Демонстрация приезда бригады СМП.\nПоздравляю! Вы спасли человека и прошли игру!"
            bot.send_message(chat_id, message)
            bot.send_message(chat_id, "Игра окончена!")  # Сообщение об окончании игры.
        elif choice == 1:
            message = "Демонстрация положения электродов и демонстрация применения АНД (с учетом продолжения СЛР). Оживление пострадавшей. Демонстрация приезда бригады СМП.\nПоздравляю! Вы спасли человека и прошли игру!"
            bot.send_message(chat_id, message)
            bot.send_message(chat_id, "Игра окончена!")  # Сообщение об окончании игры.
        elif choice == 2:
            message = "Демонстрация положения электродов и демонстрация применения АНД (с учетом продолжения СЛР). Оживление пострадавшей. Демонстрация приезда бригады СМП.\nПоздравляю! Вы спасли человека и прошли игру!"
            bot.send_message(chat_id, message)
            bot.send_message(chat_id, "Игра окончена!")  # Сообщение об окончании игры.
        elif choice == 0:
            message = "Демонстрация положения электродов и демонстрация применения АНД (с учетом продолжения СЛР). Оживление пострадавшей. Демонстрация приезда бригады СМП.\nПоздравляю! Вы спасли человека и прошли игру!"
            bot.send_message(chat_id, message)
            bot.send_message(chat_id, "Игра окончена!")  # Сообщение об окончании игры.


bot.polling()