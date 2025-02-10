import requests
import ast
import freecurrencyapi

def convert():
    client = freecurrencyapi.Client('fca_live_lNvhPRSZ6CKfTPB5Va8WVFLfFlQHGEbv2XGXr84p')

    # izprintēt jaunākās vērtības (pret 1 dollāru)
    # result = client.latest()
    # print(result)

    # api statuss
    print(client.status())

    # informācija par valūtām
    # result = client.currencies(currencies=['EUR', 'CAD'])
    # print(result)
convert()

def test():
    client = freecurrencyapi.Client('fca_live_lNvhPRSZ6CKfTPB5Va8WVFLfFlQHGEbv2XGXr84p')
    result = client.latest(base_currency='EUR')
    print(result)

test()