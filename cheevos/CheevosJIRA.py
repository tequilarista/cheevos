#!/usr/bin/python
'''
cheevos

A tool for generating fun stats about bugs and the devs who hack on them
'''

import csv
import os
import json
import sys

from CheevosBase import *
from jira.client import JIRA # pip install jira

class CheevosJIRA(CheevosBase):
    #def __init__(self, confName):
    def __init__(self):
        CheevosBase.__init__(self)
        self.jiraConn = None
        self.serverURL = None
        self.jqlQuery = None
        self.jiraUsername = None
        self.jiraPassword = None

    def loadJIRAInfoFromConfig(self,configData):
        '''
        Read template and extra info necessary to create connection to JIRA server
        '''
        self.jqlQuery = configData['bug_system']['REST_query']
        self.serverURL = configData['bug_system']['server_URL']
        self.jiraUsername = configData['bug_system']['username']
        self.jiraPassword = configData['bug_system']['password']
        if not (self.jqlQuery or self.serverURL or self.jiraUsername or self.jiraPassword):
            self.raiseError("Missing necessary connection from %s template" % self.tmplName) 

    def _createConnection(self):
        jira_server = {'server': self.serverURL}
        jira_auth = (self.jiraUsername,self.jiraPassword)
        try:
            self.jiraConn = JIRA(options=jira_server,basic_auth=jira_auth)
        except Exception, e:
            self.raiseError("Unable to create connection to JIRA", e)

    def runQuery(self):
        self._createConnection()
        try:
            jql_res = self.jiraConn.search_issues(self.jqlQuery, startAt=0, maxResults=None, fields="assignee,id", expand=None, json_result=True)
        except Exception, e:
            msg = "Failed to run JIRA query: %s" % self.jqlQuery
            self.raiseError(msg, e)
            raise


        return jql_res

    def getUserNamesFromQueryResults(self, res):
        ''' This lookup is based on the following format of JIRA results for queries
            as returned by runQuery() method:
            -------
            {
            "issues": [
                {
                    "expand": "editmeta,renderedFields,transitions,changelog,operations",
                    "fields": {
                        "assignee": {
                            "active": true,
                            "displayName": "Jane Developer",
                            "emailAddress": "jane.developer@mycompany.com",
                            "name": "jane.developer",
                            "self": "https://jira.mycompany.com/rest/api/2/user?username=jane.developer"
                        }
                    },
                    "id": "233715",
                    "key": "PROJ-123",
                    "self": "https://jira.mycompany.com/rest/api/2/issue/233715"
                    },
            -------
        '''
        devlist = []
        for elem in res['issues']:
            displayName = None
            try:
                displayName = elem['fields']['assignee']['displayName']
            except Exception:
                displayName = "Unknown"

            devlist.append(displayName)

        return devlist

    def tabulateUsers(self,devlist):
        aggregateData = {}
        finalDict = {}

        for dev in devlist:
            if not dev in aggregateData.keys():
                aggregateData[dev] = 1
            else:
                aggregateData[dev] += 1

        # magic that sorts everything by number of bug fixes, reverse order
        for key, value in sorted(aggregateData.iteritems(), 
                key=lambda (k,v): (v,k), reverse=True):
            if self.verbose:
                print "%s: %s" % (key, value)
            if value not in finalDict:
                finalDict[value] = [key]
            else: 
                finalDict[value].append(key)

        if len(finalDict.keys()) < 1:
            self.raiseError("Error Problem tabulating users!")
        return finalDict



