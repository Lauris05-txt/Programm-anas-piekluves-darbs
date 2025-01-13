import requests
import ast

def convert(have, want, amount):
    api_url = 'https://api.api-ninjas.com/v1/convertcurrency?have={}&want={}&amount={}'.format(have, want, amount)
    response = requests.get(api_url, headers={'X-Api-Key': 'Q2Ct8+B0IYgiFOzRJamJ/A==v2Xnz4KrhaHt9fno'})
    if response.status_code == requests.codes.ok:
        converted_value = ast.literal_eval(response.text)
        return converted_value["new_amount"]
    else:
        print("Error:", response.status_code, response.text)

# convert('GBP', 'AUD', 5000)