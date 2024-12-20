def get_new_confs():
    from datetime import datetime, timezone

    time_file = open("last_time.txt", "r")
    date_format = "%Y-%m-%dT%H:%M:%S"
    LAST_TIME = datetime.strptime(time_file.readlines()[0], date_format)
    time_file.close()
    CLIENT_ID = 'kNsK4r3-G9HT5OBs_mOuIw'                          # GET OWN CLIENT KEY FROM REDDIT DEV PORTAL
    SECRET_KEY = 'kTU-kOQ5ciNLJ7vsgS7xMadfhpAPdQ'                         # GET OWN SECRET KEY FROM REDDIT DEV PORTAL

    import requests
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

    data = {
        'grant_type': 'password',
        'username': '',                     # ENTER REDDIT USERNAME HERE
        'password': ''                      # ENTER REDDIT PASSWORD HERE
    }

    headers = {'User-Agent': "ConfessionalBot/0.0.1"}

    res = requests.post('https://www.reddit.com/api/v1/access_token', 
                        auth = auth, data = data, headers = headers)

    TOKEN = res.json()['access_token']

    headers['Authorization'] = f'bearer {TOKEN}'

    res = requests.get('https://oauth.reddit.com/api/mod/conversations',
                    headers = headers)

    conversations = res.json()['conversations']
    conf_list = dict()
    for message in conversations:
        new_conf = {}
        res = requests.get(f'https://oauth.reddit.com/api/mod/conversations/{message}',
                    headers = headers)
        curr_msg = res.json()
        curr_id = list(curr_msg.get("messages").keys())[0]
        new_conf[curr_msg["conversation"]["participant"]["name"]] = curr_msg["messages"][curr_id]["bodyMarkdown"]

        conf_date = curr_msg["messages"][curr_id]["date"][0:19]
        date_obj = datetime.strptime(conf_date, date_format)
        date_obj
        if(date_obj > LAST_TIME and curr_msg["conversation"]["owner"]["displayName"] == "survivorredditorgs"):
            conf_list[date_obj] = new_conf


    conf_list = dict(sorted(conf_list.items()))

    # for date, conf in conf_list.items():
    #     curr_conf = conf_list.get(date)
    #     print(date)
    #     for unam, text in curr_conf.items():
    #         text_preview = text
    #         print(f'{unam}: {text_preview}')
    #     print()

    time_string = datetime.now(timezone.utc).strftime(date_format)
    new_time = open("last_time.txt", "w")
    new_time.write(time_string)
    new_time.close()
    
    print("Pulling from Modmail Done!")

    return conf_list



    

    