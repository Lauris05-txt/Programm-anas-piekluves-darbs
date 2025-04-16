from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import utilities
import re

converter = utilities.Api()
app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route("/home", methods = ["GET", "POST"])
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
    return render_template("home.html", output_sum=output_sum, converter_error=converter_error)

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

@app.route("/", methods = ["GET"])
def home():
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    reg_err = []
    no_err = []
    no_err_count = 0
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_check = request.form.get('password_check')

                
        if email:
            a = re.match(r"^\S+@\S+\.\S+$", email)
            if a:
                no_err_count += 1
            else:
                reg_err.append("Neatbilstoša epasta adrese")
        if password == password_check:
            no_err_count += 1
        else:
            reg_err.append("Paroles nesakrīt")

        if no_err_count == 2:
            no_err.append("Reģistrācija veiksmīga!")
        else:
            print("kaut kas nogāja greizi")

        db = utilities.Database()
        db.user_data(username, email, password)
    
    print(reg_err)

    return render_template('signup.html', reg_err = reg_err, no_err = no_err)
    
@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            db = utilities.Database()
            is_user_valid = db.login(username, password)
            
            if is_user_valid:
                pass
                print("pieslēgšanās veiksmīga")
                print(is_user_valid)
                return redirect(url_for('index'))
                
            return render_template("login.html", is_user_valid = is_user_valid)



    else:
        return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)
