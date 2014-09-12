cheevosTemplate = { 'bug_system': {'type': "", 'server_URL': "", 'REST_query': "", 'username': "", 'password': "", }, 'trophies': {'num_trophies': None, 'trophy_1': "", 'trophy_2': "", 'trophy_3': "", }, 'content_system': {'type': "", 'server_URL': "", 'username': "", 'password': "", } }


check = 1
numTrophies = 3
trophyList = []
while check <= numTrophies:
    trophyFile = 'trophy_%s' % str(check)
    if cheevosTemplate['trophies'].has_key(trophyFile):
        trophyList.append(cheevosTemplate['trophies'][trophyFile])
        check += 1



import os

template = "/Users/tara.hernandez/.newpony.conf"
(userAuthArg, passAuthArg, serverArg, projectArg) = loadTemplate()
duration = "1w"
p = Pony("test.user", "test commentaries", userAuthArg, passAuthArg, serverArg, projectArg, duration)
jiraSummary = "%s requested help with: %s" % (p.customer, p.comment)
id = p.createTicket(jiraSummary)        

issue = jira.issue(id)
transitions = jira.transitions(issue)
print [(t['id'], t['name']) for t in transitions]  



baseObj = CheevosBase()
configData = baseObj.loadTemplate("/Users/tara.hernandez/Projects/github/cheevos/cheevos-bounties.json")
c = CheevosConfluence()
c.loadConfluenceInfoFromConfig(configData)
filename = os.path.basename(c.trophyList[0])

cheevosDict = {1: [u'Sheetal Kakkad', u'Phu Nguyen', u'Matthew Bogner', u'Marcia So', u'Khai Nguyen', u'Kevin Chan', u'Jon Ingle', u'Jackson Lin', u'Bhavin Brahmkshatriya', u'Bhakti Pawar', u'Adam Ayres'], 2: [u'Shane Davis'], 4: [u'Daniel Schoonmaker', u'Chad Schellenger'], 5: [u'David Gardner'], 6: [u'Chanh Dinh'], 8: [u'Chris McNelis'], 10: [u'Aditya Kumar']}

c._beginSession()

c.writeCheevosToPage(cheevosDict)

#from confluence import Confluence
#conf = Confluence(url="http://confluence.dev.lithium.com",username=c.username,password=c.password)



def _raiseError(msg,exception=None):
    errorMsg = "%s\n" % msg
    if exception:
        errorMsg += "Exception:\n---------\n %s\n---------" % exception
    raise CheevosError(errorMsg)

try:
    page = conf.storePageContent("foofoo", c.wikiSpace, pageHandle)
except Exception, e:
    msg = "Unable to write page to confluence server. Check to see if it exists"
    _raiseError(msg,e)

'''
<p>&lt;p&gt;&lt;table&gt;&lt;tbody&gt;&lt;br/&gt;<br />\n
    &lt;tr&gt;&lt;br/&gt;<br />\n
        &lt;th&gt;&lt;p&gt;Count&lt;/p&gt;&lt;/th&gt;&lt;br/&gt;<br />\n
        &lt;th&gt;&lt;p&gt;Engineer&lt;/p&gt;&lt;/th&gt;&lt;br/&gt;<br />\n
        &lt;th&gt;&lt;p&gt;Trophy&lt;/p&gt;&lt;/th&gt;&lt;br/&gt;<br />\n
        &lt;/tr&gt;
        &lt;tr&gt;&lt;br/&gt;<br />\n
        &lt;td align=&quot;center&quot;&gt;&lt;h1 style=&quot;text-align: center;&quot;&gt;10&lt;/p&gt;&lt;/h1&gt;&lt;/td&gt;&lt;br/&gt;<br />\n
        &lt;td align=&quot;center&quot;&gt;&lt;h1 style=&quot;text-align: center;&quot;&gt;Aditya Kumar&lt;/p&gt;&lt;/h1&gt;&lt;/td&gt;&lt;br/&gt;<br />\n
        &lt;td align=&quot;center&quot;&gt;&lt;h1 style=&quot;text-align: center;&quot;&gt;&lt;ac:image&gt;&lt;ri:attachment ri:filename=&quot;gold_mushroom2.jpeg&quot; /&gt;&lt;/ac:image&gt;&lt;/p&gt;&lt;/h1&gt;&lt;/td&gt;&lt;br/&gt;<br />\n
        &lt;/tr&gt;&lt;/tbody&gt;&lt;/table&gt;&lt;/p&gt;</p>'

'''



