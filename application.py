from flask import Flask, redirect, url_for, render_template, request, session
import pickle

app = Flask(__name__)
app.secret_key = "hello"

Channels = []
Users = []

class User:
    def __init__(self, name, channel):
        self.name = name
        self.channel = channel

class Message:
    def __init__(self, author, message):
        self.author = author
        self.message = message

class Channel:
    def __init__(self, index, name):
        self.index = index
        self.name = name
        self.messages = []
        self.users = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def add_user(self, user: User):
        self.users.append(user)

Channel1 = Channel(index=0,name="First Channel")
Channels.append(Channel1)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["username"]
        for user in Users:
            if user in Users:
                return render_template("error.html", message="A user with that username is already logged in :(")
        session["user"] = user
        new_user = User(name=user,channel=Channel1)
        Users.append(new_user)
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")
    
@app.route("/user")
def user():
    if "user" in session:
        username = session["user"]
        return f"<h1>{username}</h1>"
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        if user in Users:
            Users.remove(user)
            session.pop("user", None)
            return redirect(url_for("login"))
        else:
            session.pop("user", None)
            return redirect(url_for("login"))
    else:
            return render_template("error.html", message="You are not logged in :(")
        


@app.route("/channels", methods={"GET"})
def channels_view():
    if session.get("user"):
        user = session["user"]
        return render_template("channels.html", channels=Channels, user=user)
    return render_template("error.html", message="You are not logged in :(")

@app.route("/channel")
def channel():
    if session.get("user"):
        user = session["user"]
        u_channel = session["channel"]
        return render_template("channel.html", channel=Channels[u_channel], user=user , prev_user="None")
    else:
        return render_template("error.html", message="You are not logged in :(")

@app.route("/create_channel")
def create_channel():
    if request.method == "GET":
        return render_template("create_channel.html")
    if channel_name in Channels:
        return render_template("error.html", message="A channel with taht username is already created")
    channel_name = request.form.get("channel_name")
    channel_index= len(Channels)
    new_channel = Channel(index=channel_index, name=channel_name)
    Channels.append(new_channel)
    return render_template("channel.html", channel= channels)


if __name__ == "__main__":
	app.run(debug=True)