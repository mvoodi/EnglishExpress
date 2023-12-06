import speech_recognition as sr
import random
from googletrans import Translator


def recognize_speech():
    recognizer = sr.Recognizer()

    # Добавление случайного слова перед фразой "Говорите что-то..."
    random_word_russian = generate_random_word_from_file("easy_russian_words.txt")
    random_word_english = translate_to_english(random_word_russian)

    print(f"Случайное слово на русском: {random_word_russian}")
    print(f"Случайное слово на английском: {random_word_english}")

    with sr.Microphone() as source:
        print("Говорите что-то...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            print(f"Вы сказали: {text}")

            # Обработка различных фраз
            handle_phrases(text)

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


def handle_phrases(text):
    # Приветствие
    if "привет" in text.lower() or "здравствуйте" in text.lower():
        print("Привет! Как я могу вам помочь?")

    # Ответ на вопрос "Как тебя зовут?"
    elif "как тебя зовут" in text.lower():
        print("Меня зовут Боб.")


if __name__ == "__main__":
    recognize_speech()
