import pandas as pd

def extract(file_path):
    df = pd.read_csv(file_path)
    print("The data has been extracted successfully . . .")
    return df