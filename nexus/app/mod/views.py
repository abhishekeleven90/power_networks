from app.mod import mod
from flask import render_template, flash, redirect, session, g, request, url_for, abort

@mod.route('/')
def show():
    val = request.args.get('some',None)
    flash(val)
    return render_template("mod_home.html")

##adding code here so that user work doesnt clutter
##but move this to user at the onset!
@mod.route('/trial/')
def trial():
    ##user gives certain data we have changed object let's say
    from app.models.graphmodels.graph_handle import GraphHandle
    from app.utils.commonutils import Utils
    from app.constants import CRAWL_TASKID, CRAWL_PUSHDATE, CRAWL_PUSHEDBY, CRAWL_TASKTYPE
    from app.constants import CRAWL_SOURCEURL, CRAWL_FETCHDATE, CRAWL_EN_ID_NAME, RESOLVEDWITHUUID
    from app.constants import CRAWL_NODENUMBER, CRAWL_EN_ID_FORMAT

    gg = GraphHandle()
    node = gg.getOriginalCoreObject('node',77)
    copynode = gg.coredb.copyNode(node)

    ##TODO: copy the labels that is imp
    ##get uuid that is imp
    ##do your changes as you get from the html form, then push them to crawldb
    ##with the changes that we have done here
    ##TODO:
    # think if you need to use the api push? we need to save the task id too! seems overkill.

    copynode['uuid'] = None ##remove for now
    copynode[RESOLVEDWITHUUID] = 77
    copynode[CRAWL_PUSHEDBY] = 'abhi10@gmail.com'
    copynode[CRAWL_PUSHDATE] = Utils.currentTimeStamp()
    #XXX: for user ownerid = session['userid'] and iscrawled = 0, get the unique row
    ##that's our taskid
    copynode[CRAWL_TASKID] = 3
    copynode[CRAWL_SOURCEURL] = "http://wikipedia.com/NaveenJindal/"
    copynode[CRAWL_FETCHDATE] = copynode[CRAWL_PUSHDATE]-4000000
    copynode[CRAWL_TASKTYPE] = "wiki"
    copynode['job'] = "just farmer"
    #copynode.labels.add('personOfTheYear')
    copynode[CRAWL_NODENUMBER] = 1 ##though idiotic
    copynode[CRAWL_EN_ID_NAME] = CRAWL_EN_ID_FORMAT %(copynode[CRAWL_TASKID], copynode[CRAWL_NODENUMBER])

    #flash(str(node))
    flash(copynode)

    gg.crawldb.graph.create(copynode)
    copycopynode = gg.getCrawlObjectByID('node',CRAWL_EN_ID_NAME,copynode[CRAWL_EN_ID_NAME],True)
    flash(copycopynode)


    ##TODO: same things for relations
    return render_template("temp.html", temptext='trial completed')

## follows the same structure as in verifier work
@mod.route('/pickobject/<string:kind>/')
def pickobject(kind):

    from app.models.graphmodels.graph_handle import GraphHandle
    from app.constants import CRAWL_EN_ID_NAME, RESOLVEDWITHUUID

    gg = GraphHandle()

    CRAWL_ID_NAME, CURR_ID = gg.getTwoVars(kind)

    session.pop(CRAWL_ID_NAME, None)
    session.pop(CURR_ID, None)
    session.pop('kind', None)

    nodecount = gg.crawldb.getResolvedButNotModeratedNodeCount()

    node = None
    if nodecount!=0:
        node = gg.nextNodeToModerate(session['userid'])
        print 'hereeeeeeeee'
    if node is None:
        ##TODO: pass redirect or something
        abort(404)
        pass



    session[CRAWL_ID_NAME] = node[CRAWL_EN_ID_NAME]

    session[CURR_ID] = node[RESOLVEDWITHUUID]
    session['kind'] = kind

    print 'sessionnnnnnnnnn'
    print session[CRAWL_ID_NAME],  session[CURR_ID],  session['kind']


    return redirect(url_for('verifier.diffPushGen', kind=kind))
