

conflict




if (type(orig[prop]) is list):
                if (type(naya[prop]) is list):
                    if prop in MVPLIST:
                        
                        from ast import literal_eval
                        tosave = literal_eval(request.form[prop])


                        origcopy = utils.copyListOfStrings(orig[prop])
                        nayacopy = utils.copyListOfStrings(naya[prop])


                        for val in tosave:
                            
                            ##Other idea could have been to do it like aliases, but not doing that
                            ##also check here if the val already exists or not, add to alias otherwise
                            ##Keep it simple
                            if val.strip() not in orig[prop]:
                                orig[prop].append(val)


                        flash(prop+' appended : '+str(tosave))
                        continue
                    else:
                        return "prop "+str(prop)+" not in mvplist! Nothing pushed. Will be reported to admin.", 400
                else:
                    return "new property "+prop+" should have been a list. Nothing added", 400
            elif (type(naya[prop]) is list):
                return "new property "+prop+" should NOT have been a list. Nothing added", 400

                ##assuming both are list type only when in conflict
            #     import json
            #     print type(request.form[prop])
            #     print request.form[prop]
            #     #json.loads?
            #     from ast import literal_eval
            #     tosave = literal_eval(request.form[prop])

            ##there are two ways to determine if the prop is a list
            ##or the one we want to work on
            ## 1.
            # if (type(orig[prop]) is list) or (type(naya[prop]) is list):
            ## or look for mvps in constants file
            ## 2.
            # from constants import MVPLIST




new


 ##code basically checks if the prop is new for this node
                ##and is a valid list, then we will add it as a list
                ##TODO:test for phones
                ##TODO: api validation MVPLIST no singluar always a list
                if type(naya[prop]) is list:
                    if prop in MVPLIST:
                        from ast import literal_eval
                        tosave = literal_eval(request.form[prop])
                    else:
                        return "prop "+str(prop)+" not in mvplist! Nothing pushed. Will be reported to admin.", 400
                        ##TODO: report to admin