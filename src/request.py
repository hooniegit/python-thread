import requests
from configparser import ConfigParser
import requests

parser = ConfigParser()
parser.read('/home/hooniegit/git/personal/python-thread-pool/config/config.ini')
client_id = parser.get("SPOTIFY", "client_id")
client_sc = parser.get("SPOTIFY", "client_sc")

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}
data = f'grant_type=client_credentials&client_id={client_id}&client_secret={client_sc}'.encode()
response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data).json()
token = response['access_token']

date_gte = "2023-08-25"
movie_name = "oppenheimer"


query = f"{movie_name}"
headers = {
    'Authorization': f'Bearer {token}',
}
params = {
    'q' : query,
    'type': 'album',
    'limit' : "3"
}
response = requests.get('https://api.spotify.com/v1/search', params=params, headers=headers).json()

print(response)