from flask import Flask, render_template, request, redirect, url_for, session, make_response
import jwt
from datetime import datetime, timezone, timedelta
import utilities
import re
from functools import wraps

converter = utilities.Api()
app = Flask(__name__, static_folder='static', template_folder='templates')

SECRET_KEY = "parole"


# Wrapper function for checking if logged in
def check_token(func):
    @wraps(func) # Here so check_token can be used for multiple pages
    def wrapper():
        token = request.cookies.get('jwt_token')

        if not token:
            current_user = (1, 'GUEST', '', '') # if no token found, go with guest account
        else:
            # Check if user_id from token is in database
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            db = utilities.Database()
            current_user = db.get_user_data_by_id(data["user_id"])
        
        return func(current_user)

    return wrapper

@app.route("/", methods = ["GET"])
def index():
    return render_template("index.html")

@app.route("/home", methods = ["GET", "POST"])
@check_token
def home(current_user):
    print("current_user:", current_user)
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
            db.insert_conversion_history(current_user[0], input_sum, input_currency, output_sum, output_currency, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S"))
        
        except KeyError as e:
            converter_error = f"KeyError: {e}"
        except ValueError as e:
            converter_error = f"ValueError: {e}"
        except Exception as e:
            converter_error = f"Error: {e}"
    return render_template("home.html", output_sum=output_sum, converter_error=converter_error)

@app.route("/history", methods = ["GET"])
@check_token
def history(current_user):
    db = utilities.Database()
    history = db.get_histrory(current_user[0])
    print(history == [])
    if history == []:
        return render_template("history.html", history = (("", "", "", "", "", "", "")))
    else: return render_template("history.html", history = history)

@app.route("/api/delete_history", methods = ["POST", "GET"])
@check_token
def delete_history(current_user):
    db = utilities.Database()
    history = db.delete_history(current_user[0])
    return render_template("history.html", history = history)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    err = []
    success_message = []
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_check = request.form.get('password_check')

                
        if email:
            is_email_valid = re.match(r"^\S+@\S+\.\S+$", email)
            if not is_email_valid:
                err.append("Neatbilstoša epasta adrese")
        if password != password_check:
            err.append("Paroles nesakrīt")


        if err:
            print(err)
        else:
            success_message.append("Reģistrācija veiksmīga")
            print(success_message)
            db = utilities.Database()
            db.user_data(username, email, password)
            

        return render_template('signup.html', err = err, success_message = success_message)

    return render_template('signup.html', err = err, success_message = success_message)
    
@app.route('/login', methods = ["POST", "GET"])

def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            db = utilities.Database()
            is_user_valid = db.login(username, password)
            
            if is_user_valid:
                print("pieslēgšanās veiksmīga")
                user = db.get_user_data_by_username(username)
                print("user:", user)
                token = jwt.encode({'user_id': user[0], 'exp': datetime.now(timezone.utc) + timedelta(hours=1)}, 
                               SECRET_KEY, algorithm="HS256")
                response = make_response(redirect(url_for('home')))
                response.set_cookie('jwt_token', token)
                return response 
            else:
                is_user_valid = "Lietotājvārds un/vai parole nav pareiza"

            return render_template("login.html", is_user_valid = is_user_valid)



    else:
        return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)
