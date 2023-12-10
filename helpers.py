import requests

from flask import redirect, render_template, session
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


'''
request from exercisedb a number of random exercises
number of exercises and body part/equipment/target muscle can be selected
https://rapidapi.com/justin-WFnsXH_t6/api/exercisedb
docs: https://v2.exercisedb.io/docs/static/index.html#/
'''
def get_exercise(filter, filter_options, limit):

    # {filter} can be = ['bodyPart', 'equipment', 'target']
    # {filter_options} are each of the filter's options
    url = f"https://exercisedb.p.rapidapi.com/exercises/{filter}/{filter_options}"

    # set number of generated exercises
    querystring = {"limit": limit}

    headers = {
        "X-RapidAPI-Key": "5a40bac1bdmsh394e0f4e58b629bp19dc43jsnb0c4bc61d0e7",
        "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


'''
api request from Mega Fitness Calculator
https://rapidapi.com/bejjaothmane/api/mega-fitness-calculator1/
'''
def get_bmi(weight, height):

    url = "https://mega-fitness-calculator1.p.rapidapi.com/bmi"

    querystring = {"weight": weight, "height": height}

    headers = {
        "X-RapidAPI-Key": "5a40bac1bdmsh394e0f4e58b629bp19dc43jsnb0c4bc61d0e7",
        "X-RapidAPI-Host": "mega-fitness-calculator1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()
