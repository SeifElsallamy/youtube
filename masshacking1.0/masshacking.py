import requests
import json
import difflib
import os

auth=('<your hackerone username>', '<your hackerone api key>')

h2 = ""
script_dir = os.path.dirname(os.path.abspath(__file__))
def getAllPrograms():
    global auth
    for i in range(1,7):
        headers = {'Accept': 'application/json'}
        r = requests.get('https://api.hackerone.com/v1/hackers/programs?page[size]=100&page[number]='+str(i), auth=auth,headers = headers)
        programs = r.json()["data"]
        for program in programs:
            if program["attributes"]["offers_bounties"]:
                text = "Name: " + str(program["attributes"]["name"]) + "\n"
                text = text + "Handle: " + str(program["attributes"]["handle"]) + "\n"
                text = text + "Valid Reports Per User: " + str(program["attributes"]["number_of_valid_reports_for_user"]) + "\n"
                text = text + "Start accepting at: " + str(program["attributes"]["started_accepting_at"]) + "\n"
                text = text + "Mode: " + str(program["attributes"]["state"]) + "\n"
                text = text + "Accept Submission: " + str(program["attributes"]["submission_state"]) + "\n"
                text = text + "Allow Splitting: " + str(program["attributes"]["allows_bounty_splitting"]) + "\n"
                text = text + "Currency: " + str(program["attributes"]["currency"])
                getAssets(str(program["attributes"]["handle"]), text)

def getAssets(handle, text):
    global h2
    global auth
    text2=""
    headers = {'Accept': 'application/json'}
    r = requests.get('https://api.hackerone.com/v1/hackers/programs/'+handle, auth=auth, headers = headers)
    try:
        scopes = r.json()["relationships"]["structured_scopes"]["data"]
        for scope in scopes:
            if scope["attributes"]["eligible_for_bounty"] and ("2023" in scope["attributes"]["created_at"] or "2023" in scope["attributes"]["updated_at"]):
                text2 = text2 + scope["attributes"]["asset_identifier"] + "\n"
    except:
        pass
    if text2:
        h2 = h2 + text + "\n" + text2 + "\n"
        print(text)
        print(text2)

def writeResults():
    global h2
    global script_dir
    global h3
    h3 = "\n".join(h3)
    with open(os.path.join(script_dir, 'program_details.txt'), "w") as f:
        f.write(h2)
    with open(os.path.join(script_dir, 'domains.txt'), "w") as f:
        f.write(h3)

def getTargets():
    global h2
    c = h2.splitlines()
    doms = []
    urls = []
    for dom in c:
        dom1 = ""
        if "//" in dom:
            dom = dom.split("//")[1]
        if "*." in dom:
            dom1 = dom.replace("*.","blog.")
            dom = dom.replace("*.","")
            dom1 = dom1.replace("*","")
            dom = dom.replace("*","")
        if dom and (" " not in dom) and ("." in dom) and (dom.count("/") < 2) and (not dom.startswith("com.")) and ( "ios" not in dom.lower()) and ( "android" not in dom.lower()):
            if dom[-1] == "/":
                dom = dom.split("/")[0]
                dom1 = dom1.split("/")[0]
            if "/" in dom:
                continue
            doms.append(dom)
            if dom1:
                doms.append(dom1)
    doms = list(set(doms))
    return doms



getAllPrograms()
h3 = getTargets()
writeResults()
