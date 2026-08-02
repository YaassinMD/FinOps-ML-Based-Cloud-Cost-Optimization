import pandas as pd

def preprocess_input(input_df, feature_columns):

    input_df = pd.get_dummies(input_df)

    input_df = input_df.reindex(
        columns=feature_columns,
        fill_value=0
    )

    return input_df