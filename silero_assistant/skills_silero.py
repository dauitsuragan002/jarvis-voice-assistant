import os
import subprocess
import webbrowser
import asyncio
import datetime
import app
import aiohttp
import psutil


jarvis_yes = 'path to sound pack/Jarvis Sound Pack_ru/Загружаю сэр.wav'
jarvis_off = 'path to sound pack/Jarvis Sound Pack_ru/Отключаю питание 2.wav'
ok_always = 'path to sound pack/Jarvis Sound Pack_ru/Всегда к вашим услугам сэр.wav'


async def browser(active_assistant):
    '''Открывает браузер, указанный по умолчанию в системе, с указанным URL'''
    webbrowser.open('https://www.youtube.com/@dautmantis/videos', new=2)
    if active_assistant in app.JARVIS_WAKE_WORDS:
       app.play_audio(jarvis_yes)

async def browser_exit(active_assistant):
    '''Закрывает браузер'''
    browser_processes = ["chrome.exe", "firefox.exe", "msedge.exe" , "browser.exe"]

    closed = False
    for process in psutil.process_iter():
        try:
            if process.name().lower() in browser_processes:
                process.terminate()
                closed = True
        except psutil.Error:
            pass

    if closed:
        if active_assistant in app.JARVIS_WAKE_WORDS:
            app.play_audio(jarvis_yes)
    else:
        print("Bot's response: Процесс браузера не найден.")
        await app.assistant_tts('Процесс браузера не найден.', 'output.mp3', active_assistant)
        

async def game(active_assistant):
    try:
        os.startfile("C:/Users/dauit/OneDrive/Рабочий стол/Hill Climb Racing.lnk")
        if active_assistant in app.JARVIS_WAKE_WORDS:
           app.play_audio(jarvis_yes)
    except:
        print("Bot's response: Путь к файлу не найден, проверьте, правильный ли путь ?")
        await app.assistant_tts('Путь к файлу не найден, проверьте, правильный ли путь?', 'output.mp3', active_assistant)
        

async def game_exit(active_assistant):
    try:
        if active_assistant in app.JARVIS_WAKE_WORDS:
            app.play_audio(ok_always)

        process_name = 'C:/Users/dauit/OneDrive/Рабочий стол/Hill Climb Racing.lnk'

        for proc in psutil.process_iter():
            try:
                if proc.name() == process_name:
                    proc.terminate()
            except psutil.NoSuchProcess:
                pass
    except:
        print("Bot's response: Произошла ошибка при попытке закрытия игры.")
        await app.assistant_tts('Произошла ошибка при попытке закрытия игры', 'output.mp3', active_assistant)
        

async def offpc(active_assistant):
    '''Отключает ПК под управлением Windows'''
    if active_assistant in app.JARVIS_WAKE_WORDS:
        app.play_audio(jarvis_off)
    os.system('shutdown /s /t 0')
    print("Bot's response: ПК был бы выключен, но команде # в коде мешает ;))) ")
    await app.assistant_tts('ПК был бы выключен, но команде # в коде мешает ;)))', 'output.mp3', active_assistant)
    

async def weather(active_assistant):
    '''Погода'''
    async with aiohttp.ClientSession() as session:
        try:
            place = "Astana"
            # API in site https://openweathermap.org/
            url = f'https://api.openweathermap.org/data/2.5/weather?q={place}&appid=YOUR_API&units=metric&lang=ru'
            async with session.get(url) as response:
                data = await response.json()
                status = data['weather'][0]['description']
                temp = data['main']['temp']
        except aiohttp.ClientError as e:
            print(f"Произошла ошибка при попытке запроса к ресурсу API:{e}")
            await app.synthesize_speech(f'Произошла ошибка при попытке запроса к ресурсу API:{e}', 'output.mp3', active_assistant)
        else:
            print(f"Bot's response: На улице {status} {temp} градусов")
            await app.synthesize_speech(f"На улице {status} {temp} градусов", 'output.mp3', active_assistant)
            app.play_audio('output.mp3')
            

async def offBot():
    '''Отключает бота'''
    asyncio.get_event_loop().stop()

async def passive(active_assistant):
    '''Пассив'''
    if active_assistant in app.JARVIS_WAKE_WORDS:
        app.play_audio(jarvis_yes)
    else:
        print("Bot's response: Я вас слышаю пассивно.")
        await app.assistant_tts(f"Bot's response: Я вас слышаю пассивно.", 'output.mp3', active_assistant)

async def time(active_assistant):
    '''Возвращает текущее время'''
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    print(f"Сейчас {current_time}")
    try:
        await app.assistant_tts(f"Сейчас {current_time}", 'output.mp3', active_assistant)
        
    except:
        print("Bot's response: Произошла ошибка. Вы же можете сам посмотреть на экран компьютера или телефона")
        await app.assistant_tts('Произошла ошибка. Вы же можете сам посмотреть на экран компьютера или телефона', 'output.mp3', active_assistant)
        

async def date(active_assistant):
    '''Возвращает текущую дату'''
    now = datetime.datetime.now()
    current_date = now.strftime("%d.%m.%Y")
    print(f"Сегодня {current_date}")
    try:
        await app.assistant_tts(f"Сегодня {current_date}", 'output.mp3', active_assistant)
        
    except:
        print("Bot's response: Произошла ошибка. Вы же можете сам посмотреть на экран компьютера или телефона")
        await app.assistant_tts('Произошла ошибка. Вы же можете сам посмотреть на экран компьютера или телефона', 'output.mp3', active_assistant)
        