from flask import jsonify

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

        if 'aliases' in props:
            if type(props['aliases']) is not list:
                return False, 'aliases'

        if 'bidirectional' in props: ##for the validations in wiki form
            val = props['bidirectional']
            if val!="True" and val!="False":
                return False, 'bidirectional'

        return True, 'success'

    def error_helper(self, message,statuscode):
        return jsonify({'error':message}), statuscode

    def internalPropsConverter(self, props):

        if 'startdate' in props:
            props['startdate'] = long(props['startdate'])

        if 'enddate' in props:
            props['enddate'] = long(props['enddate'])

        if 'iscurrent' in props:
            val = (props['iscurrent'])
            if val=='True':
                props['iscurrent'] = True
            else:
                props['iscurrent'] = False

        return props
