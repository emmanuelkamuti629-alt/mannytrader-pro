from flask import Flask, render_template_string, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = "manny_secret_key"

USER_EMAIL = "emmanuelkamuti629@gmail.com"
USER_PASSWORD = "1234"

known_devices = {}
otp_store = {}

EXCHANGES = ["Binance", "KuCoin", "MEXC", "Gate.io"]
active_exchange = "Binance"
bot_running = False

def send_email_alert(msg):
    print("EMAIL ALERT:", msg)

def layout(content):
    return f"""
    <html><head><title>MannyTrader Pro</title></head>
    <body style="background:black;color:white;font-family:Arial;">
    <h2 style="color:#00ff7f;">MannyTrader Pro</h2>
    <a href="/dashboard">Dashboard</a> |
    <a href="/exchanges">Exchanges</a> |
    <a href="/logout">Logout</a>
    <hr>
    {content}
    </body></html>
    """

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email == USER_EMAIL and password == USER_PASSWORD:
            device = request.headers.get("User-Agent")

            if email not in known_devices:
                known_devices[email] = []

            if device not in known_devices[email]:
                known_devices[email].append(device)
                send_email_alert(f"New login: {device}")

            session["user"] = email
            return redirect("/dashboard")

        return layout("<h3>❌ Invalid login</h3>")

    return layout("""
    <h3>Login</h3>
    <form method="post">
    <input name="email" placeholder="Email"><br>
    <input name="password" type="password" placeholder="Password"><br>
    <button>Login</button>
    </form>
    <a href="/forgot">Forgot Password?</a>
    """)

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    balance = round(random.uniform(100, 500),2)
    status = "🟢 Running" if bot_running else "🔴 Stopped"

    return layout(f"""
    <h3>Dashboard</h3>
    <p>Exchange: {active_exchange}</p>
    <p>Balance: ${balance}</p>
    <p>Status: {status}</p>

    <form method="post" action="/toggle">
    <button>{'Stop Bot' if bot_running else 'Start Bot'}</button>
    </form>
    """)

@app.route("/toggle", methods=["POST"])
def toggle():
    global bot_running
    bot_running = not bot_running
    return redirect("/dashboard")

@app.route("/exchanges", methods=["GET","POST"])
def exchanges():
    global active_exchange

    if request.method == "POST":
        active_exchange = request.form["ex"]

    buttons = ""
    for ex in EXCHANGES:
        buttons += f"""
        <form method="post">
        <button name="ex" value="{ex}">{ex}</button>
        </form>
        """

    return layout(f"<h3>Exchanges</h3>{buttons}<p>Active: {active_exchange}</p>")

@app.route("/forgot", methods=["GET","POST"])
def forgot():
    if request.method == "POST":
        email = request.form["email"]
        otp = str(random.randint(100000,999999))
        otp_store[email] = otp

        return layout(f"""
        <h3>OTP: {otp}</h3>
        <form method="post" action="/reset">
        <input name="email" value="{email}">
        <input name="otp" placeholder="OTP">
        <input name="new_password" placeholder="New Password">
        <button>Reset</button>
        </form>
        """)

    return layout("""
    <h3>Forgot Password</h3>
    <form method="post">
    <input name="email" placeholder="Email">
    <button>Send OTP</button>
    </form>
    """)

@app.route("/reset", methods=["POST"])
def reset():
    global USER_PASSWORD

    email = request.form["email"]
    otp = request.form["otp"]
    new_password = request.form["new_password"]

    if otp_store.get(email) == otp:
        USER_PASSWORD = new_password
        return layout("<h3>✅ Password reset</h3>")
    else:
        return layout("<h3>❌ Invalid OTP</h3>")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run()
