from pandas import DataFrame
from pydantic import BaseModel

from app.core.ml_models import Model


class Application:

    model: Model
    dataset: DataFrame

    def __init__(
            self,
            **kwargs,
    ):
        self.model = Model()
        self.dataset = DataFrame()

    def process_data(self, file: DataFrame) -> DataFrame:
        return self.model.process(file)


def create_app(settings: BaseModel) -> Application:
    return Application(**settings.model_dump())
