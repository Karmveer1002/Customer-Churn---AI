import pandas as pd
from sklearn.preprocessing import LabelEncoder


class DataPreprocessor:

    def __init__(self):

        self.encoders = {}

        self.feature_columns = []

    def load_dataset(self, file_path):

        df = pd.read_csv(file_path)

        return df

    def clean_dataset(self, df):

        df = df.copy()

        df.drop_duplicates(inplace=True)

        df.drop(columns=["RowNumber"], inplace=True)

        df.drop(columns=["CustomerId"], inplace=True)

        df.drop(columns=["Surname"], inplace=True)

        return df

    def encode_dataset(self, df):

        categorical = [

            "Geography",

            "Gender"

        ]

        for column in categorical:

            encoder = LabelEncoder()

            df[column] = encoder.fit_transform(df[column])

            self.encoders[column] = encoder

        return df

    def prepare_dataset(self, file_path):

        df = self.load_dataset(file_path)

        df = self.clean_dataset(df)

        df = self.encode_dataset(df)

        X = df.drop("Exited", axis=1)

        y = df["Exited"]

        self.feature_columns = list(X.columns)

        return X, y