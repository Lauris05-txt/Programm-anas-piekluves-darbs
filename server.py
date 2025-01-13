from flask import Flask, render_template, redirect, url_for
import currency_converter as conv

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    value = conv.convert('GBP', 'AUD', 5000)
    return render_template('index.html', value=value)

if __name__ == "__main__": 
    app.run(debug=True)

