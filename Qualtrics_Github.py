# -*- coding: utf-8 -*-

    
import io
import zipfile
import requests

def download_qualtrics(api_token, data_center, survey_id, output_path, file_format="csv"):
    base_url = f"https://{data_center}.qualtrics.com/API/v3/surveys/{survey_id}/export-responses/"
    headers = {
        "content-type": "application/json",
        "X-API-TOKEN": api_token,
    }
    data = {"format": file_format, 
            "useLabels":True, #use this if you want text responses instead of numeric code values; the default is False.
            "timeZone": "America/New_York"}
    
    response = requests.post(base_url, headers=headers, json=data)
    if response.status_code != 200:
        print("POST request failed with status code:", response.status_code)
        return
    print(f"POST request {survey_id} successful!")
    
    progress_id = response.json()["result"]["progressId"]
    
    percent_complete = 0
    fileId = 0
    done = False
    
    request_url = base_url + progress_id
    while not done:
        request_response = requests.get(request_url, headers=headers)
        percent_complete = request_response.json()["result"]["percentComplete"]
        if percent_complete == 100:
            done = True
            fileId = request_response.json()["result"]["fileId"]
            print("Export complete!")
    
            
    request_download_url = f"{base_url}/{fileId}/file"
    request_download = requests.get(request_download_url, headers=headers, stream=True)
    zipfile.ZipFile(io.BytesIO(request_download.content)).extractall(output_path)
    print('Downloaded Qualtrics survey data to', output_path)

if __name__ == "__main__":
    api_token = "" #put your API token inside the quotation mark.
    data_center = '' #put your organizationID.datacenter inside the quotation mark.
    survey_ids = ["ID1", "ID2", "ID3", 
                  "ID4", "ID5", "ID6"]
    output_path = "/Users/Desktop/Yourfolder"
    for survey_id in survey_ids:
        download_qualtrics(api_token, data_center, survey_id, output_path)
