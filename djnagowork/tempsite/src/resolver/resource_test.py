import pkg_resources as pr

print pr.resource_exists('src.input','consids.csv')
#this is how we can get file names independently
filename = pr.resource_filename('src.input','consids.csv')
print filename
