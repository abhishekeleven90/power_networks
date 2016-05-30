import diff_match_patch

class SideBySideDiff(diff_match_patch.diff_match_patch):

    def old_content(self, diffs):
        """
        Returns HTML representation of 'deletions'
        """
        html = []
        for (flag, data) in diffs:
            text = (data.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace("\n", "<br>"))

            if flag == self.DIFF_DELETE:
                html.append("""<del style=\"background:#ffb3b3;
                    \">%s</del>""" % text)
            elif flag == self.DIFF_EQUAL:
                html.append("<span>%s</span>" % text)
        return "".join(html)

    def new_content(self, diffs):
        """
        Returns HTML representation of 'insertions'
        """
        html = []
        for (flag, data) in diffs:
            text = (data.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace("\n", "<br>"))
            if flag == self.DIFF_INSERT:
                html.append("""<ins style=\"background:#b3ffb3;
                    \">%s</ins>""" % text)
            elif flag == self.DIFF_EQUAL:
                html.append("<span>%s</span>" % text)
        return "".join(html)



def diffObjects(str1,str2):
    diff_obj = SideBySideDiff()
    result = diff_obj.diff_main(str1, str2)
    diff_obj.diff_cleanupSemantic(result)
    oldstr = diff_obj.old_content(result) 
    newstr = diff_obj.new_content(result)
    # ll = []
    # ll.append(oldstr)
    # ll.append(newstr)
    return oldstr,newstr



