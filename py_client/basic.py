import requests

endpoint = "http://localhost:8000/api/"


get_response = requests.post(endpoint, json={"title": "Hello world"})
print(get_response.text)
# print(get_response.json())


# ## first lessons
# get_response = requests.get(endpoint, json={"product_id": 123})
# # print(get_response.text)

# # print(f"\n\n\n")

# print(get_response.json())


