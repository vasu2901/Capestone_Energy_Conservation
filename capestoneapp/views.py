import pandas as pd
from django.shortcuts import render


def read_data(request):
    try:
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

        # Ensure all expected columns are present, fill missing ones with 0
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

        # Reorder columns
        pivot_df = pivot_df[["Year", "State"] + expected_columns]

        pivot_df = pivot_df.fillna(0)

        pivot_df = pivot_df[
            [
                "oil-gas",
                "hydro",
                "small-hydro",
                "solar",
                "nuclear",
                "wind",
                "coal",
                "bio-power",
                "Year",
                "State",
            ]
        ]

        # Convert the transformed DataFrame to HTML for display
        data_html = pivot_df.to_html(index=False)

        return render(
            request,
            "index.html",
            {"table": data_html, "columns": pivot_df.columns},
        )

    except Exception as e:
        return render(request, "index.html", {"error": str(e)})


# Let me know if you’d like me to add file upload handling, API responses, or anything else! 🚀
