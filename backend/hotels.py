import requests

url = 'https://api.makcorps.com/citysearch/{cityname}/{page}/{currency}/{num_of_rooms}/{num_of_adults}/{check_in_date}/{check_out_date}'
api_key = 'YOUR-API-KEY'

url = url.format(
    cityname='London',
    page='0',
    currency='USD',
    num_of_rooms='1',
    num_of_adults='3',
    check_in_date='2023-10-03',
    check_out_date='2023-10-04'
)

url_with_api_key = f"{url}?api_key={api_key}"

response = requests.get(url_with_api_key)

# Print the response
print(response.json())