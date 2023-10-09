import requests
import plivo
from time import sleep
import os
from dotenv import load_dotenv
load_dotenv()

AUTH_ID = os.getenv("AUTH_ID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
CRICKET_API_KEY = os.getenv("CRICKET_API_KEY")

def get_live_match_id():
    try:
        url = "https://livescore6.p.rapidapi.com/matches/v2/list-live"

        querystring = {"Category": "cricket"}

        headers = {
            "X-RapidAPI-Key": CRICKET_API_KEY,
            "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            if len(response.json()["Stages"]) != 0:
                Eid = response.json()["Stages"][0]["Events"][0]["Eid"]
                return Eid
            else:
                print("No Live Match running.")
                return 0
        else:
            print(f"API request failed, {response.json()}")
            return -1
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return -1
    
def get_live_match_status():
    try:
        Eid = get_live_match_id()
        if Eid == 0 or Eid == -1:
            return [Eid]

        url = "https://livescore6.p.rapidapi.com/matches/v2/get-scoreboard"

        querystring = {"Eid": Eid, "Category": "cricket"}

        headers = {
            "X-RapidAPI-Key": CRICKET_API_KEY,
            "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            details = response.json()
            name = details["Stg"]["Snm"]
            T1 = details["T1"][0]["Nm"]
            T2 = details["T2"][0]["Nm"]
            status = details["ECo"]
            return [1,name,T1,T2,status]
        else:
            print(f"API request failed with status code {response.json()}")
            return -1
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return -1
    
def send_sms(numbers):
    match_details = get_live_match_status()
    if match_details[0] == 0:
        print("No Live Match Running.")
        msg = "No Live Match Running."
        # return None
    elif match_details[0] == -1:
        print("Unable to fetch match details.")
        msg = "Unable to fetch match details."
        # return None
    else:
        msg = match_details[1] + "\n" + match_details[2] + " vs " + match_details[3] + "\n" + match_details[4]

    client = plivo.RestClient(AUTH_ID,AUTH_TOKEN)
    # response = client.numbers.search(country_iso='GB')
    # response = client.numbers.buy(number='441603364363')

    for num in numbers:
        response = client.messages.create(
            src='441603364363',
            dst=num,
            text=msg
            )
        print(response)

def check_phoneno(number):
    try:
        client = plivo.RestClient(AUTH_ID,AUTH_TOKEN)
        response = client.calls.create(
        from_='441603364363',
        to_=number,
        answer_url='https://s3.amazonaws.com/static.plivo.com/answer.xml',
        answer_method='GET')
        print(response)
    except:
        print(response)

    sleep(10)
    
    url = 'https://api.plivo.com/v1/Account/{auth_id}/Call/'.format(auth_id=AUTH_ID)

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.get(url, headers=headers, auth=(AUTH_ID, AUTH_TOKEN))

    objects = response.json()["objects"]
    valid = 0

    for obj in objects:
        if obj["to_number"] == number:
            if obj["hangup_cause_code"] == 4010:
                valid = 1
                break

    return valid

if __name__ == "__main__":
    print()