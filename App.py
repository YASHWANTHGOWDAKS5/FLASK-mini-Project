from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="bus@1234",
        database="busbooking"
    )

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        if user == "yashu gowda" and password == "12345":
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return "Invalid Admin Credentials"
    return render_template("admin_login.html")

@app.route("/admin/dashboard", methods=["GET", "POST"])
def admin_dashboard():
    if "admin" not in session:
        return redirect(url_for("admin"))
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == "POST":
        name = request.form["name"]
        source = request.form["source"]
        destination = request.form["destination"]
        seats = 20
        cur.execute("INSERT INTO buses (name, source, destination, seats) VALUES (%s,%s,%s,%s)",
                    (name, source, destination, seats))
        conn.commit()
    cur.execute("SELECT * FROM buses")
    buses = cur.fetchall()
    conn.close()
    return render_template("admin_dashboard.html", buses=buses)

@app.route("/passenger", methods=["GET", "POST"])
def passenger():
    if request.method == "POST":
        passenger = request.form["passenger"]
        session["passenger"] = passenger
        return redirect(url_for("book_bus"))
    return render_template("passenger_login.html")

@app.route("/passenger/book", methods=["GET", "POST"])
def book_bus():
    if "passenger" not in session:
        return redirect(url_for("passenger"))
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == "POST":
        bus_id = request.form["bus_id"]
        cur.execute("SELECT seats FROM buses WHERE id=%s", (bus_id,))
        seats = cur.fetchone()[0]
        if seats > 0:
            cur.execute("INSERT INTO bookings (bus_id, passenger) VALUES (%s,%s)",
                        (bus_id, session["passenger"]))
            cur.execute("UPDATE buses SET seats=seats-1 WHERE id=%s", (bus_id,))
            conn.commit()
        else:
            return "No seats available"
    cur.execute("SELECT * FROM buses")
    buses = cur.fetchall()
    conn.close()
    return render_template("book_bus.html", buses=buses, passenger=session["passenger"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
