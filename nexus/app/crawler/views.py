from app.crawler import crawler
from flask import render_template, flash, redirect, session, g, request, url_for, abort
from app.forms import EditEntityForm, form_error_helper

@crawler.route('/')
def show():
    return render_template("crawler_home.html", homeclass="active", temptext='crawler')