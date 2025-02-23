import freecurrencyapi
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import re
import requests

class Api():
    def __init__(self):
        self.admin = freecurrencyapi.Client('fca_live_lNvhPRSZ6CKfTPB5Va8WVFLfFlQHGEbv2XGXr84p')
        self.result = None
        self.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def get_currency_data(self, currency):
        result = self.admin.latest(base_currency=currency)
        return result

    def convert_currency(self, input_currency, output_currency):
        response = self.get_currency_data(input_currency)
        return response["data"][output_currency]

converter = Api()
# a.get_currency_data()
app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route("/", methods = ["GET", "POST"])
def index():
    output_sum = ""
    if request.method == "POST":
        input_currency = request.form.get("input_currency")
        output_currency = request.form.get("output_currency")
        input_sum = request.form.get("input_sum")
        
        output_conversion = converter.convert_currency(input_currency, output_currency)
        output_sum = float(output_conversion) * float(input_sum)

    print(output_sum)
    return render_template("index.html", output_sum=output_sum)
    
if __name__ == '__main__':
    app.run(debug=True)