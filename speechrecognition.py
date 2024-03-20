import asyncio
import speech_recognition as sr


trigger_phrases_ua = ["гвинтокрил", "привіт пока до побачення", "твоя мама попросила мене", "ти сьогодні без мами", "пішли зі мною", "відведу додому"]
trigger_phrases_ru = ["вертолет", "привет пока", "твоя мама попросила меня", "сегодня без мам", "пошли со мной", "отведу домой"]


recognizer = sr.Recognizer()


async def process_speech(text: str):
    if not text:
        return

    text = text.lower().replace('ё', 'е')

    for phrase in trigger_phrases_ua:
        if phrase in text:
            print("Found trigger phrase in Ukrainian:", phrase)

    for phrase in trigger_phrases_ru:
        if phrase in text:
            print("Found trigger phrase in Russian:", phrase)


async def recognize_speech_ua(audio):
    try:
        text = recognizer.recognize_google(audio, language="uk-UA")
        print(f'Text in Ukrainian: {text}')
        return text
    except sr.UnknownValueError as e:
        print(f"Don't understand. Error: {e}")
    except sr.RequestError as e:
        print(f"Sorry, there was an error processing your request. Error: {e}")


async def recognize_speech_ru(audio):
    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        print(f'Text in Russian: {text}')
        return text
    except sr.UnknownValueError as e:
        print(f"Don't understand. Error: {e}")
    except sr.RequestError as e:
        print(f"Sorry, there was an error processing your request. Error: {e}")


async def recognize_audio():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print('Listening...')

        while True:
            audio = recognizer.listen(source, phrase_time_limit=4)

            ua_text_task = recognize_speech_ua(audio)
            ru_text_task = recognize_speech_ru(audio)

            ua_text, ru_text = await asyncio.gather(ua_text_task, ru_text_task)
            await process_speech(ua_text)
            await process_speech(ru_text)


async def print_second():
    while True:
        print('Програма працює асинхронно.')
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(
        recognize_audio(),
        print_second()
    )

asyncio.run(main())
