def transform(df):
    print("Initiating transformation process . . .")

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")   # cleans column names

    df = df.drop_duplicates()   # get rid of duplicate rows
    df = df.dropna()   # delete missing values

    print("Transformation complete!")
    return df