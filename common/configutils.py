import xmltodict

# ### test ###
# with open('config.xml') as fd:
#     doc = xmltodict.parse(fd.read())
#
# print doc['mydocument']['and']['many'] # == [u'elements', u'more elements']
# print doc['mydocument']['and']['many'] # == [u'elements', u'more elements']
# print doc['mydocument']['plus']['@a'] # == u'complex'
# print doc['mydocument']['plus']['#text'] # == u'element as well'

class Config(object):
    def __init__(self,file):
        ""
        self._configFile=file
        self.read(self._configFile)


    def get(self,key):
        ""
        return self._map[key]

    def put(self,key,val):
        ""
        self._map[key]=val

    def read(self,path_file):
        ""
        self._map=dict(xmltodict.parse(open(self._configFile,'r').read())['config'])

    def save(self,path_file):
        ""

        open(self._configFile,'w').write(xmltodict.unparse(self._map,pretty=True))

    def count(self):
        print self._map

        return len(self._map)

    def read_ip(self):
        ""
        d={}
        for key, value in my_dict.iteritems():   # iter on both keys and values
            if key.startswith('IP'):
                d[key]=value

        return d


    def get_map(self):
        ""
        return self._map


if __name__ == '__main__':

    config = Config('config.xml')
    print config.count()

    my_dict=config.get_map()

    print config.read_ip()