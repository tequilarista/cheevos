import json

'''
TODO:

Have good working base class to extend for different bug tracking systems.

Local tasks:
    * read and write template files
    * define required sub-class method imlementations

'''

# the spirit of Ryan Burns' code reviews haunts me.  Must have named exceptions!
class CheevosError(Exception):
    pass

class CheevosBase():
    '''
    Cheevos base class -- many things here should be overridden by a sub-class
    '''
    def __init__(self):
        self.cheevosTemplate = { 'bug_system': {
                                    'type': "",
                                    'server_URL': "",
                                    'REST_query': "",
                                    'username': "",
                                    'password': "",
                                    },
                                'trophies': {
                                    'num_trophies': None,
                                    'trophy_1': "", 
                                    'trophy_2': "", 
                                    'trophy_3': "", 
                                    },
                                'content_system': {
                                    'type': "",
                                    'server_URL': "", 
                                    'username': "",
                                    'password': "",
                                    }
                               } 
        self.verbose = False

    def validateJSON(self):
        '''
        In the future, maybe do something more thorough, but in the 
        meantime at least make sure we have a non-empty struct
        '''
        if len(self.cheevosTemplate.keys()) == 0:
            raise CheevosError("JSON template appears to be empty")

    def loadTemplate(self, tmplName):
        #raise NotImplementedError
        '''
        Reads a saved template in order to construct a connection to a bug system
        '''
        try:
            fh = open(tmplName, 'r')
            res = json.loads(fh.read())
            fh.close()
        except IOError, e:
           print "Unable to load %s" % tmplName
           raise

        return res

    def writeTemplate(self, type, tmplName):
        '''
        Creates a template json file that can be filled in and then used to 
        create cheevos results.
        '''
        self.cheevosTemplate['bug_system']['type'] = type
        fh = open(tmplName, "w+")
        dump = json.dumps(self.cheevosTemplate, indent=4, sort_keys=True)
        fh.write(dump)
        fh.close()

    def runQuery(self):
        raise NotImplementedError

    def writeResults(self):
        raise NotImplementedError

    def raiseError(self,msg,exception=None):
        errorMsg = "%s\n" % msg
        if exception:
            errorMsg += "\nException:\n---------\n %s\n---------" % exception
        raise CheevosError(errorMsg)

