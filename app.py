import sqlite3,string,random,os
from datetime import datetime
from flask import Flask,render_template,request,redirect,url_for


app=Flask(__name__)

def get_db():
    return sqlite3.connect("data/data.db")

def date_time():
    now = datetime.now()
    formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    return formatted

def get_id(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def add_conf(c):
    conn=get_db()
    cursor=conn.cursor()
    idd=get_id()
    cursor.execute("SELECT id FROM confessions")
    ids=cursor.fetchall()
    ids=tuple(x[0] for x in ids)
    while idd in ids:
        idd=get_id()
    cursor.execute("SELECT id FROM confessions")
    cursor.execute("INSERT INTO confessions (id,context,time) VALUES (?, ?, ?)",(idd,c,date_time()))
    conn.commit()
    conn.close()
    return 0

def read():
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM confessions")
    data=cursor.fetchall()
    conn.close()
    return data

def delete(idd:string):
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("SELECT id FROM confessions")
    ids=cursor.fetchall()
    ids=tuple(x[0] for x in ids)
    if idd in ids:
        cursor.execute("DELETE FROM confessions WHERE id = ?", (str(idd),))
        conn.commit()
        conn.close()
        return 0
    else:
        conn.close()
        return 1

@app.route("/", methods=["GET","POST"])
def home():
    data=read()
    if request.method=="POST":
        context=request.form.get("secret")
        add_conf(context)
        data=read()
        return redirect(url_for("home"))

    return render_template("main.html",data=data)

@app.route("/admin",methods=["GET","POST"])
def admin():
    login=False
    data=None
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        if username=="IDEA" and password=="IDEACLUB@2025":
            login=True
            data=read()
        elif "delete-conf" in request.form:
            conf_id=request.form.get("conf-delete")
            print(delete(str(conf_id)))
            data=read()
            return render_template("admin.html",login=True,confs=data)

    return render_template("admin.html",login=login,confs=data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
