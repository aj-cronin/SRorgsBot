import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from pullmodmail import get_new_confs

DOCUMENT_ID = open("current_id.txt","r").readlines()[0]            # CHANGE TO ID OF WHATEVER CURRENT DOC IS

def push_to_doc():
    CLIENT_FILE = "google_secret_key.json"                                  # GET YOUR OWN SECRET KEY FROM GOOGLE CLOUD
    SCOPES = ["https://www.googleapis.com/auth/documents"]
    REDDIT_NAMES = {"u/Royal130": "Daniel",
                    "u/Easymoney810": "Evan",
                    "u/eviepie123": "Eve",
                    "u/Hirowxo": "Jairo",
                    "u/Left_Past3736": "Kanlu",
                    "u/Little_Carob_951": "Leo",
                    "u/Embarrassed-Win3642": "N-Dawg",
                    "u/NekoluChan": "Nyx",
                    "u/TocantinsDub": "Troy",
                    "u/Mean_Ad_1252": "T-Dog",
                    "u/thegoat129420": "Cire",
                    "u/FRONKO1234123231": "Francessca",
                    "u/Future-Combination88": "Nate",
                    "U/lord_angel_dust": "Tod",
                    "u/xsopan": "Susan",
                    "u/rjred": "RJ",
                    "u/ThingsLikeThat67": "AJ"}

    TRIBES =        {"u/Royal130": "Jury",
                    "u/Easymoney810": "Kamieskroon",
                    "u/eviepie123": "Kamieskroon",
                    "u/Hirowxo": "Jury",
                    "u/Left_Past3736": "Jury",
                    "u/Little_Carob_951": "Jury",
                    "u/Embarrassed-Win3642": "Jury",
                    "u/NekoluChan": "Jury",
                    "u/TocantinsDub": "Jury",
                    "u/Mean_Ad_1252": "Jury",
                    "u/thegoat129420": "Kalbaskop",
                    "u/FRONKO1234123231": "Kalbaskop",
                    "u/Future-Combination88": "Kalbaskop",
                    "U/lord_angel_dust": "Kalbaskop",
                    "u/xsopan": "Kalbaskop",
                    "u/rjred": "Tafelberg",
                    "u/ThingsLikeThat67": "Hosts"}

    COLORS =        {"Kamieskroon": {'red':255 / 255,'green':94 / 255,'blue':187 / 255},
                    "Tafelberg": {'red':254 / 255,'green':110 / 255,'blue':2 / 255},
                    "Kalbaskop": {'red':255 / 255,'green':245 / 255,'blue':2 / 255},
                    "Jury": {'red':219 / 255,'green':66 / 255,'blue':199 / 255},
                    "Hosts": {'red':45 / 255,'green':118 / 255,'blue':197 / 255}
                    }

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("docs", "v1", credentials=creds)
        document = service.documents().get(documentId = DOCUMENT_ID).execute()

        new_confs = get_new_confs()
        num_of_confs = len(new_confs)
        if num_of_confs == 0:
            print("No New Confessionals!")
            return "There are no new confessionals at this time."
        for date, conf in new_confs.items():
            for unam, text in conf.items():
                if TRIBES["u/"+unam] != "Jury":
                    document = service.documents().get(documentId = DOCUMENT_ID).execute()

                    
                    end_index = document["body"]["content"][-3]["endIndex"]

                    requests = [
                                {
                                    'insertTable': {
                                        'rows': 1,
                                        'columns': 1,
                                        'location': {
                                            "index": end_index - 1
                                        }
                                    }
                                }
                    ]

                    result = service.documents().batchUpdate(
                    documentId=DOCUMENT_ID, body={'requests': requests}).execute()


                    document = service.documents().get(documentId = DOCUMENT_ID).execute()
                    prev_table = document["body"]["content"][-4]["startIndex"]
                    requests = [
                                {  'updateTableCellStyle': {
                                        'tableCellStyle': {
                                            'backgroundColor': {
                                                'color': {
                                                    'rgbColor': COLORS[TRIBES["u/"+unam]]
                                                }
                                            }
                                        },
                                        "fields": '*',
                                        'tableStartLocation': {
                                                    "index": prev_table
                                                }
                                        }
                                },
                                {
                                'insertText': {
                                    'location': {
                                        'index': prev_table + 3 
                                    },
                                    'text': text + "\n\n" + f"        -      {REDDIT_NAMES['u/'+ unam]} ({TRIBES['u/' + unam]})"
                                }
                                }
                    ]
                    result = service.documents().batchUpdate(
                    documentId=DOCUMENT_ID, body={'requests': requests}).execute()

                    document = service.documents().get(documentId = DOCUMENT_ID).execute()
                    prev_table_end = document["body"]["content"][-4]["endIndex"]
                    requests = [
                                {   "updateTextStyle": {
                                        "textStyle": {
                                            "weightedFontFamily": {
                                                "fontFamily": "Oswald"
                                            } 
                                        },
                                        "fields": "weightedFontFamily", 
                                        "range": {
                                            "startIndex": prev_table_end - 36,
                                            "endIndex": prev_table_end - 1
                                        }
                                }
                                }
                                ]
                                

                    result = service.documents().batchUpdate(
                    documentId=DOCUMENT_ID, body={'requests': requests}).execute()
        
        print("Updating Document Done!")
        if num_of_confs == 1:
            return f"Successfully updated document with 1 new confessional."
        
        return f"Successfully updated document with {num_of_confs} new confessionals."

        
    except HttpError as err:
        print(err)

def update_id(new_id_str):
    new_id = open("current_id.txt", "w")
    new_id.write(new_id_str)
    new_id.close()