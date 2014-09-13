import json
import re
import sys
import xmlrpclib

from CheevosBase import *

class CheevosConfluence(CheevosBase):
    def __init__(self):
        CheevosBase.__init__(self)
        self.verbose = False

        self.wikiSpace = None
        self.wikiPage = None
        self.username = None
        self.password = None
        self.serverUrl = None
        self.token = None
        self.server = None
        self.numTrophies = None
        self.trophyList = []
        self.trophyPageURL = None

        self.pageHandle = None

        # standard HTML5 vars
        self.Header ="<table><tbody>\n"
        self.Footer ="</tbody></table>\n"
        self.RowStart = "<tr>\n"
        self.RowEnd = "</tr>"
        self.ColStart = "<td align=\"center\"><h1 style=\"text-align: center;\">"
        self.ColEnd = "</p></h1></td>\n"
        self.ColTitleStart = "<th><p>"
        self.ColTitleEnd = "</p></th>\n"
        self.AttachStart = "<ac:image><ri:attachment ri:filename=\""
        self.AttachEnd = "\" /></ac:image>"


    def _beginSession(self):
        '''
        Grab a connection to the appropriate page on the confluence server.
        Takes name of page to update, assumes the STI display space
        '''
        self.server = xmlrpclib.ServerProxy(self.serverUrl)
        self.token = self.server.confluence2.login(self.username, self.password)
        try:
            self.pageHandle = self.server.confluence2.getPage(self.token, self.wikiSpace, self.wikiPage)
        except Exception, e:
            msg = "Unable to get a page handle to specified page: %s\n" % self.trophyPageURL
            self.raiseError(msg,e)
        if self.verbose:
            print self.pageHandle
        else:
            self.pageHandle["content"] = self.Header

    def _storePageToServer(self):
        '''
        Write page buffer back to server
        '''
        try:
            self.server.confluence2.storePage(self.token, self.pageHandle)
        except Exception, e:
            msg = "Unable to write page to confluence server. Check to see if it exists %s" % self.trophyPageURL
            self.raiseError(msg,e)

    def _endSession(self):
        '''
        Everything ends the same way
        '''
        if self.verbose:
            print self.Footer
        else:
            self.pageHandle["content"] += self.Footer
            self._storePageToServer()

    def addConfluenceNodesToTemplate(self, cheevoObj):
        '''
        Add Confluence-required additions to a cheevo template, basically 'space'
        and 'page'
        '''
        cheevoObj.cheevosTemplate['content_system']['space'] = ""
        cheevoObj.cheevosTemplate['content_system']['page'] = ""

    def loadConfluenceInfoFromConfig(self,configData):
        self.wikiSpace = configData['content_system']['space']
        self.username = configData['content_system']['username']
        self.password = configData['content_system']['password']
        self.serverUrl = configData['content_system']['server_URL']
        self.wikiPage = configData['content_system']['page']
        self.numTrophies = configData['trophies']['num_trophies']

        check = 1
        while check <= self.numTrophies:
            trophyFile = 'trophy_%s' % str(check)
            if configData['trophies'].has_key(trophyFile):
                self.trophyList.append(configData['trophies'][trophyFile])
                check += 1
            else:
                self.raiseError("Looks like we're missing a trophy image file?")

        self.trophyPageURL = self.getPageURL(configData)

        if not (self.wikiSpace or self.serverURL or self.username or self.password or self.pageHandle):
            self.raiseError("Missing necessary information from %s template/parameters") 

    def validateTrophyAttachments(self):
        trophyNames = []

        if self.pageHandle == None:
            self._beginSession()

        try:
            fileList = self.server.confluence2.getAttachments(self.token, self.pageHandle['id'])
        except Exception, e:
            msg = "Unable to get a list of attachments from page"
            self.raiseError(msg,e)

        for f in fileList:
            trophyNames.append(f['fileName'])

        for i in self.trophyList:
            if i not in trophyNames:
                self.raiseError("Trophy '%s' appears to be missing" % i)
                return False

        return True

    def writeCheevosToPage(self,cheevosDict):
        self._beginSession()
        self.validateTrophyAttachments()

        count = 0
        
        self.pageHandle["content"] += self.RowStart 
        self.pageHandle["content"] += self.ColTitleStart 
        self.pageHandle["content"] += "Count"
        self.pageHandle["content"] += self.ColTitleEnd
        self.pageHandle["content"] += self.ColTitleStart 
        self.pageHandle["content"] += "Engineer"
        self.pageHandle["content"] += self.ColTitleEnd
        self.pageHandle["content"] += self.ColTitleStart 
        self.pageHandle["content"] += "Achievement"
        self.pageHandle["content"] += self.ColTitleEnd
        self.pageHandle["content"] += self.RowEnd

        keys = sorted(cheevosDict.keys(),reverse=True)
        while (count < (self.numTrophies) and count < len(keys)): 
            if self.verbose:
                print self.RowStart 
                print self.ColStart + str(keys[count]) + self.ColEnd
                print self.ColStart + "<br>".join(cheevosDict[keys[count]]) + self.ColEnd
                print self.ColStart + self.AttachStart + self.trophyList[count] + self.AttachEnd + self.ColEnd
                print self.RowEnd
            else:
                self.pageHandle["content"] += self.RowStart 
                self.pageHandle["content"] += self.ColStart + str(keys[count]) + self.ColEnd
                self.pageHandle["content"] += self.ColStart + "<br>".join(cheevosDict[keys[count]]) + self.ColEnd
                self.pageHandle["content"] += self.ColStart + self.AttachStart + self.trophyList[count] + self.AttachEnd + self.ColEnd
                self.pageHandle["content"] += self.RowEnd
            count += 1

        self._endSession()

    def getPageURL(self, configData):
        '''
        Calculate final URL of generated confluence page
        '''
        baseURL = re.sub('/rpc/xmlrpc','', configData['content_system']['server_URL'])
        urlStr = "%s/display/%s/%s" % (baseURL,configData['content_system']['space'],configData['content_system']['page'])
        return urlStr

