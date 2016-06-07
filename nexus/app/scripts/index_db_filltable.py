import shlex,subprocess

def fill_table(path):
    ##Assuming entities.csv is in current folder
    cmd = '''mysqlimport --ignore-lines=1 \
            --fields-terminated-by=; --fields-enclosed-by=\\" --columns='uuid,name,labels,aliases,keywords' \
            --local -u nexus -h 10.237.27.67 -p power_nexus '''+path

    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output

if __name__ == '__main__':
    import sys
    if(len(sys.argv)<2):
        print 'Usage: python index_db_filltable.py /home/Desktop/entities.csv'
        sys.exit(1)
    path = sys.argv[1]
    fill_table(path)