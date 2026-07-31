import joblib
import pandas as pd
import os


class ChurnPredictor:

    def __init__(self):

        model_path = os.path.join(
            "models",
            "churn_model.pkl"
        )

        saved = joblib.load(model_path)

        self.model = saved["model"]

        self.encoders = saved["encoders"]

        self.features = saved["features"]

    def preprocess(self, data):

        df = pd.DataFrame([data])

        for column, encoder in self.encoders.items():

            if column in df.columns:

                try:

                    df[column] = encoder.transform(df[column])

                except:

                    df[column] = 0

        df = df[self.features]

        return df

    def predict(self, customer):

        customer = self.preprocess(customer)

        prediction = self.model.predict(customer)[0]

        probability = self.model.predict_proba(customer)[0][1]

        probability = round(probability * 100, 2)

        if probability >= 80:

            risk = "High"

            color = "danger"

            recommendation = (
                "Immediate retention campaign. "
                "Offer premium benefits and assign a relationship manager."
            )

        elif probability >= 50:

            risk = "Medium"

            color = "warning"

            recommendation = (
                "Send personalized offers and monitor customer activity."
            )

        else:

            risk = "Low"

            color = "success"

            recommendation = (
                "Customer is stable. Continue engagement and loyalty rewards."
            )

        return {

            "prediction": int(prediction),

            "probability": probability,

            "risk": risk,

            "color": color,

            "recommendation": recommendation

        }


predictor = ChurnPredictor()