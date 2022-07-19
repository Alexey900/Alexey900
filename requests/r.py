import requests
import os
value = "cat"  # DEFINE!!!!!!!

path = "https://developers.lingvolive.com/api/v1.1/authenticate"
if not os.path.exists("api_token.txt"):
    with open("APIkey.txt", "r") as file:
        headers = {"Authorization ": "Basic " + file.read()}
        result = requests.post(url=path, headers=headers)
        print(result.status_code)
        print(result.json)
        file = open("api_token.txt", "w+")
        file.write(result.text)

minicard_path = "https://developers.lingvolive.com/api/v1/Minicard"
params = {"text": value, "srcLang": 1033, "dstLang": 1049}
try:
    token = open("api_token.txt", "r")
    headers = {"Authorization ": "Bearer " + token.read()}
    result = requests.get(minicard_path, params=params, headers=headers)
    with open("output.txt", "w+") as output:
        output.write(result.json())

except FileNotFoundError as error:
    print("can't open file ", error)

finally:
    token.close()
