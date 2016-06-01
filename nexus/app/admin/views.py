from app.admin import admin
from flask import render_template, flash, redirect, session, g, request, url_for, abort

@admin.route('/')
def show():
    return render_template("admin_home.html", homeclass="active")

@admin.route('/deleteallsolr/')
def deleteallsolr():
    print 'inside delete'
    from app.solr.SolrIndex import delete_index
    temptext = delete_index()
    flash(temptext)
    print 'should have been done'
    return render_template("admin_home.html", homeclass="active")

@admin.route('/fullimportsolr/')
def fullimportsolr():
    from app.solr.SolrIndex import full_import
    temptext = full_import()
    flash(temptext)
    return render_template("admin_home.html", homeclass="active")


