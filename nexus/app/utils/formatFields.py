''' Contains routines for formatting strings to a particular type'''
import re


def formatName(name):
    """ name - in last name, first name fmt
        output - name in first_name last_name
    """

    # - split name by ','
    name_list = [x.strip().lower() for x in name.split(',')]
    # join the string - first element is last if ',' exists
    # name types assumed - title FN LN or LN, title FN

    if len(name_list) > 1:
        mod_name = ' '.join(name_list[1:] + [name_list[0]])
    else: mod_name = ' '.join(name_list)

    # remove all dots from name and salutations
    mod_name = re.sub(r'\.', '', mod_name)
    salutations = ['mr', 'srimati', 'sreemati', 'shrimati', 'shreemati',
                   'shriman', 'mrs', 'ms', 'shri', 'shree', 'dr', 'lt',
                   'capt',  'smt', 'late']

    # instead of re.sub we can use word in string to check above words
    #salutations = '|'.join(salutations)
    # mod_name = re.sub(r'(\b' + salutations + r'\b)', '',
    #                  mod_name, flags=re.IGNORECASE)

    #This one is better!
    mod_name = ' '.join([x for x in mod_name.split() if x not in salutations])

    return mod_name.strip()

def getTimeStampLong(datestr, fmt=None):
    #TODO - form datetime obj using str
    from datetime import datetime
    from time import mktime

    if fmt is None:
        dtobj = datetime.strptime(datestr, "%d %b %Y")
    else:
        try:
            dtobj = datetime.strptime(datestr, fmt)
        except ValueError as e:
            print repr(e)
            try:
                dtobj = datetime.strptime(datestr, "%d %b %Y")
            except:
                return "000.000"

    #TODO - get UTC time stamp from the object
    return mktime(dtobj.timetuple())


if __name__ == "__main__":
    print formatName('Adhalrao Patil,Shri Shivaji')
    print formatName('Adhikari,Shri Deepak (Dev)')
    print formatName('Shrimati Kalpakam Yechury')
    print formatName('Shri Amartya Chaudhuri')
    print getTimeStampLong('05 Jun 1972')
    print getTimeStampLong('15 Jul 1972')

