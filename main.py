import speech_recognition as sr
import random
from googletrans import Translator
import langid
import time

def recognize_speech():
    recognizer = sr.Recognizer()
    total_score = 0

    while True:
        random_word_russian = generate_random_word_from_file("easy_russian_words.txt")
        random_word_english = translate_to_english(random_word_russian)

        print(f"Случайное слово на русском: {random_word_russian}")
        print(f"Переведите и произнесите слово правильно! \n"
              f"Для завершения скажите 'enough'.")

        with sr.Microphone() as source:
            print("Скажите перевод слова...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio, language="en-US")
                print(f"Ваш ответ: {text}")

                if text.lower() == "enough":
                    print(f"Игра завершена. Общее количество очков: {total_score}. Спасибо за участие!")
                    break

                if is_english(text):
                    score = handle_phrases(text, random_word_english)
                    total_score += score
                    print(f"Текущий счет: {score}. Общий счет: {total_score}")

                    # Пауза перед следующим словом (3 секунды)
                    time.sleep(2)
                else:
                    print("Речь не распознана")

            except sr.UnknownValueError:
                print("Речь не распознана")
            except sr.RequestError as e:
                print(f"Ошибка при запросе к сервису распознавания: {e}")

def generate_random_word_from_file(file_path):
    words = load_words_from_file(file_path)
    return random.choice(words)

def load_words_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]

def translate_to_english(word):
    translator = Translator()
    translation = translator.translate(word, src="ru", dest="en").text
    return translation

def is_english(text):
    lang, _ = langid.classify(text)
    return lang == 'en'

def handle_phrases(text, expected_english_word):
    if text.lower() == expected_english_word.lower():
        print("Абсолютно верно!!")
        return 100
    else:
        print(f"Неправильно. Правильный ответ: {expected_english_word}.")
        return 0

if __name__ == "__main__":
    recognize_speech()
