import openai
import os
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up OpenAI API key
openai.api_key = "YOU-API-KEY"

def generate_query(prompt, table_structure):
    # Use the user's prompt and table structure to generate a query
    query_prompt = f"Write a query that will fulfill the user's request of {prompt} using the table structure {table_structure}"
    query = openai.Completion.create(
        engine="text-davinci-002", prompt=query_prompt, temperature=0.4, max_tokens=500)
    return query['choices'][0]['text']

# Set up API credentials
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

while True:
    source = input("Would you like to use a Google Sheet or a local file as your data source? (Sheet/File)")
    if source == "Sheet":
        sheet_name = input("Please enter the URL of the Google Sheet: ")
        sheet_name_2 = input("Please enter the sheet name:")
        wb = client.open_by_url(sheet_name)
        sheet = wb.worksheet(sheet_name_2)
        original_df = sheet.get_all_values()
        data = pd.DataFrame(original_df[1:], columns=original_df[0])
        break
    elif source == "File":
        file_path = input("Please enter the file path: ")
        data = pd.read_csv(file_path, low_memory=False)
        break
    else:
        print("Invalid option. Please enter 'Sheet' or 'File'.")

while data is not None:
    # Get the user's prompt
    prompt = input("Ask away, what do you want to know?")
    # Generate the query
    query = generate_query(prompt, data.dtypes.to_string())
    print(query)

