import math
import vkbottle.bot
from vkbottle_types import *
import sqlite3
import os
from vkbottle.callback import BotCallback
from vkbottle import CtxStorage, BaseStateGroup
from Data import config, txt
import os
import google.cloud.dialogflow
from vkbottle.bot import Bot, Message
import random
import re
import sqlite3
import vk as vk
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink, Location, EMPTY_KEYBOARD
from vkbottle.tools.dev.keyboard import button


bot = Bot(config.TOKEN)

dialogflow = google.cloud.dialogflow
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "configbot.json"
session_client = dialogflow.SessionsClient()
project_id = 'id'
session_id = 'sessions'
language_code = 'ru'
session = session_client.session_path(project_id, session_id)


TOKEN = os.getenv("VK_TOKEN")
url = os.getenv("https://vk.com/michurinai_bot")
title = os.getenv("MichurinAI_bot")
secret_key = os.getenv("VK_SECRET_KEY")
callback = BotCallback(
    url = url,
    title = title
)



ctx = CtxStorage()


class Test(BaseStateGroup):
    QUEST1 = 0
    QUEST2 = 1
    QUEST3 = 2
    QUEST4 = 3
    QUEST5 = 4
    END = 5


@bot.on.private_message(text="Меню")
async def handler(message: Message):
    keyboard = Keyboard()

    keyboard.add(Text("Где найти Мичуринские яблоки?"), KeyboardButtonColor.POSITIVE)

    keyboard.row()

    keyboard.add(OpenLink("https://t.me/MichurinAi_bot", "Мы в Telegram"))
    keyboard.add(Text("Что я могу?"), KeyboardButtonColor.PRIMARY)
    await message.answer("Добро пожаловать в меню!", keyboard=keyboard)


@bot.on.private_message(text="Что я могу?")
async def function(message:  Message):
    keyboard = Keyboard(one_time=False)

    keyboard.add(Text("Афиша"), KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("find"), KeyboardButtonColor.POSITIVE)

    keyboard.row()

    keyboard.add(Text("Квест"), KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Предложить"), KeyboardButtonColor.POSITIVE)

    keyboard.row()

    keyboard.add(Text("Меню"), KeyboardButtonColor.NEGATIVE)
    await message.answer("Вот что я умею", keyboard=keyboard)


@bot.on.private_message(text="Квест")
async def quests(message:  Message):
    keyboard = Keyboard(one_time=True)

    keyboard.add(Text("Начинаем!"), KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Меню"), KeyboardButtonColor.NEGATIVE)

    await message.answer("Начинаю викторину!", keyboard=keyboard)


@bot.on.private_message(lev="Начинаем!")
async def quest(message: Message):
     await bot.state_dispenser.set(message.peer_id, Test.QUEST1)
     return txt.hi, txt.ask1


@bot.on.private_message(state=Test.QUEST1)
async def quest1(message: Message):
     ctx.set('answer1', message.text)
     await bot.state_dispenser.set(message.peer_id, Test.QUEST2)
     return txt.ask2


@bot.on.private_message(state=Test.QUEST2)
async def quest2(message: Message):
     ctx.set('answer2', message.text)
     await bot.state_dispenser.set(message.peer_id, Test.QUEST3)
     return txt.ask3


@bot.on.private_message(state=Test.QUEST3)
async def quest3(message: Message):
     ctx.set('answer3', message.text)
     await bot.state_dispenser.set(message.peer_id, Test.QUEST4)
     return txt.ask4


@bot.on.private_message(state=Test.QUEST4)
async def quest4(message: Message):
    ctx.set("answer4", message.text)
    await bot.state_dispenser.set(message.peer_id, Test.QUEST5)
    return txt.ask5


@bot.on.private_message(state=Test.QUEST5)
async def quest5(message: Message):
    ctx.set("answer5", message.text)
    await bot.state_dispenser.set(message.peer_id, Test.END)
    await message.answer("Произвожу подсчет баллов")


@bot.on.private_message(state=Test.END)
async def answer_q5(message: Message):
    answer1 = ctx.get("answer1")
    answer2 = ctx.get("answer2")
    answer3 = ctx.get("answer3")
    answer4 = ctx.get("answer4")
    answer5 = ctx.get("answer5")

    def check_answers():
        scores = 0
        if answer1 == "Рязанская" or answer1 == "Рязанская область" or answer1 == "Рязанская губерния" or answer1 == "В Рязанской" or answer1 == "рязанская" or answer1 == "в рязанской":
            scores += 1
        if answer2 == "В 1855 году" or answer2 == "1855" or answer2 == "1855 год":
            scores += 1
        if answer3 == "В 1872 году" or answer3 == "1872" or answer3 == "1872 год":
            scores += 1
        if answer4 == "17 лет" or answer4 == "17" or answer4 == "лет 17":
            scores += 1
        if answer5 == "Память Мичурина" or answer5 == "память мичурина":
            scores += 1
        return scores

    score = check_answers()

    await message.answer(f"Ваши баллы: {score}")


@bot.on.private_message(text="Афиша")
async def advert(message: Message):

    await message.answer(txt.ad)


@bot.on.private_message(text="/find")
async def handle_locate(message: Message, keyboards=None):
    await message.answer('Здравствуйте, нажмите на кнопку, чтобы отправить своё местоположение', keyboard=keyboards.locate.keyboard_location)
    await bp.storage.set(message.peer_id, {"command": "find"})


@bot.on.private_message(geo=True, state={"command": "find"})
async def handle_geo(message: Message, geo: Geo, state: dict):
    latitude_user = geo.coordinates.latitude
    longitude_user = geo.coordinates.longitude

    def distance(lat1, lon1, lat2, lon2):
        R = 6371  # радиус Земли в км
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dLon / 2) * math.sin(dLon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    connect = sqlite3.connect('maib_admin/db.sqlite3')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM admin_panel_geo")
    result_geo = cursor.fetchall()

    min_distance = None
    closest_coordinate = None
    closest_name = None
    all_coordinates = []

    for row in result_geo:
        url = row[3]
        name = row[1]
        match = re.search(r"@([\d\.]+),([\d\.]+)", url)
        latitudes = float(match.group(1))
        longitudes = float(match.group(2))
        dist = distance(latitudes, longitudes, latitude_user, longitude_user)
        if min_distance is None or dist < min_distance:
            min_distance = dist
            closest_coordinate = (latitudes, longitudes)
            closest_name = name
        all_coordinates.append((name, (latitudes, longitudes), dist))

    inline_keyboard = []
    for name, coordinate, dist in sorted(all_coordinates, key=lambda x: x[2])[1:3]:
        inline_keyboard.append(
            {
                "text": f"{name} ({dist:.2f} км)",
                "callback_data": f"location_{coordinate[0]}_{coordinate[1]}"
            }
        )

    await message.answer(f"Ближайшая к вам достопримечательность: {closest_name}")
    await message.answer_location(closest_coordinate[0], closest_coordinate[1])
    await bp.storage.set(message.peer_id, {})


@bot.on.callback_query(payload={"cmd": "location"})
async def process_location_callback(query: CallbackQuery):
    _, latitude, longitude = query.payload['data'].split('_')
    await bp.api.messages.send(
        user_id=query.from_id,
        lat=float(latitude),
        long=float(longitude),
        random_id=0
    )
    await bp.api.messages.mark_as_answered(callback_id=query.id)


@bot.on.callback_query()
async def process_callback_button(query: CallbackQuery):
    # Разбиваем строку callback_data на параметры с помощью символа "="
    callback_data = query.payload['data']
    event_id = int(callback_data.split("=")[1])

    # Получаем информацию о мероприятии из базы данных
    connect = sqlite3.connect('maib_admin/db.sqlite3')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM admin_panel_poster WHERE id = ?", (event_id,))
    event_info = cursor.fetchone()

    # Отправляем сообщение с информацией о мероприятии
    message = (
        f'Здравствуйте, ожидается мероприятие "{event_info[1]}"\n'
        f'Описание: {event_info[2]}\n'
        f'Мероприятие походит по адресу {event_info[4]}, ({event_info[3]})\n'
        f'Дата: {event_info[5]}\n'
        f'Возраст: {event_info[6]}\n'
    )
    await bp.api.messages.send(user_id=query.from_id, message=message, random_id=0)
    await bp.api.messages.mark_as_answered(callback_id=query.id)


@bot.on.private_message(text="Предложить")
async def suggest(message: Message):

    await message.answer(txt.sugg)


@bot.on.private_message(text="<msg>")
async def send_message(ans: Message, msg):
    language = 'ru'
    text_input = dialogflow.TextInput(
        text=msg, language_code=language)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        session=session, query_input=query_input)
    if response.query_result.fulfillment_text:
        await ans.answer(response.query_result.fulfillment_text)
    else:
        await ans.answer("Я вас не понял, мне пора в сад")


bot.run_forever()
