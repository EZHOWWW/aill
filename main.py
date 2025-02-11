from model import SentimentAnalyzer


def main():
    s = SentimentAnalyzer()
    text = "Это вещь просто отвратительна. Она ужасна до невозможности. Фу. Я так люблю всё что есть на свете. Я обажаю этот мир это потрясающе."
    r = s.predict(text)
    print(r)


if __name__ == "__main__":
    main()
