import requests

base_api_url = "http://www.thecocktaildb.com/api/json/v1/1/list.php?i="
cocktailID = "11000"
api_url = base_api_url + cocktailID
print(api_url)
response = requests.post(api_url)
print(response.json())