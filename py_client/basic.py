import requests

# endpoint = "https://httpbin.org/"
# endpoint = "https://httpbin.org/anything"
endpoint = "http://localhost:8000/"

get_response = requests.get(endpoint, json={'query': 'Hello'})
print(get_response.text)

