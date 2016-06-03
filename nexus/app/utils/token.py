class NexusToken():

    def __init__():
        '''nothing to do'''
        pass

    def generateApiKey(self, userid):
        '''key generation but the key can be very wllp be same as somebody else's key'''
        '''gives 32 bit token for that user'''
        '''to uniquely identify a call auth would be on user and apikey'''
        import hashlib, random  
        bits = str(random.getrandbits(256))
        bits = bits+userid
        bits = ''.join(random.sample(bits,len(bits)))
        return hashlib.md5( str(random.getrandbits(256)) ).hexdigest()