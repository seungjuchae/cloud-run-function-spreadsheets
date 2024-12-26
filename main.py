import functions_framework
import pandas as pd
import gspread
from google.oauth2 import service_account
from flask import jsonify 


@functions_framework.http
def hello_http(request):

    request_json = request.get_json(silent=True)
    if request_json and "sheet_id" in request_json:
        sheet_id = request_json["sheet_id"]
    else:
        sheet_id = request.args.get("sheet_id", None)
    if not sheet_id:
        return jsonify({"error": "Sheet ID not provided"}), 400


    # Setting up the credentials and client
    scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = service_account.Credentials.from_service_account_file('service_account.json', scopes=scopes)
    client = gspread.authorize(creds)


    # open the google sheet and select the first sheet
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.get_worksheet(0)

    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    return jsonify(df.to_dict(orient="records"))
