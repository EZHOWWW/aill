import os  # Добавьте импорт модуля os

import gradio as gr
import requests

from app.api.config import settings as api_setting
from app.config import settings as app_setting


def upload_dataset(file_obj):
    """Загружает файл и возвращает сообщение об успехе/ошибке."""
    try:
        filename = os.path.basename(file_obj.name)  # Получаем имя файла из пути
        files = {'file': (filename, open(file_obj.name, 'rb'))}  # Используем имя файла
        response = requests.post(f"http://{app_setting.run.host}:{app_setting.run.port}{api_setting.prefix}/upload_dataset/",
                                 files=files)  # Измените на ваш URL
        response.raise_for_status()  # Проверка на HTTP ошибки
        return "Файл успешно загружен!" + "\n" + response.text
    except requests.exceptions.RequestException as e:
        return f"Ошибка загрузки файла: {e}"


def process_dataset():
    """Запускает обработку файла."""
    try:
        response = requests.get(
            f"http://{app_setting.run.host}:{app_setting.run.port}{api_setting.prefix}/predict_dataset/")  # Измените на ваш URL
        response.raise_for_status()
        return "Файл успешно обработан!" + "\n" + response.text
    except requests.exceptions.RequestException as e:
        return f"Ошибка обработки файла: {e}"


def download_dataset():
    """Запускает скачивание файла."""
    try:
        response = requests.get(f"http://{app_setting.run.host}:{app_setting.run.port}{api_setting.prefix}/download_dataset/",
                                stream=True)  # Измените на ваш URL
        response.raise_for_status()

        # Extract filename from headers
        content_disposition = response.headers.get("Content-Disposition")
        if content_disposition:
            filename = content_disposition.split("filename=")[1].strip('"')
        else:
            filename = "downloaded_data.csv"  # Default name

        return "simple.py"

    except requests.exceptions.RequestException as e:
        return f"Ошибка скачивания файла: {e}"


with gr.Blocks() as demo:
    file_input = gr.File(file_types=[".csv", ".xlsx", ".xls"], label="Загрузить датасет (CSV/XLSX/XLS)")
    upload_button = gr.Button("Загрузить")
    process_button = gr.Button("Обработать датасет")
    download_button = gr.Button("Скачать датасет")

    upload_output = gr.Textbox(label="Результат загрузки")
    process_output = gr.Textbox(label="Результат обработки")
    download_output = gr.File(label="Скачать обработанный файл")

    upload_button.click(upload_dataset, inputs=file_input, outputs=upload_output)
    process_button.click(process_dataset, inputs=None, outputs=process_output)
    download_button.click(download_dataset, inputs=None, outputs=download_output)

if __name__ == "__main__":
    demo.launch()
