# Please first download FFMPEG  https://ffmpeg.org/  and add to your PATH.  Tutorial - https://www.youtube.com/watch?v=db2xBoH6jPQ&t=5s
# Read README.MD and unpack zip files. Jarvis Sound Pack_ru_ru.zip
# Usage: pip install -r requirements.txt

import asyncio
import re
import pydub
from pydub import playback
import openai
import skills_app
import speech_recognition as sr
from gtts import gTTS

# https://platform.openai.com/account/api-keys
openai.api_key = "API-KEY"

JARVIS_WAKE_WORDS = ["Джарвис", "Ты здесь"]

def get_wake_word(phrase):
    for wake_word in JARVIS_WAKE_WORDS:
        if wake_word.lower() in phrase.lower():
            return wake_word
    return None

def play_audio(file):
    sound = pydub.AudioSegment.from_file(file, format="mp3")
    playback.play(sound)

async def recognize_speech(file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio, language="ru-RU")
        return text
    except sr.UnknownValueError:
        return ""
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return ""

async def synthesize_speech(text, output_file, active_assistant):
    text = re.sub(r"[\U0001F3A8\U0001F60A\U0001F44B\U0001F64F]+", "", text)
    if text.strip():
        tts = gTTS(text=text, lang="ru")
        tts.save(output_file)

async def handle_bot_response(user_input, active_assistant):
    
    if active_assistant in JARVIS_WAKE_WORDS:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты Джарвис помощник Тони Старка. Всегда твой первый ответ будет кратким."},
                {"role": "user", "content": user_input},
            ],
        )
        bot_response = response["choices"][0]["message"]["content"]
        print("Bot's response:", bot_response)
        await synthesize_speech(bot_response, "response.mp3", active_assistant)
        play_audio("response.mp3")

    else:
        bot_response = "Простите, я вас не понял."
        print("Bot's response:", bot_response)

        if active_assistant in JARVIS_WAKE_WORDS:
            await synthesize_speech(bot_response, "response.mp3", active_assistant)
        play_audio("response.mp3")
    return bot_response

async def recognize_command(command, active_assistant, data):
    if active_assistant in JARVIS_WAKE_WORDS:
        if "открой браузер" in command.lower():
            await skills_app.browser(active_assistant)
        elif "закрывай браузер" in command.lower():
            await skills_app.browser_exit(active_assistant)
        elif "открой игру" in command.lower():
            await skills_app.game(active_assistant)
        elif "закрывай игру" in command.lower():
            await skills_app.game_exit(active_assistant)
        elif "выключи компьютер" in command.lower():
            await skills_app.offpc(active_assistant)
        elif "погода" in command.lower():
            await skills_app.weather(active_assistant)
        elif "время" in command.lower():
            await skills_app.time(active_assistant)
        elif "дата" in command.lower():
            await skills_app.date(active_assistant)
        elif "заглушка" in command.lower():
            await skills_app.passive(active_assistant)
        elif active_assistant in JARVIS_WAKE_WORDS:
            bot_response = await handle_bot_response(command, active_assistant)
            await synthesize_speech(bot_response, "response.mp3", active_assistant)
            return bot_response

async def main():
    active_assistant = None

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print(f"Waiting for wake words 'Джарвис'...")
        while True:
            audio = recognizer.listen(source)
            try:
                audio_path = "audio_prompt.wav"
                with open(audio_path, "wb") as f:
                    f.write(audio.get_wav_data())

                phrase = await recognize_speech(audio_path)
                if phrase:
                    print(f"You said: {phrase}")
                    if active_assistant is None:
                        wake_word = get_wake_word(phrase)
                        if wake_word is not None:
                            active_assistant = wake_word
                            if active_assistant in JARVIS_WAKE_WORDS:
                                play_audio("path to sound pack/Jarvis Sound Pack_ru/Jarvis Sound Pack/Да сэр.wav")
                            print("Speak a prompt...")
                            continue

                    if "стоп" in phrase.lower() or "выход" in phrase.lower():
                        if active_assistant in JARVIS_WAKE_WORDS:
                            play_audio("path to sound pack/Jarvis Sound Pack_ru/Jarvis Sound Pack/Выхожу.wav")
                        active_assistant = None
                        print(f"Waiting for wake words 'Джарвис'...")
                        continue

                    if "отключайся" in phrase.lower() or "пока" in phrase.lower():
                        if active_assistant in JARVIS_WAKE_WORDS:
                            play_audio("path to sound pack/Jarvis Sound Pack_ru/Jarvis Sound Pack/Есть.wav")
                        active_assistant = None
                        print(f"Bot's response: Пока!")
                        break

                    await recognize_command(phrase, active_assistant, audio_path)
                    print("Speak a prompt...")

            except Exception as e:
                print("Error transcribing audio: {0}".format(e))
                continue

if __name__ == "__main__":
    asyncio.run(main())