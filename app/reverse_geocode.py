import requests

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((39.7240255,-105.1947462))
print(type(reverse_geocode_result))
print(type(reverse_geocode_result[0]))
for k, v in reverse_geocode_result[0].items():
    print(k)
print(reverse_geocode_result[0]['formatted_address'])    

