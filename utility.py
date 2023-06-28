import pandas
from pandas.core.interchange import dataframe


def load_training_data() -> dataframe:
    with open("Data/data.csv", "r") as f:
        return pandas.read_csv(f)
