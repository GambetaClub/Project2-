from flask import Flask, redirect, url_for, render_template, request, session
import pickle

app = Flask(__name__)
app.secret_key = "hello"

Channels = []
Users = []

Channels.append("Channel 1")


@app.route("/")
def home():
	return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form.get("username")
        if user in Users:
            return render_template("error.html", message="A user with that username is already logged in :(")
        session["user"] = user
        Users.append(user)
        pickle.dump(user, open( "save.p", "wb" ))
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
    else:
        channel_name = request.form.get("channel_name")
        if channel_name in Channels:
            return render_template("error.html", message="A channel with that name is already created")
        Channels.append(channel_name)
        return render_template("channel.html", channel=channel_name)


if __name__ == "__main__":
	app.run(debug=True)