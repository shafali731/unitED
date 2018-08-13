#!/usr/bin/python
print 'Content-type: text/html\n'
print ''

import cgi,cgitb,os

#cgitb.enable()

def makerow():
    return """
        <center>
        <div class="row">
        <div class="callout small">
        <div class="medium-6 small-centered columns">
                """
def closeRow():
    return """         </div></div></div> </center> """
def header():#HTML header to improve the general layout of the site and how it looks. Incorporates CSS to make the frontend look even better!
    return"""
        <!DOCTYPE HTML>
        <html>
        <head>
        <title>HandShake</title>
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="foundation/css/foundation.css">
        <link rel="stylesheet" href="foundation/css/app.css">
        </head>
        <style>
        body {
        background-color:white;
        color: #000;
        padding: 0;
        margin: 0;
        font-family: "Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;
        font-weight: normal;
        font-style: normal;
        line-height: 1;
        position: relative;
        cursor: default;
        }
        .button {
        background-color:#17BEBB;
        
        }
        .callout-small{
        background-color:#8E4EF4;
        }
        .callout-1{
        background-color:#3993DD;
        padding: 1em;
        border: 1px solid rgba(10, 10, 10, 0.25);
        }
        
        h1 {
        color:white;
        }
        h2 {
        color:black;
        }
        </style>
        <body>
        <div class="beginning">
        <div class="callout-small">
        <center><h1><b>Hello """ + D["user"] + """</b></h1> </font>
            </center>
            </div>
            </div>"""
def footer():#returns end of HTML
    return """</body>
</html>"""

def FStoD():
    '''
    Converts cgi.FieldStorage() return value into a standard dictionary
    '''
    d = {}
    formData = cgi.FieldStorage()
    for k in formData.keys():
        d[k] = formData[k].value
    return d
D = FStoD()#Makes D = what's in the search query
def userprofile():#loads otheruser's description and other parts of profile
    if "otheruser" in D:
        F = open("profiles.txt","r")
        File = F.readlines()
        F.close()
        exist = False#automatically starts out as false, is true if the otheruser that was inputted is an actual user.
        i = 0
        for x in File:
            File[i]= File[i].strip()
            File[i] = File[i].split(",")
            if File[i][0] == D["otheruser"]:
                description = File[i][1]#Sets the otheruser's description to variable
                exist = True
            i += 1
        p = makerow() + '<h2>'#Makes description look better!
        if exist:
            p += "Username: " + D["otheruser"] + "<br>Description: " + description + '</h2>'#if otheruser input value exists adds the otheruser's information
        else:
            p += "No such user exists!" + '</h2>'
        p += closeRow()#Makes description printed out look better!
        return p

def otheruserposts():#Returns list of otheruser's old posts
    F = open("users.txt","r")#posts recorded on users.txt
    File = F.readlines()
    F.close()
    i = 0
    for x in File:
        File[i]= x.strip()
        File[i] = File[i].split(",")
        if File[i][0] == D["otheruser"]:
            return File[i][2:]#returns everything the user has posted without returning the encrypted password or username from users.txt
        i +=1
    return ""

def tablify(L):#Makes table from list of posts
    l = len(L)
    i= 0
    table = ""
    begintable = "<table border ='1'>"
    while l > 0:
        table = "<tr><td>"
        table = table + "Post #" + str(l) + "</td><td>"
        table += L[i]
        table += "</td></tr>"
        l -= 1
        i += 1
    return begintable + table + "</table>"

def tablifyolduserposts():
    posts = otheruserposts()#Makes posts a list of all otheruser's posts
    if "otheruser" in D and len(posts) > 0 and not(userprofile() == "No such user exists!"):#Checks to make sure it's necessary to print out a table
        g = makerow()
        g += """<br><h2>Here are """ + D["otheruser"] +"""'s old posts</h2>""" + tablify(posts)#Processes other user's posts to make a table of posts
        g += closeRow()
        print g
def tableee(page, text):
	print """<table border="1" bgcolor= "pink" align= "right"> <tr><td><font size= "6">""" + """<a href="""+page+securefields()+""">"""+ text+ """</a></font></td></tr></table>"""
def securefields():
    if 'user' in D and 'magicnumber' in D:
        user = D['user']
        magicnumber = D['magicnumber']
        return "?user="+user+"&magicnumber="+str(magicnumber)
    return ""
print header()
print userprofile()
tableee("page1.py", "Profile")
tablifyolduserposts()


print footer()
"""Above functions call on everything defined throughout this File!"""