import mysqldb
import pandas as pd

def store_image(filename):

    img = open(filename, "rb")
    tablename = "image_table"
    query = "INSERT INTO " + tablename + "(uuid, content\
             , uploadedby, uploadeddat) VALUES (%d, %s, '%s', '%s')"

    param = (row['uuid'], img, row['uploadedby'], row['uploadedat'])

    #TODO - connect to mysqldb and push in the image content in blob
    conn = mysqldb.connect("localhost", "root", "yoyo")
    cur = 

    return

