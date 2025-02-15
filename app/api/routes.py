import io
import os

import fastapi.responses
import pandas as pd
import openpyxl
from fastapi import APIRouter
from fastapi import File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from app.core import Application, APP_SETTINGS, create_app
from .config import settings
from .utils import validate_dataset

application: Application = create_app(APP_SETTINGS)
router = APIRouter(
    prefix=settings.prefix,
    tags=settings.tags,
)


@router.post("/upload_dataset/")
async def upload_dataset(file: UploadFile = File(...)):
    """
    Загружает CSV или Excel (xls/xlsx) файл, валидирует его,
    запускает модель для предсказания тональности и возвращает
    датасет с предсказанной колонкой "Class".

    Args:
        file: Загружаемый файл.

    Returns:
        JSONResponse: Весь датафрейм с предсказанной колонкой "Class" в формате JSON.
                       Возвращает ошибку, если файл не поддерживается или не проходит валидацию.
    """

    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="Имя файла не указано.")

        file_parts = file.filename.split(".")
        if len(file_parts) <= 1:  # No extension found
            raise HTTPException(status_code=400, detail="Не указано расширение файла.")

        file_extension = file_parts[-1].lower()

        if file_extension == "csv":
            contents = await file.read()
            df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        elif file_extension in ["xls", "xlsx"]:
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла.  Поддерживаются CSV, XLS и XLSX.")

        # Валидация датасета
        # validate_dataset(df)

        # Предсказание тональности с помощью модели
        df = application.process_data(df)

        # Маппинг числовых значений обратно в строковые представления классов
        reverse_mapping = {1: "G", 0: "N", -1: "B"}
        df["Class"] = df["Class"].map(reverse_mapping)  # Преобразуем обратно в G, N, B

        application.dataset = df

        print(df)

        # Возвращаем весь датафрейм с предсказаниями
        # return JSONResponse(content=df.to_dict(orient="records"))
        return fastapi.responses.Response("Success")

    except Exception as e:
        # Обработка ошибок чтения файла и других исключений
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке файла: {str(e)}")


@router.get("/predict_dataset/")
async def predict_dataset():
    if application.dataset is None:
        return fastapi.responses.Response("Не загружен датасет", 400)

    application.process_data(application.dataset)
    return fastapi.responses.Response("Success")


@router.get("/download_dataset/")
async def download_dataset():
    if application.dataset is None:
        return fastapi.responses.Response("Не загружен датасет", 400)

    application.dataset.to_csv("temp.csv", index=False)

    return fastapi.responses.FileResponse("temp.csv", filename="dataset.csv")


