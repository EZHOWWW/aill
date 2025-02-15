from pandas import DataFrame
import numpy as np


class Model:
    name: str

    def __init__(self, **kwargs):
        pass

    def process(self, data: DataFrame) -> DataFrame:
        data["Class"] = np.random.choice(["G", "B", "N"], data.shape[0])
        return data
