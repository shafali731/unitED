#!/usr/bin/python
print 'Content-type: text/html\n'
print ''

import cgi,cgitb,os,random,hashlib

#cgitb.enable()checks for errors in the code and shows them live on the website, code working so commented out 

def header():#HTML heading... also lets user know that their login status is being checked
        return """
    <!DOCTYPE HTML>
    <html>
    <head>
    <title>login checker</title>
    </head>
    <body>
    Checking your login status...<br>
    """
    
def footer():#HTML ending
    return """</body>
</html>"""

def md5Pass(password):#Uses advanced algorithm to encode the password
    m = hashlib.md5()
    m.update(password)
    return m.hexdigest()

def checkIfNameExists(user):#If user in users.txt returns true, else returns false
    text = open('users.txt', 'r').readlines()
    print text
    for line in text:#For loops through all of "users.txt" checking if the user is in it
        if line.split(",")[0]==user:
            return True
    return False

def authenticate(user,password):#Uses username and password as a "password" thats encrypted as a code
    password = md5Pass(password+user) # you can make this different, but still unique md5Pass(password+user)
    text = open('users.txt', 'r').readlines()
    for line in text:
        line = line.strip().split(",")
        if line[0]==user:#checks if the user you inputted is the same 
            if line[1]==password:#Checks if the password you inputted after being reencrypted matches with the current one in the data base of users.txt
                return True #Returns true if you inputted a correct password + username
            else:
                return False
    return False

#the following code takes care of making sure the user is recognized
#as being logged in on other parts of the website
#remove a user, only do this if they successfully authenticated
#since this does not check to see if you have the right person
def remove(user):#Removes a persons log in status
    infile = open('loggedin.txt','r')
    text = infile.read()
    infile.close()
    if (user+",") in text:
        #remove code
        outfile = open('loggedin.txt','w')
        lines = text.split('\n')
        for i in range(len(lines)):
            lines[i]=lines[i].split(",")
            if len(lines[i]) > 1:
                if(lines[i][0] != user):
                    outfile.write(','.join(lines[i])+'\n')
        outfile.close();


#only meant to be run after password authentication passes.
#uses call to remove(user) that will remove them no matter what.
def logInUser(username):#Generates magic number to go along with each signed in user
    magicNumber = str(random.randint(1000000,9999999))
    remove(username)
    outfile = open('loggedin.txt','a')
    IP = "1.1.1.1"
    if "REMOTE_ADDR" in os.environ :
        IP = os.environ["REMOTE_ADDR"]
    outfile.write(username+","+magicNumber+","+IP+"\n")
    outfile.close()
    return magicNumber
            
def login(form):
    result = ""
    if not ('user' in form and 'pass' in form):
        return "Username or password not provided"
    user = form['user'].value
    password = form['pass'].value
    if authenticate(user,password):#if user and pass match one in users.txt
        result += "Success!<br>\n"
        #add user to logged in status
        magicNumber = logInUser(user)
        result += '<a href="page1.py?user='+user+'&magicnumber='+str(magicNumber)+'">Click here to go to the main site!</a>'#Adds magic number and username to search query so the site can process them
    else:
        result += """Failed to log in, authentication failure<br><a href ="index.html">Try again here!</a>"""
    return result


def notLoggedIn():
    return '''You need to login, <a href="login.html">here</a>\n'''

def main():#Combines everything above together!
    form = cgi.FieldStorage()
    body = ""
    if len(form)==0:#if nothing inputted, return message saying to login
        body += notLoggedIn()
    else:
        body += login(form)#Goes through entire login(form) function above to generate a login message if user succesfully logins. Also, changes serach query to match the logged in user. 
    print header() + body + footer()#Prints everything

main()#Calls on function to print everything
