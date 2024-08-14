"""
Script that makes a new json file with only the courses that have a timetable available.
"""

import pandas as pd
from loguru import logger

input_json_file = 'courses.json'
output_json_file = 'cleaned_courses.json'

# Load the combined JSON file
df = pd.read_json(input_json_file)

# Drop rows where 'timetable' is "Not Available"
df_clean = df[df["timetable"] != "Not Available"]

# Save the cleaned DataFrame back to JSON
df_clean.to_json(
    output_json_file, 
    orient='records', 
    force_ascii=False, 
    indent=4
)

print(f"Cleaned data saved to {output_json_file}")
print(f"number of rows before cleaning: {df.shape[0]}")
print(f"number of rows after cleaning: {df_clean.shape[0]}")