from app.verifier import verifier
from flask import render_template, flash, redirect, session, g, request, url_for, abort

@verifier.route('/')
def show():
    return render_template("temp.html", homeclass="active", temptext='verifier')

@verifier.route('/diff/')
def diff():
    import app.graphdb as t

    ##keep info about not shoiwng labels and not showing props 
    orig = t.orig() ##from the graph
    naya = t.node3() ##from the row
    
    new_labels = t.labelsToBeAdded(orig,naya)    
    conf_props,new_props = t.propsDiff(orig,naya)


    return render_template("verifier_diff.html", homeclass="active",
        new_labels=new_labels,conf_props=conf_props, new_props=new_props,orig=orig, naya=naya)

## TODO: this can be better!
@verifier.route('/match/')
def match():
    ##TODO: this should actaully change acc to the resolve props and show the diffs acc, to the resolve things only!
    import app.graphdb as t
    row = t.node1()
    graphnodes = [t.orig(),t.node2(),t.node3()]
    return render_template("verifier_match.html", homeclass="active",
        row=row,graphnodes=graphnodes)

@verifier.route('/temp/')
def temp():
    temptext = "Hi"
    return render_template("temp.html", homeclass="active",temptext=temptext)    