#!/usr/bin/python 

import pyzabbix, sys, json, os, time

if len(sys.argv) > 2:
    IMPORT_DIR = sys.argv[1]
    ZABBIX_SERVER = sys.argv[2]
else:
    IMPORT_DIR = "import_pack"
    ZABBIX_SERVER = 'http://localhost'

print "*****"
print "** App iports files in Lexicographical order from '{0}' folder".format(IMPORT_DIR)
print "*****"
print ""

zapi = pyzabbix.ZabbixAPI(ZABBIX_SERVER)
zapi.login('admin', 'zabbix')

def readFile(f):
    with open(f, 'r') as f:
        return f.read()

def importAction( str ):
    data = json.loads(str)
    for action in data:
        try:
            print "Create: {0}".format(json.dumps(action))
            zapi.action.create(action)
        except pyzabbix.ZabbixAPIException as e:
            print e

def importHostGroups( str ):
    data = json.loads(str)
    for group in data:
        try:
            zapi.hostgroup.create({"name": group["name"]})
        except pyzabbix.ZabbixAPIException as e:
            print e

def importTemplate( str ):
    data = json.loads(str)
    zapi.template.create(data)

def importTemplateXml( template ):
    rules = {
        'applications': {
            'createMissing': 'true',
            'updateExisting': 'true'
        },
        'discoveryRules': {
            'createMissing': 'true',
            'updateExisting': 'true'
        },
        'graphs': {
            'createMissing': 'true',
            'updateExisting': 'true'
        },
        'groups': {
            'createMissing': 'true'
        },
        'hosts': {
            'createMissing': 'true',
            'updateExisting': 'true'
        },
        'images': {
            'createMissing': 'true',
            'updateExisting': 'true'
        },
        'items': {
            'createMissing': 'true',
            'updateExisting': 'true'
        },
        'maps': {
            'createMissing': 'true',
            'updateExisting': 'true'
        },
        'screens': {
            'createMissing': 'true',
            'updateExisting': 'true'
        },
        'templateLinkage': {
            'createMissing': 'true',
            'updateExisting': 'true'
        },
        'templates': {
            'createMissing': 'true',
            'updateExisting': 'true'
        },
        'templateScreens': {
            'createMissing': 'true',
            'updateExisting': 'true'
        },
        'triggers': {
            'createMissing': 'true',
            'updateExisting': 'true'
        },
    }
    zapi.confimport('xml', template, rules)

def readHostGroupVars():
    vars = {}
    groups = zapi.hostgroup.get()
    for g in groups:
        key = g["name"].upper().replace(" ", "_")
        vars[key] = g["groupid"]
    return vars

def readTemplatesGroupVars():
    vars = {}
    templates = zapi.template.get()
    for t in templates:
        key = t["name"].upper().replace(" ", "_")
        vars[key] = t["templateid"]
    return vars

def replaceVars(data, prefix, dic):
    for key, value in dic.iteritems():
        data = data.replace("<" + prefix + key + ">", value)
    return data

dir = os.path.abspath(IMPORT_DIR)
for fileName in sorted(os.listdir(IMPORT_DIR)):
    print ""
    print "import {0}".format(fileName)
    print "-----"
    f = os.path.join(dir, fileName)
    data = readFile(f)
    time.sleep(1)
    basename = os.path.basename(f)
    if "action" in basename:
        varGroups = readHostGroupVars()
        varTpls = readTemplatesGroupVars()
        data = replaceVars(data, "REPLACE_ME_GROUP_", varGroups)
        data = replaceVars(data, "REPLACE_ME_TPLS_", varTpls)
        importAction(data)
        continue
    if "hostgroup" in basename:
        importHostGroups(data)
        continue
    if "template.xml" in  basename:
        importTemplateXml(data)
        continue
    if "template" in  basename:
        importTemplate(data)
        continue
