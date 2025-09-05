import requests

endpoint = "https://httpbin.org/anything"

get_response = requests.get(endpoint, json={"query": "Hi Kacper"})
print(get_response.json())

get_response = requests.get(endpoint, data={"data": "Hi Agata"})
print(get_response.json())




# Notes #
# HTTP Request -handles-> HTML
# REST API HTTP Request -handles-> JSON
# JSON (JavaScript Object Nototion) -similar-to-> Python Dict