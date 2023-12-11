from flask import Flask, render_template, request  # Import Flask library.
from flask_limiter import Limiter,util
import weather_report_functions  # Import python functions from weather_report_functions
import chatbot      # Import python functions from chatbot

# Creates the Flask instance
app = Flask(__name__)

# Set travel itinerary array, order corresponds to combo box on index.html
itinerary = open("Itinerary.txt").read().splitlines()

# Sets max endpoint requests to 999 per day
limiter = Limiter(app=app, key_func=util.get_remote_address, default_limits=["999 per day"], storage_uri="memory://")

# Home page display, default window
@app.route("/", methods=["POST", "GET"])
def home():
    # Checks if submit button has been pressed if item value is within the array range (default selection is not)
    if request.method == "POST" and int(request.form["city"]) <= len(itinerary):
        # Uses selected item from combo box for weather report function arguement location
        overview = weather_report_functions.display_report_overview(itinerary[int(request.form["city"])])
        temp = weather_report_functions.display_report_temp(itinerary[int(request.form["city"])])
        report_future = weather_report_functions.display_report_future(itinerary[int(request.form["city"])])
        iframe_link = weather_report_functions.replace_text(itinerary[int(request.form["city"])], " ", "%20")

        # Updates current page and passes the weather report results and iframe link as keyword arguements for html code
        return render_template("index.html", content=overview, content2=temp, content3=report_future, link=iframe_link)

    # Checks if submit button has been pressed and if anything has been written in the textbox
    elif request.method == "POST" and request.form["chatbot"] != "":
        #checks if user typed a location
        if chatbot.chatbot_location(request.form["chatbot"]) is not None:

            overview = weather_report_functions.display_report_overview(chatbot.chatbot_location(request.form["chatbot"]))
            temp = weather_report_functions.display_report_temp(chatbot.chatbot_location(request.form["chatbot"]))
            report_future = weather_report_functions.display_report_future(chatbot.chatbot_location(request.form["chatbot"]))
            iframe_link = weather_report_functions.replace_text((chatbot.chatbot_location(request.form["chatbot"])), " ", "%20")
            chatbot_response = chatbot.chatbot(request.form["chatbot"])
            # Updates current page and passes the weather report results and iframe link as keyword arguements for html code
            return render_template("index.html", content=overview, content2=temp, content3=report_future, chatbot=chatbot_response, link=iframe_link)
        else:
            chatbot_response = chatbot.chatbot(request.form["chatbot"])
            return render_template("index.html", content="No location selected", chatbot=chatbot_response)
    else:
        # Default view of no location selected
        return render_template("index.html", content="No location selected")


# Login form display
# EXAMPLE ONLY - Out of scope
@app.route("/login", methods=["POST", "GET"])
@limiter.exempt     # This endpoint has no rate limit
def login():
    # Checks if form submitted + username/password=admin
    if request.method == "POST" and (request.form["userName"] and request.form["userPassword"]) == "admin":
        # Displays default homepage
        return render_template("index.html", content="No location selected")
    else:
        # Clears username and password to reset page
        return render_template("login.html")


# Runs app
if __name__ == '__main__':
    app.run()
