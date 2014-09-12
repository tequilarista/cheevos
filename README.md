Overview
========

CHEEVOS!

A tool for doing silly gamification of the development process by allowing a manager/PM/whoever
define achievments that will query a bug/task system and generate a corresponding high score list
that can be displayed on random screens.

Good for bragging rights, throwdowns, and other sundry critical aspects of the software development
process.

### JIRA Info
Just provide valid credentials and JQL search query string and you're good.  Doesn't work with
saved searches yet, however.

### Confluence Info
Currently you are required to pre-create your Confluence page and pre-upload
your trophy image attachments.  This is because both the Confluence xmlrpc and 
python APIs currently hate me, but I'm hoping for a future reconciliation.

Size is up to you but personally I try to avoid anything bigger than 200x200. 
"Your mileage may vary"

### Future Plans
* Jenkins integration as an input

* Github as an input/output

* Bugzilla 5 as an input, esp. since they're coming out with a new RESTful API

* My current Bamboo input implementation I've been using is not shareable in its current state, 
going to rewite that module before posting it.


Usage
=====
    usage: cheevos [-h] [--inputType <issue system>]
                   [--outputType <content mgr system>] [--trophyName trophyName]
                   [--confName confName]

    Let's make some cheevos!

    optional arguments:
      -h, --help            show this help message and exit
      --inputType <issue system>
                            Bug data store [default value = jira]
      --outputType <content mgr system>
                            Content display [default value = confluence]
      --trophyName trophyName
                            Unique name for your cheevo trophy
      --confName confName   Unique tag to include in configuration template name

Summary:
-------
To create easy access template, run:

    % cheevo --trophyName top-bug-fixer

Edit subsequent "cheevos-top-bug-fixer.conf" file.  Will look something like this:

    {
        "bug_system": {
            "REST_query": "",
            "password": "",
            "server_URL": "",
            "type": "jira",
            "username": ""
        },
        "content_system": {
            "page": "",
            "password": "",
            "server_URL": "",
            "space": "",
            "type": "",
            "username": ""
        },
        "trophies": {
            "num_trophies": null,
            "trophy_1": "",
            "trophy_2": "",
            "trophy_3": ""
        }
          }

A completed config file will look like this:

    {
        "bug_system": {
            "REST_query": "issuetype = bug AND resolutiondate >= '-6d' AND Resolution in (done,fixed)", 
            "password": "jiraUser", 
            "server_URL": "http://jira.mycompany.com", 
            "type": "jira", 
            "username": "jiraPassword"
        }, 
        "content_system": {
            "page": "TopBugFixer", 
            "password": "confluencePassword", 
            "server_URL": "http://confluence.mycompany.com/rpc/xmlrpc", 
            "space": "MyProjectSpace", 
            "type": "confluence", 
            "username": "confluenceUser"
        }, 
        "trophies": {
            "num_trophies": 3,
            "trophy_1": "gold_trophy.jpeg", 
            "trophy_2": "silver_trophy.jpeg", 
            "trophy_3": "bronze_trophy.jpeg"
        }
    }

Now that you have a completed config file, you can start generating your cheevos page!

    % cheevos --confName cheevos-top-bug-fixer.conf


Authors
-------
Author:: Tara Hernandez (tequilarista@gmail.com)

