from flask import Flask, request, redirect, session, render_template_string

app = Flask(__name__)
app.secret_key = "manny_secret_key"

# ✅ Your login details
USER_PHONE = "254728308602"
USER_PASSWORD = "2425"

# 🔥 LOGIN PAGE (clean, centered)
login_page = """
<!DOCTYPE html>
<html>
<head>
<title>Login</title>
<style>
body {
    background: #111;
    color: white;
    font-family: Arial;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
.container {
    width: 90%;
    max-width: 400px;
}
input {
    width: 100%;
    padding: 15px;
    margin: 10px 0;
    font-size: 16px;
    border: none;
    border-radius: 5px;
}
button {
    width: 100%;
    padding: 15px;
    background: red;
    color: white;
    border: none;
    font-size: 18px;
    border-radius: 5px;
}
h2 {
    text-align: center;
}
</style>
</head>
<body>
<div class="container">
<h2>Login</h2>
<form method="POST">
<input type="text" name="phone" placeholder="Phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">LOGIN</button>
</form>
<p style="color:red; text-align:center;">{{ error }}</p>
</div>
</body>
</html>
"""

# 🔥 DASHBOARD (only after login)
dashboard_page = """
<!DOCTYPE html>
<html>
<head>
<title>Dashboard</title>
<style>
body {
    background: black;
    color: white;
    font-family: Arial;
    text-align: center;
    padding-top: 50px;
}
a {
    color: red;
    text-decoration: none;
    font-size: 18px;
}
</style>
</head>
<body>
<h1>Welcome to MannyTrader</h1>
<p>No trades yet</p>
<br>
<a href="/logout">Logout</a>
</body>
</html>
"""

# 🔥 LOGIN ROUTE
@app.route("/", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        phone = request.form["phone"]
        password = request.form["password"]

        if phone == USER_PHONE and password == USER_PASSWORD:
            session["logged_in"] = True
            return redirect("/dashboard")
        else:
            error = "Invalid login"

    return render_template_string(login_page, error=error)

# 🔥 DASHBOARD ROUTE (PROTECTED)
@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/")
    return render_template_string(dashboard_page)

# 🔥 LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# 🔥 RUN APP
if __name__ == "__main__":
    app.run()
