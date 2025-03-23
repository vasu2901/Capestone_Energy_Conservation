import pandas as pd
from django.shortcuts import render
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import numpy as np

global_df = None

def home(request):
    return render(request, "index.html")


def read_data(request):
    global global_df
    try:
        if global_df is None or global_df.empty:
            # Load the Excel file
            data = pd.read_excel(
                r"capestoneapp/Generation_Metatable_Data_1740834320048.xlsx"
            )

            # Remove rows where 'Source' is NaN
            data = data.dropna(subset=["Source"])

            # Pivot the DataFrame to rearrange columns
            pivot_df = data.pivot(
                index=["Year", "State"], columns="Source", values="Generation (In MU)"
            ).reset_index()

            # Ensure all expected columns are present
            expected_columns = [
                "oil-gas",
                "hydro",
                "small-hydro",
                "solar",
                "nuclear",
                "wind",
                "coal",
                "bio-power",
            ]
            for col in expected_columns:
                if col not in pivot_df.columns:
                    pivot_df[col] = 0

            # Reorder and fill missing
            pivot_df = pivot_df.fillna(0)
            pivot_df = pivot_df[["Year", "State"] + expected_columns]

            global_df = pivot_df

        # Display table (Source column no longer exists)
        data_html = global_df.to_html(index=False)

        return render(
            request,
            "index2.html",
            {"table": data_html, "columns": global_df.columns},
        )

    except Exception as e:
        return render(request, "index2.html", {"error": str(e)})


def model(request):
    global global_df
    try:
        if global_df is None or global_df.empty:
            # Load the Excel file
            data = pd.read_excel(
                r"capestoneapp/Generation_Metatable_Data_1740834320048.xlsx"
            )

            # Remove rows where 'Source' is NaN
            data = data.dropna(subset=["Source"])

            # Pivot the DataFrame to rearrange columns
            pivot_df = data.pivot(
                index=["Year", "State"], columns="Source", values="Generation (In MU)"
            ).reset_index()

            # Ensure all expected columns are present
            expected_columns = [
                "oil-gas",
                "hydro",
                "small-hydro",
                "solar",
                "nuclear",
                "wind",
                "coal",
                "bio-power",
            ]
            for col in expected_columns:
                if col not in pivot_df.columns:
                    pivot_df[col] = 0

            # Reorder and fill missing
            pivot_df = pivot_df.fillna(0)
            pivot_df = pivot_df[["Year", "State"] + expected_columns]

            global_df = pivot_df
        df = global_df.copy()
        df["Year"] = df["Year"].str[:4].astype(int)  # e.g., 2015-16 -> 2015

        # Step 3: Encode 'State'
        le = LabelEncoder()
        df["State_Code"] = le.fit_transform(df["State"])

        # Step 4: Features and targets
        features = ["Year", "State_Code"]
        targets = [
            "oil-gas",
            "hydro",
            "small-hydro",
            "solar",
            "nuclear",
            "wind",
            "coal",
            "bio-power",
        ]

        X = df[features]
        y = df[targets]

        # Step 5: Train-Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Step 6: Train model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Step 7: Predict for 2024-25 (Year = 2024)
        states = df["State"].unique()
        future_data = pd.DataFrame({"Year": [2025] * len(states), "State": states})

        future_data["State_Code"] = le.transform(future_data["State"])

        X_future = future_data[["Year", "State_Code"]]
        predictions_2024 = model.predict(X_future)

        # Step 8: Combine predictions with state names
        result_2024 = pd.DataFrame(predictions_2024, columns=targets)
        result_2024["State"] = future_data["State"]
        result_2024["Year"] = 2025

        result_html = result_2024.to_html(index=False)

        return render(
            request,
            "index2.html",
            {"table": result_html, "columns": result_2024.columns},
        )

    except Exception as e:
        return render(request, "index2.html", {"error": str(e)})


def contactus(request):
    return render(request, "contactus.html")
