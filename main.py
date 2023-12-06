import speech_recognition as sr
import random
import nltk

nltk.download("words")

def recognize_speech():
    recognizer = sr.Recognizer()

    # Добавление случайного слова перед фразой "Говорите что-то..."
    random_word = generate_random_word()
    print(f"Случайное слово перед началом: {random_word}")

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

def generate_random_word():
    words = nltk.corpus.words.words()
    return random.choice(words)

def handle_phrases(text):

    if "привет" in text.lower() or "здравствуйте" in text.lower():
        print("Привет! Как я могу вам помочь?")


    elif "как тебя зовут" in text.lower():
        print("Меня зовут Боб.")

if __name__ == "__main__":
    recognize_speech()