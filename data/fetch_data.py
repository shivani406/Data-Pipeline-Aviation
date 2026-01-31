import pandas as pd
import requests 

url = "https://opensky-network.org/api/states/all"

europe_box = {
    "lamin": 34.5,
    "lomin": -10.0,
    "lamax": 60.0,
    "lomax": 30.0
}
response = requests.get(url , params=europe_box)
response.raise_for_status()

json_data = response.json()

print(response)
print(response.status_code)
print(json_data)

states = json_data.get("states")

columns = [

"icao24", "callsign", "origin_country", "time_position",
"last contact", "longitude", "latitude", "baro altitude",
"on ground", "velocity", "true track", "vertical_rate",
"sensors", "geo altitude", "squawk", "spi", "position_ source" ] 

# df = pd.DataFrame(states, columns=columns)
# df.drop_duplicates(inplace=True)
# df.dropna(how='all', inplace=True)