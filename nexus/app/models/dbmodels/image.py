'''
Read image from file. store it to mysql db and retrieve from it
'''

class image:

    def __init__(self, content=None, id=None, uuid=None,
            uploadedby=None, uploadedat=None):

        self.content = content
        self.uuid = uuid
        self.uploadedby = uploadedby
        self.uploadedat = uploadedat
        return

    def push_image(self, uuid, uploadedby=None, uploadedat=None):

        #TODO - connect to mysql

        #TODO push the image / insert

        #TODO - return numrows
        return

    def getSelfFromDB(self):
        #TODO - get from mysqldb by uuid
        query = "SELECT (uuid, content, uploadedby, uploadedat)\
                FROM images_table WHERE uuid=%d" % self.uuid

        print query
        try:
            cursor = self.dbwrap.connect()
            cursor.execute(query)
            rows = cursor.fetchall()

            assert(len(rows) == 1)
            for r in rows:
                self.uuid = r[0]
                self.content = r[1]
                self.uploadedby = r[2]
                self.uploadedat = r[3]
        except Exception as e:
            import traceback
            print traceback.format_exc()
            print repr(e)

        self.dbwrap.commitAndClose()

        #TODO - return object
        return self

    @classmethod
    def getImgUUid(cls, uuid):
        img = image(uuid=uuid)
        return img.getSelfFromDB()
