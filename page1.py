#!/usr/bin/python
import random
import cgi,cgitb,os

#cgitb.enable()

#the field storage is a global variable.
#Since your page has exactly one, you can
#just acccess it from anywhere in the program.
form = cgi.FieldStorage()

def header():#Begins HTML and adds CSS to properly format the webpage and make it look better!
        return """content-type: text/html

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
    body {    background-color:white;
    color: #000;
    padding: 0;
    margin: 0;
    font-family: "Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;
    font-weight: normal;
    font-style: normal;
    line-height: 1;    position: relative;
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
    </div> """

def footer():#Returns end HTML
    return """</body>
</html>"""

def FStoD():
    '''
    Converts cgi.FieldStorage() return value into a standard dictionary
    '''
    d = {}
    formData = cgi.FieldStorage()
    for k in formData.keys():
        d[k] = (formData[k].value)
    return d
D= FStoD()#Makes global variable D a dictionary made of the search query 

def authenticate():#Checks to make sure that you are actually logged in onto an account 
    if 'user' in D and 'magicnumber' in D:
        #get the data from D, and IP from user.
        user = D['user']
        magicnumber = D['magicnumber']
        IP = 'NULL'
        if 'REMOTE_ADDR' in os.environ:
            IP = os.environ["REMOTE_ADDR"]
        #compare with file
        text = open('loggedin.txt').readlines()
        for line in text:
            line = line.strip().split(",")
            if line[0]==user:#when you find the right user name
                if line[1]==magicnumber and line[2]==IP:
                    return True
                else:
                    return False
        return False#in case user not found
    return False #no/missing fields passed into field storage


#either returns ?user=__&magicnumber=__  or an empty string.
def securefields():#helps in making a link in the future
    if 'user' in D and 'magicnumber' in D:
        user = D['user']
        magicnumber = D['magicnumber']
        return "?user="+user+"&magicnumber="+magicnumber
    return ""

def makerow():
    return """<div class="row">"""

#makes a link, link will include secure features if the user is logged in
def makeLink(page, text):
    p = """ <div class="small-4  columns">"""
    p += '<a href="'+page+securefields()+'">'
    p += """<button class="button"name="status">""" + text+'</button></a></div>'
    return p

def loggedIn():
    return '''
'''

def notLoggedIn():#Message that pops up if you aren't logged in. 
    return '''You need to login to see more. You can log in here: <a href="login.html">here</a>\n'''

def closediv():
    return "</div>"

def main():
    body = ""
    #use this to add stuff to the page that anyone can see.
    body += ""
    body += makerow()

    #determine if the user is properly logged in once. 
    isLoggedIn = authenticate()

    #use this to determine if you want to show "logged in " stuff, or regular stuff
    if isLoggedIn:
        body += loggedIn()
    else:
        body += notLoggedIn()

    #anyone can see this
    body += ""
    #attach a logout link only if logged in
    if isLoggedIn:
        body+= makeLink("logout.py","Click here to log out")

    #make links that include logged in status when the user is logged in
    body += makeLink("makePost.py","Click here to make a post!")
    body += makeLink("posts.py","Click here to view your posts!")
    body += closediv()
    #finally print the entire page.
    print header() + body


def tablemake():
	print "<center><h2>" + D["user"] + "'s Profile" + '<h2></center><br>'

def table2():#Allows user to make a description given a textarea and a submit button
	print """<br>
        <center>
        <div class="row">
        <div class="callout small">
        <div class="medium-6 small-centered columns">

    <form name ="input" action="page1.py" method="GET">
    <h2> Update Description </h2>
    <input type="hidden" name="user" value='""" + D["user"]+ """' /> 
    <input type="hidden" name="magicnumber" value='""" + D["magicnumber"]+ """' />
    <div align="center" ><textarea rows="5" name="description" cols="50"></textarea> </div><br>
    <div align = "center"><button class="button" type="submit" value="Update" name="status">Update<button/> </div> <br>
</form></div></div></div> </center>"""

def adddescrip():#Saves most recent description into the "profiles.txt"
    if "description" in D:
        F = open("profiles.txt","r")
        File = F.readlines()
        F.close()
        alreadyexist = False
        i = 0
        for x in File:
            File[i]= File[i].strip()
            File[i] = File[i].split(",")
            if File[i][0] == D["user"]:
                File[i][1] = D["description"]
                alreadyexist = True
            i += 1
        if not alreadyexist:#If user isn't already saved into "profiles.txt", saves the user in by appending it to the file
            F = open("profiles.txt","a")
            F.write("\n" + D["user"] + "," + D["description"])
            F.close()
        else: 
            i = 0
            for x in File:
                File[i] = ",".join(File[i])
                i+=1
            File= "\n".join(File)
            File = File + "\n"
            F = open("profiles.txt","w")
            F.write(File)
            F.close()


def printdescription():#Prints the description onto the webpage
    if "description" in D:#If description recently updated and present in query returns description from query
        return D["description"]
    else:#If no description present in search query, description is taken from the saved "profiles.txt"
        F = open("profiles.txt","r")
        File = F.readlines()
        F.close()
        alreadyexist = False
        i = 0
        for x in File:
            File[i]= File[i].strip()
            File[i] = File[i].split(",")
            if File[i][0] == D["user"]:
                return File[i][1]
            i += 1
        return "No current description!"#If no description present, returns this! 

def otherusr():#Allows user to search for and view other user's profiles by letting them input a username
    print """
    <center>
    <div class="row">
    <div class="callout small">
    <div class="medium-6 small-centered columns">
    
    <form name ="input" action="otheruser.py" method="GET">
    <h2> Search Other Users </h2>
    <input type="hidden" name="user" value='""" + D["user"]+ """' />
        <input type="hidden" name="magicnumber" value='""" + D["magicnumber"]+ """' />
            <div align="center" > <input type= "text" name="otheruser" size= '20'>  </div><br>
            <div align = "center"><button class="button" type="submit" value="Update" name="status">Search<button/> </div> <br>
            </form></div></div></div> </center>""" #Keeps hidden input types so that the webpage keeps the magic number and user

def thatthing():#Makes formatting look better 
    print """<table align= 'center' border= "5" bgcolor= "white" width= 10% > <tr> <td><b> \
    Current Description: </b></td> <td>""" + printdescription() + """<td> </tr> </table>"""
def tableofusers():
    F = open("users.txt","r")
    File = F.readlines()
    i = 0
    L = []
    for x in File:
        File[i] = x.strip()
        File[i] = File[i].split(",")
        L.append(File[i][0])
    return tablify(L)

def tablify(L):
    l = len(L)
    i= 0  
    begintable = "<h2>List of Users</h2><table border ='1'>"
    table = ""
    while l > 0:
        table += "<tr><td style='font-size: 16px;'>" + '<h3>'
        table = table + "User #" + str(l) + "</td></h3><h3><td style='font-size: 16px;'>"
        table += L[i]
        table += "</td>" + '</h3>'
        l -= 1
        i += 1
    return begintable + table + "</table>" 
	

main()
tablemake()
thatthing()
adddescrip()
table2()
otherusr()
print tableofusers()
print footer()
""" Above few lines calls all functions previously defined"""
