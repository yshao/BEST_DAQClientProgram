import ConfigParser

class IniParser(ConfigParser.ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d

if __name__ == '__main__':
    parser = IniParser()
    parser.read('test.ini')
    print parser.as_dict()