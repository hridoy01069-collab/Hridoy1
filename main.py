from flask import Flask, request, redirect, session, render_template_string
import sqlite3, os
app = Flask(__name__)
app.secret_key = "workbd_123"
def init_db():
    conn = sqlite3.connect('workbd.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, balance REAL DEFAULT 0)')
    conn.commit()
    conn.close()
init_db()
PAGE = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>WorkBD Pro</title><style>
body{background:#0f0f0f;color:white;font-family:Arial;margin:0}
.header{background:#1a1a1a;padding:15px;text-align:center;border-bottom:2px solid #a855f7}
.balance{background:linear-gradient(90deg,#a855f7,#ec4899);padding:20px;border-radius:15px;margin:15px;text-align:center}
.job{background:#1e1e1e;margin:15px;border-radius:15px;padding:20px;border:1px solid #333}
.btn{background:#22c55e;color:white;padding:12px;border:none;border-radius:8px;width:100%;font-weight:bold}
input{width:90%;padding:12px;margin:8px;border-radius:8px;border:none}
</style></head><body>
<div class="header"><h1 style="color:#a855f7">💼 WorkBD Pro</h1>{% if 'user' in session %} Hi, {{session['user']}} | <a href="/logout" style="color:red">Logout</a>{% endif %}</div>
{% if 'user' not in session %}
<div style="text-align:center;padding:30px"><h2>Login / Register</h2><form method="post" action="/login"><input name="username" placeholder="Username" required><br><input name="password" type="password" placeholder="Password" required><br><button class="btn">Login / Register</button></form><p style="color:#888">প্রথমবার Username দিলে Account খুলবে!</p></div>
{% else %}
<div class="balance"><h2>ব্যালেন্স: ${{ "%.2f"|format(balance) }}</h2><p>User: {{session['user']}}</p></div>
<div class="job"><h3>📱 YouTube Subscribe - $0.50</h3><form method="post" action="/task"><input type="hidden" name="amount" value="0.5"><button class="btn">✅ কাজ করেছি - $0.50 যোগ হবে</button></form></div>
<div class="job"><h3>📸 Instagram Follow - $0.30</h3><form method="post" action="/task"><input type="hidden" name="amount" value="0.3"><button class="btn">✅ কাজ করেছি</button></form></div>
<div class="job"><h3>🌐 Website Visit - $0.20</h3><form method="post" action="/task"><input type="hidden" name="amount" value="0.2"><button class="btn">✅ ভিজিট করেছি</button></form></div>
<div class="job" style="background:#a855f7;text-align:center"><h3>💸 Withdraw</h3><p>Min $10</p><form method="post" action="/withdraw"><input name="number" placeholder="Bkash Number" required><button class="btn" style="background:white;color:#a855f7">Withdraw Request</button></form></div>
{% endif %}</body></html>
"""
@app.route("/")
def home():
    bal=0
    if 'user' in session:
        conn=sqlite3.connect('workbd.db');c=conn.cursor();c.execute("SELECT balance FROM users WHERE username=?",(session['user'],));r=c.fetchone();bal=r[0] if r else 0;conn.close()
    return render_template_string(PAGE,balance=bal)
@app.route("/login",methods=["POST"])
def login():
    u=request.form['username'];p=request.form['password'];conn=sqlite3.connect('workbd.db');c=conn.cursor();c.execute("SELECT * FROM users WHERE username=?",(u,));user=c.fetchone()
    if user:
        if user[2]!=p:return "Wrong Password <a href='/'>Back</a>"
    else:c.execute("INSERT INTO users (username,password,balance) VALUES (?,?,0)",(u,p));conn.commit()
    session['user']=u;conn.close();return redirect("/")
@app.route("/task",methods=["POST"])
def task():
    if 'user' not in session:return redirect("/")
    amt=float(request.form['amount']);conn=sqlite3.connect('workbd.db');c=conn.cursor();c.execute("UPDATE users SET balance=balance+? WHERE username=?",(amt,session['user']));conn.commit();conn.close();return redirect("/")
@app.route("/withdraw",methods=["POST"])
def wd():return "<h1 style='text-align:center;margin-top:50px'>✅ Withdraw Request Sent to Admin Hridoy!<br><br><a href='/'>Back</a></h1>"
@app.route("/logout")
def lo():session.clear();return redirect("/")
@app.route("/admin")
def admin():
    conn=sqlite3.connect('workbd.db');c=conn.cursor();c.execute("SELECT username,balance FROM users");users=c.fetchall();conn.close();return "<h1>Admin - Users: "+str(len(users))+"</h1>"+"<br>".join([f"{x[0]} - ${x[1]}" for x in users])
if __name__=="__main__":app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
