from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import utilities

converter = utilities.Api()
app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route("/", methods = ["GET", "POST"])
def index():
    output_sum = ""
    converter_error = ""
    if request.method == "POST":
        try:
            input_currency = request.form.get("input_currency")
            output_currency = request.form.get("output_currency")
            input_sum = request.form.get("input_sum")
            output_conversion = converter.convert_currency(input_currency, output_currency)
            output_sum = float(output_conversion) * float(input_sum)

            db = utilities.Database()
            db.insert_conversion_history("1", input_sum, input_currency, output_sum, output_currency, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S"))
        
        except KeyError as e:
            converter_error = f"KeyError: {e}"
        except ValueError as e:
            converter_error = f"ValueError: {e}"
        except Exception as e:
            converter_error = f"Error: {e}"
    return render_template("index.html", output_sum=output_sum, converter_error=converter_error)

@app.route("/history", methods = ["GET"])
def history():
    db = utilities.Database()
    history = db.get_histrory()
    print(history == [])
    if history == []:
        return render_template("history.html", history = (("", "", "", "", "", "", "")))
    else:
        return render_template("history.html", history = history)

@app.route("/api/delete_history", methods = ["POST", "GET"])
def delete_history():
    db = utilities.Database()
    history = db.delete_history()
    return render_template("history.html", history = history)

@app.route("/home", methods = ["GET"])
def home():
    return render_template("home.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    db = utilities.Database()
    db.user_data(username, email, password)
    return render_template('signup.html')
    
if __name__ == '__main__':
    app.run(debug=True)
