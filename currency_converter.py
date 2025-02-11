import freecurrencyapi
from flask import Flask, render_template, request, redirect
from datetime import datetime
import re
import requests

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route("/")
def index():
    return render_template("index.html")

class Api():
    def __init__(self):
        self.admin = freecurrencyapi.Client('fca_live_lNvhPRSZ6CKfTPB5Va8WVFLfFlQHGEbv2XGXr84p')
        self.result = None
        self.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def get_currency_data(self):
        result = self.admin.latest(base_currency=input("Enter currency: "))
        print(result)

a = Api()
a.get_currency_data()

if __name__ == '__main__':
    app.run(debug=True)