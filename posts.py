#!/usr/bin/python
print 'Content-type: text/html\n'
print ''

import cgi,cgitb,os

cgitb.enable()

form= cgi.FieldStorage()
def makerow(): #makes row with css
    return """
        <center>
        <div class="row">
        <div class="callout small">
        <div class="medium-6 small-centered columns">
        """
def closeRow(): #closes row
    return """         </div></div></div> </center> """


def header(): #Heading with formatting 
        return """
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
            .table {
                font-size: 16px; 
                font-family: Arial;
            
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

def makepage(page, text): #link to another page 
    gh = """ <div class="small-4  columns">"""
    gh += '<a href="'+ page +'">'
    gh += """<button class="button"name="status">""" + text + '</button></a></div>'
    return gh

def securefields(): #keeps username and magicnumber in query string and helps in creating a link 
    if 'user' in form and 'magicnumber' in form:
        user = form['user'].value
        magicnumber = form['magicnumber'].value
        return "?user="+user+"&magicnumber="+str(magicnumber)
    return ""


def footer(): #ends html
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
D = FStoD()#Sets D as a dictionary made of the search query
def changeFile(newpost): #appends post to file with username so it can be easily accessable, doesn't use append however it does work in a similar way to append using write
    F = open("users.txt","r")
    File = F.readlines()
    F.close()
    i = 0
    for x in File:
	File[i]= File[i].strip() #removes newlines
        File[i] = File[i].split(",") #breaks file into sublists
        if File[i][0] == D["user"]:
            File[i].append(newpost) 
        i += 1
    i = 0 
    for x in File:
        File[i] = ",".join(File[i])
	i+=1
    File= "\n".join(File)
    File = File + "\n"#Lines above create a large variable File which holds all of the modified contents of the users.txt file
    F = open("users.txt","w")
    F.write(File)#Writes in users.txt
    F.close()
def accessPost():
    F = open("users.txt","r")
    File = F.readlines()
    F.close()
    i = 0
    for x in File:
        File[i] = File[i].split(",")
        if File[i][0] == D["user"]:
            return File[i][-1] #returns most recent post made
        i += 1
def checklen(): #Returns the sublist that is created after processing users.txt, returns the username, password, and any posts made by the user in one list
    F = open("users.txt","r")
    File = F.readlines()
    F.close()
    i = 0
    for x in File:#For loop not necessary, while loop possible as well!
        File[i] = File[i].split(",")#splits everything based on commas
        if File[i][0] == D["user"]:
            return File[i] #returns the entire sublist 
        i += 1
def recentpost():#Returns the most recent post that the user made
    if "new_post" in D:#If new post in search query then returns it 
        changeFile(D["new_post"])
        return '<h2>Your most recent post! <br>' +   D["new_post"]  + '</h2>'
    else:
	if len(checklen()) > 2:#Else returns the newest post that is storied in users.txt
        	return """
<h2> Your most recent post! <br> """ + accessPost() + '</h2>'
	else: 
		return "No post has been made on this account!"
def oldposts():#Returns a list of all old posts
    F = open("users.txt","r")
    File = F.readlines()
    F.close()
    i = 0
    for x in File:
	File[i]= File[i].strip()#gets rid of newlines
        File[i] = File[i].split(",")#splits by commas to make sublists
        if File[i][0] == D["user"]:
            return File[i][2:-1]#Returns full list
	i +=1

def tablify(L):#Tablifies a list 
    l = len(L)
    i= 0  
    begintable = "<table border ='1'>"
    table = ""
    while l > 0:
        table += "<tr><td style='font-size: 16px;'>" + '<h3>'
        table = table + "Post #" + str(l) + "</td></h3><h3><td style='font-size: 16px;'>"
        table += L[i]
        table += "</td>" + '</h3>'
        l -= 1
        i += 1
    return begintable + table + "</table>" 
    

         
def tablifyoldposts():#Combies tablify() with oldposts()
	if len(checklen()) > 3:
		print """<br><h2>Old Posts</h2><br>""" + tablify(oldposts())

def tableee(page, text):#Creates link back to page1.py
	print """<table align= "right" border="1" bgcolor= "#8E4EF4"> <tr><td><font size= "6" color= "white">""" + """<a href="""+page+securefields()+""">"""+ text+ """</a></font></td></tr></table>"""

print header()
print makerow()
print recentpost()
print closeRow()
print makerow()
tablifyoldposts()
print closeRow()
tableee("page1.py", "Profile")
print footer()
"""above lines call on functions defined throughout this file"""

