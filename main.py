import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Говорите что-то...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            print(f"Вы сказали: {text}")
        except sr.UnknownValueError:
            print("Речь не распознана")
        except sr.RequestError as e:
            print(f"Ошибка при запросе к сервису распознавания: {e}")

if __name__ == "__main__":
    recognize_speech()