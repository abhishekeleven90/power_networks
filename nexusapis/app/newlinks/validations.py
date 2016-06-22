class Validate:

    def __init__(self):
        pass

    def isValidNonMetaProp(self, propname):
        if propname[0]=='_' or propname[-1]=='_':
            return False
        return True

    def checkAllPropnamesValid(self, propvaljson):
        for prop in propvaljson:
            if not self.isValidNonMetaProp(prop):
                return False, prop
        return True, None

    def checkEntityInLabels(self, en):
        '''
            returns msg on how the labels should be:
            entity, person
            entity, organization for now
        '''
        ##you can check if
        ##XXX: organization, person, disjoint and one of them there
        nodelabels = en['labels']
        return 'entity' in nodelabels

    def validateNodeIsEntityOrHyperedge(self, en):
        required_en_labels_disjoint = ['entity','hyperedgenode']
        nodelabels = en['labels']
        count = 0
        for label in required_en_labels_disjoint:
            if label in nodelabels:
                count = count + 1
        return (count == 1)

    def validateUrl(self, url):
        from werkzeug.datastructures import MultiDict
    	from app.forms import URLForm
        urldata = {}
        urldata['url']= url
    	formdata = MultiDict(mapping=urldata)
    	form = URLForm(formdata, csrf_enabled=False)
        return form.validate()

    def checkInternalProps(self, props):
        if 'startdate' in props:
            if not props['startdate'].isdigit():
                return False, 'startdate'

        if 'enddate' in props:
            if not props['enddate'].isdigit():
                return False, 'enddate'

        if 'iscurrent' in props:
            val = props['iscurrent']
            if val!="True" and val!="False":
                return False, 'iscurrent'

        return True, 'success'





    # def isEntityvalid(self, en, nodes):
    #     '''
    #         returns True, success on success
    #         else False, msgs
    #     '''
    #     ##MAJOR TODO reserved keywords and required keywords list
    #     ##MAJOR TODO format and pattern against keywords with regex ??
    #     from app.apiconstants import required_endict_props, reserved_en_props, required_en_props
    #     validate = self
    #
    #     if not validate.checkEntityInLabels(en):
    #         return False, 'a node must have entity as a label'
    #
    #     for prop in required_endict_props:
    #         if not prop in en:
    #             return False, str(prop)+' required attribute missing for an entity'
    #
    #     #print entities[en]
    #     nodeid = en['id']
    #
    #     if not nodeid.isdigit():
    #         return False, 'entity id should be a number'
    #
    #     if nodeid in nodes:
    #         return False, 'id repeated under entities'
    #
    #     if not len(en['labels'])>0:
    #         return False, 'Labels list empty for an entity'
    #
    #     for prop in required_en_props:
    #         if (not prop in en['properties']) : ##patch for allowing hyperedgenode, checked doesnt affect anything else
    #             return False, str(prop)+' required property missing for an entity'
    #
    #     ## ALIASES CODE
    #     # if not len(en['properties']['aliases'])>0:
    #     #     return False,'aliases list empty for an entity'
    #     # ##TODO: how to verify if the name is in aliases?
    #
    #     ## XXX: aliases to be handled as a csv?? ##keep it as it is will add - will have to change code when generating keywords etc.
    #     ## Merge two options for all strings- assume csv seperate - add with "" and then see if lists do not have duplicates append and use
    #     ## aliases not a list many changes, many places! ##or you can just assume a list and assume no prop named aliases
    #
    #     for prop in reserved_en_props:
    #         if prop in en['properties']:
    #             return False, str(prop)+' reserved property not allowed explicitly for an entity'
    #
    #     allPropnamesValid, prop = validate.checkAllPropnamesValid(en['properties'])
    #     if not allPropnamesValid:
    #         return False, str(prop)+' cannot begin or end with underscore'
    #
    #     ## MAJOR todo: determine automatically that the type is a list!!
    #     ## Also push it then like a list - but will have to maintain a list of props that can be list
    #     ## OR MV and check here back!
    #
    #     nodelabels = en['labels']
    #
    #     fetchdate = en['fetchdate']
    #     sourceurl = en['sourceurl']
    #
    #     if not fetchdate.isdigit():
    #         return False,'fetchdate should be a long time since epoch, negative if dates before 1970'
    #
    #     if not validate.validateUrl(sourceurl):
    #         return False,'sourceurl should be valid url for entity'
    #
    #     return True, 'success'
