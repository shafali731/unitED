#!/usr/bin/python
import cgi,cgitb,os
cgitb.enable()
def header():
    return """content-type: text/html

<!DOCTYPE HTML> 
<html>
<head>
<title>logout</title>
</head>
<body>
Attempting to log you out...<br>

"""

def footer():
    return """</body>
</html>"""

#remove a user, only do this if they successfully authenticated
#since this does not check to see if you have the right person
def remove(user,magicnumber):
    text = open('loggedin.txt','r').read()
    result = "User not logged out<br>\n"
    if (user+",") in text:
        #remove code
        outfile = open('loggedin.txt','w')
        lines = text.split('\n')
        for i in range(len(lines)):
            lines[i]=lines[i].split(",")
            if len(lines[i]) > 2:
                if(lines[i][0] != user or lines[i][1] != str(magicnumber) ):
                    outfile.write(','.join(lines[i])+"\n")
                else:
                    result = "Logged out user<br>\n"
        outfile.close();
    else:
        result = "User not found<br>\n"
    return result


def processForm(form):
    if( 'user' in form and 'magicnumber' in form): #checks for username and magic number 
        user = form.getvalue('user') #obtains username
        mn = form.getvalue('magicnumber') #obtains magicnumber
        return remove(user,mn) #removes user 
    return "You must be logged in properly to log out!<br>\n"

def notLoggedIn():
    return "You must be loggedin before trying to log out!<br>\n"

def main():
    form = cgi.FieldStorage() 
    body = ""
    if len(form)==0:
        body += notLoggedIn()  #if there isn't anything inn the query string, they were not logged in 
    else:
        body += processForm(form)		
    print header() + body 


main()
print """<a href ="index.html">HandShake</a>""" #link back to homepage
footer()
