from app.guest import guest
from flask import render_template, flash, redirect, session, g, request, url_for, abort

@guest.route('/')
def show():
    import hashlib
    text = hashlib.md5("yoyo").hexdigest()
    return render_template("temp.html", homeclass="active", temptext=text)
