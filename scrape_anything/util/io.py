import pandas as pd
import os


def to_text_file(text, filename):
    import datetime

    with open(filename, "a") as file:
        file.write(
            "\nExecution Time: "
            + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            + "\n"
        )
        file.write("-----\n")
        file.write(text)


def dataframe_to_csv(df, csv_filename):
    _df = df.copy()
    _df = stringable_dataframe_to_csv(_df)
    _df.to_csv(csv_filename, index=False)


def dataframe_from_csv(csv_filename):
    if not os.path.exists(csv_filename):
        raise Exception(f"implementation error file {csv_filename} wasn't found.")

    df = pd.read_csv(csv_filename)
    return dataframe_to_stringable(df)


def dataframe_to_stringable(df):
    for column in df.columns:
        if hasattr(df[column], "str"):
            df[column] = (
                df[column].str.replace("<comma>", ",").str.replace("<new_line>", "\n")
            )
    return df


def stringable_dataframe_to_csv(df):
    for column in df.columns:
        if hasattr(df[column], "str"):
            df[column] = (
                df[column].str.replace(",", "<comma>").str.replace("\n", "<new_line>")
            )
    return df


def pickle(data, filename):
    import pickle

    # Pickle the dictionary and save it to a file
    with open(filename, "wb") as file:
        pickle.dump(data, file)


def unpickle(file_name):
    import pickle

    with open(file_name, "rb") as file:
        return pickle.load(file)
