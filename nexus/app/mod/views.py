from app.mod import mod
from flask import render_template, flash, redirect, session, g, request, url_for, abort

@mod.route('/')
def show():
    return render_template("temp.html", homeclass="active", temptext='moderator')
