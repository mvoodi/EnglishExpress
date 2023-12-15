import os
import speech_recognition as sr
import random
from googletrans import Translator
import langid
import sys


def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        print('\033c', end='')


def display_menu():
    try:
        clear_console()
        print("Меню:")
        print("1: Изменить список слов")
        print("2: Добавить новые слова в список")
        print("3: Игра: Переводческий Марафон")
        print("4: Игра: Фонетический Тренажёр")
        print("5: Выйти")
        choice = input("Выберите номер пункта из меню: ")
        return choice
    except KeyboardInterrupt:
        print("\nПрограмма завершена. Спасибо за использование!")
        sys.exit()


def modify_word_list():
    clear_console()
    file_path = "easy_russian_words.txt"
    confirm = input(f"Вы уверены, что хотите изменить список слов в файле {file_path}? (y/n): ")

    if confirm.lower() == "y":
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                num_words = int(input("Введите количество слов, которые вы хотите ввести (или 'cancel' для отмены): "))

                if num_words < 0:
                    print("Ошибка: Введите корректное число слов.")
                    return

                for _ in range(num_words):
                    word = input("Введите слово (или 'cancel' для отмены): ")
                    if word.lower() == 'cancel':
                        print("Изменение списка слов отменено.")
                        return
                    file.write(word + "\n")
                print("Список слов успешно обновлен!")
        except ValueError:
            print("Ошибка: Введите корректное число слов.")
    else:
        print("Изменение списка слов отменено.")


def add_new_words():
    clear_console()
    file_path = "easy_russian_words.txt"
    confirm = input(f"Вы уверены, что хотите добавить новые слова в файл {file_path}? (y/n): ")

    if confirm.lower() == "y":
        try:
            with open(file_path, "a", encoding="utf-8") as file:
                num_words = int(input("Введите количество слов, которые вы хотите ввести (или 'cancel' для отмены): "))

                if num_words < 0:
                    print("Ошибка: Введите корректное число слов.")
                    return

                for _ in range(num_words):
                    word = input("Введите слово (или 'cancel' для отмены): ")
                    if word.lower() == 'cancel':
                        print("Добавление новых слов отменено.")
                        return
                    file.write(word + "\n")
                print("Новые слова успешно добавлены!")
        except ValueError:
            print("Ошибка: Введите корректное число слов.")
    else:
        print("Добавление новых слов отменено.")


def recognize_speech_game_manual():
    clear_console()
    total_score = 0

    while True:
        random_word_russian = generate_random_word_from_file("easy_russian_words.txt")
        random_word_english = translate_to_english(random_word_russian)

        print(f"Слово на русском: {random_word_russian}")
        print(f"Переведите и введите слово правильно! \n"
              f"Для завершения введите 'exit'.")

        text = input("Введите перевод слова: ")

        if text.lower() == "exit":
            print("Возвращение в меню...")
            return

        if is_english(text):
            if is_english(text):
                score = handle_phrases(text, random_word_english)
            total_score += score
            print(f"Текущий счет: {score}. Общий счет: {total_score}")

        else:
            print("Введенный текст не правильный или язык не поддерживается")


def recognize_speech_game_voice():
    clear_console()
    recognizer = sr.Recognizer()
    total_score = 0
    consecutive_failures = 0
    max_consecutive_failures = 2

    while True:
        random_word_russian = generate_random_word_from_file("easy_russian_words.txt")
        random_word_english = translate_to_english(random_word_russian)

        print(f"Слово на русском: {random_word_russian}")
        print(f"Произнесите слово правильно! \n"
              f"Для завершения произнесите 'exit'.")

        with sr.Microphone() as source:
            print("Скажите перевод слова...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="auto")
            print(f"Ваш ответ: {text}")

            if text.lower() == "exit":
                print("Возвращение в меню...")
                return

            if is_english(text):
                if is_english(text):
                    score = handle_phrases(text, random_word_english)
                total_score += score
                print(f"Текущий счет: {score}. Общий счет: {total_score}")

            else:
                print("Речь не распознана или язык не поддерживается")
                consecutive_failures += 1

        except sr.UnknownValueError:
            print("Речь не распознана. Пожалуйста, повторите.")
            consecutive_failures += 1
        except sr.RequestError as e:
            print(f"Ошибка при запросе к сервису распознавания: {e}")

        if consecutive_failures >= max_consecutive_failures:
            print("Достигнуто максимальное количество неудачных попыток. Переход к следующему слову.")


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


def handle_phrases(text, expected_word):
    if expected_word.lower() in text.lower():
        print("Абсолютно верно!!")
        return 100
    else:
        print(f"Неправильно. Правильный ответ: {expected_word}.")
        return 0


if __name__ == "__main__":
    while True:
        choice = display_menu()

        if choice == '1':
            modify_word_list()
        elif choice == '2':
            add_new_words()
        elif choice == '3':
            recognize_speech_game_manual()
        elif choice == '4':
            recognize_speech_game_voice()
        elif choice == '5':
            print("Спасибо за использование! Возращайтесь! ")
            sys.exit()
        else:
            print("Некорректный выбор. Пожалуйста, выберите 1, 2, 3, 4 или 5.")