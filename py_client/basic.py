import requests

endpoint = "http://localhost:8000/api/"

get_response = requests.get(endpoint, json={"query": "Hi Kacper"})
print(get_response.text)

# print(f"\n\n\n")

print(get_response.json())


