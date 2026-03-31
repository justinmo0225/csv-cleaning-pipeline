from pipeline.extract import extract
from pipeline.transform import transform
from pipeline.load import load
from visualize import run_visuals

FILE_PATH = "data/messy_employee_dataset.csv"   # MUST match the csv file name in the data folder

df = extract(FILE_PATH) # ETL pipeline -- extract stage

print("Initiating cleaning process . . .")
df_clean = transform(df)    # ETL pipeline -- transform stage

load(df_clean)  # ETL pipeline -- load stage

print("The pipeline is complete!")

# run visualizations
print("The data has been extracted successfully . . .")
print("Initiating cleaning process . . .")
print("Transformation complete!")
run_visuals()