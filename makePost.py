#!/usr/bin/python
print 'Content-type: text/html\n'
print ''

import cgi,cgitb,os,random,hashlib

#cgitb.enable()

def makerow():#Makes formatting look better!
    return """
        <center>
        <div class="row">
        <div class="callout small">
        <div class="medium-6 small-centered columns">
        """
def closeRow():#Helps make formatting look better!
    return """         </div></div></div> </center> """

def header():#HTML header which incorporates CSS to make webpage look better!
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

def footer():#Ends HTML
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
D = FStoD()#Sets D as a dictionary made from the search query
def textbox(): #creates user input textbook so that the user can make a post
    p = makerow()
    
    p += """
        <form method="get" action='posts.py'>
<h2> Make A Post </h2>
<input type="hidden" name="user" value='""" + D["user"]+ """' /> 
<input type="hidden" name="magicnumber" value='""" + D["magicnumber"]+ """' />
<div align="center" > <textarea rows="5" name="new_post" cols="50"></textarea> </div>
<br>
<div align = "center"><button class="button" type="submit" value="Make your post!" name="pushit"
>Make Post<button/> </div> <br>
</form> """
    p += closeRow()
    return p

def securefields():#Assists with making links
    if 'user' in D and 'magicnumber' in D:
        user = D['user']
        magicnumber = D['magicnumber']
        return "?user="+user+"&magicnumber="+str(magicnumber)
    return ""
def makeLink(page):#Makes a link with securefields()
    return page+securefields()
def tableee(page, text):
	print """<table align= "right" border="1" bgcolor= "#8E4EF4"> <tr><td><font size= "6">""" + """<a href="""+page+securefields()+""">"""+ text+ """</a></font></td></tr></table>"""



print header()
print textbox()
tableee("page1.py", "Profile")
print footer()
"""Above few lines of code call previously defined functions"""
