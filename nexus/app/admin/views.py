from app.admin import admin
from flask import render_template, flash, redirect, session, g, request, url_for, abort

@admin.route('/')
def show():
    return render_template("temp.html", homeclass="active", temptext='admin')
