from app.guest import guest
from flask import render_template, flash, redirect, session, g, request, url_for, abort
from app.solr.SolrIndex import *

@guest.route('/')
def show():
    import hashlib
    text = hashlib.md5("yoyo").hexdigest()
    return render_template("temp.html", homeclass="active", temptext=text)

@guest.route('/temp2/')
def temp2():
    from app.models.dbmodels.index_entities import Entity
    print 'should work fine'
    #Entity.del_all_entities()
    #en = Entity(4, 'Kapil', 'person,politician', 'Kapil, Thakkar', 'gujrat iit mumbai')
    #rows = en.insertEntity()
    #en.name = 'Amartya'
    #en.updateEntity()
    en2= Entity()
    en2.getEntity(4)
    print 'will be here if all fine'
    return render_template("temp.html", homeclass="active", temptext ='You are here '+en2.name+' '+en2.labels)

@guest.route('/temp3/')
def temp3():
    from app.utils.locprocess import getCityState
    (city,state) = getCityState('pondicherry')
    return render_template("temp.html", homeclass="active", temptext=city+' '+state)

@guest.route('/viz/')
def viz():
    ##get cypher from request.args['cypher']

    ## use constant variables

    ##cypher variable is the one having query
    ##task 1 validate if query is read query - at start assume the query is valid

    ##### any validation function can be moved to graphdb.py later to see if the query is read or not.
    ##### use cypher card  : http://neo4j.com/docs/cypher-refcard/current/
    #####  CREATE, MERGE, DELETE, REMOVE, SET, INDEX, LOAD, LOAD CSV, CONSTRAINT, any case
    ##### nodes return, mandatory

    ##task 2 fecth the results of the query
    ##task 3 show on viz.html or something

    ##to decide: post or not?
    cypher = 'MATCH (n)-[r]->(m) RETURN n,r,m LIMIT 50'
    return render_template("viz.html", homeclass="active", temptext=cypher)

@guest.route('/temp4/')
def solr():
    delete_index()
    full_import()
    print 'will be here if all fine'
    return render_template("temp.html", homeclass="active", temptext = 'You are here')
