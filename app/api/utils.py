import pandas as pd
from fastapi import HTTPException


def validate_dataset(df: pd.DataFrame) -> None:
    """
    Валидирует DataFrame по заданным критериям.

    Args:
        df: DataFrame для валидации.

    Raises:
        HTTPException: Если датасет не соответствует критериям валидации.
    """

    if len(df.columns) < 3:
        raise HTTPException(status_code=400, detail="В датасете должно быть не менее 3 колонок.")

    # 1. Валидация колонки "UserSenderId"
    if "UserSenderId" not in df.columns:
        raise HTTPException(status_code=400, detail="Колонка 'UserSenderId' отсутствует.")
    try:
        df["UserSenderId"] = pd.to_numeric(df["UserSenderId"], errors='raise', downcast='integer')
    except ValueError:
        raise HTTPException(status_code=400, detail="Колонка 'UserSenderId' должна содержать только целые числа.")

    # 2. Валидация колонки "SubmitDate"
    if "SubmitDate" not in df.columns:
        raise HTTPException(status_code=400, detail="Колонка 'SubmitDate' отсутствует.")
    try:
        df["SubmitDate"] = pd.to_datetime(df["SubmitDate"], format="%d %m %Y  %H:%M:%S", errors='raise')
    except ValueError:
        raise HTTPException(status_code=400,
                            detail="Колонка 'SubmitDate' должна быть в формате '15 03 2021  %H:%M:%S'.")

    # 3. Валидация колонки "MessageText"
    if "MessageText" not in df.columns:
        raise HTTPException(status_code=400, detail="Колонка 'MessageText' отсутствует.")
    # Дополнительная проверка формата не требуется, просто проверяем наличие колонки

    # 4. Валидация колонки "Class" (опционально)
    if "Class" in df.columns:
        valid_classes = {"G": 1, "N": 0, "B": -1}

        invalid_classes = []
        for index, row in df.iterrows():
            class_value = row["Class"]
            if class_value not in valid_classes:
                invalid_classes.append(class_value)
        if invalid_classes:
            raise HTTPException(status_code=400,
                                detail=f"Колонка 'Class' содержит недопустимые значения: {', '.join(set(invalid_classes))}. Допустимые значения: G, N, B.")
        df["Class"] = df["Class"].map(valid_classes)  # Преобразуем в числовые значения
