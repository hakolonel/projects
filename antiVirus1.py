import os
import requests
import time

url = "https://www.virustotal.com/api/v3/files"
api_key = "f3ceb980d547001e492b513923d90d977a1f89dd590e9658843bd11e4ef394d8"
headers = {
    "accept": "application/json",
    "x-apikey": api_key
    }

def scan_directory(path):
    if(os.path.isdir(path)):
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            print(item)
            if os.path.isdir(full_path):
                scan_directory(full_path)
            else:
                print("Scanning file: " + item)
                get_scan_analysis(full_path)
    else:
        print("scanning file: " + path)
        get_scan_analysis(path)
def get_scan_analysis(analysis):

    with open(analysis, "rb") as file:
        files = {"file": (os.path.basename(analysis), file)}
        response = requests.post(url, headers=headers, files = files)
        if response.status_code == 200:
            analysis_id = response.json()["data"]["id"]
            is_virus = scan_report(analysis_id)
            if is_virus:
                print("file is a virus")
            elif is_virus == False:
                print("file is clean")
            else:
                print("an error has occurred while analyzing the file")
        else:
            print("upload failed with status code: " + str(response.status_code))


def scan_report(response):
    analysis_url = f"https://www.virustotal.com/api/v3/analyses/{response}"
    Get_response = requests.get(analysis_url,headers=headers)
    if Get_response.status_code == 200:
        result = Get_response.json()
        status = result["data"]["attributes"]["status"]
        if status in ["queued", "in-progress"]:
            print("file is being analyzed")
            time.sleep(10)
            return scan_report(response)
        else:
            return result["data"]["attributes"]["stats"]["malicious"] > 0

    else:
        print("an error has occurred: "+ str(Get_response.status_code))
        return None



path = r"C:\Users\Gaming PC\Downloads"
scan_directory(path)
