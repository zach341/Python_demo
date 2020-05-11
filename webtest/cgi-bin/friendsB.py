import cgi

header = 'Content-Type: text/html\n\n'

formhtml = """<html><head><title>
Friends Cgi Demo</title></head>
<body><h3>friends list for: <I>NEW USER</I></h3>
<form action = "/cgi-bin/friendsB.py">
<b>Enter your name: </b>
<input type=hidden name = action value = edit>
<input type = text name = person value = "new user" size = 15>
<p><b>how many friends do you have?</b>
%s
<p><input type = submit></form></body></html>"""

fradio = '<input type = radio name = howmany value = "%s" %s> %s\n'

def showForm():
    friends = []
    for i in (0,10,25,50,100):
        check = ''
        if i == 0:
            check = "checked"
        friends.append(fradio%(str(i),check,str(i)))
    
    print( '%s%s' % (header , formhtml % ''.join(friends)))

reshtml = """<html><head><title>
Friends Cgi Demo</title></head>
<body><h3>friends list for : <I>%s</I></h3>
your name is: <B>%s</B><p>
your have <B>%s</B> friends.
</body></html>"""

def doResults(who, howmany):
    print((header+reshtml)%(who,who,howmany))

def process():
    form = cgi.FieldStorage()
    if 'person' in form:
        who = form['person'].value
    else:
        who = 'NEW USER'

    if 'howmany' in form:
        howmany = form['howmany'].value
    else:
        howmany = 0
    if 'action' in form:
        doResults(who,howmany)
    else:
        showForm()

if __name__ == '__main__':
    process()
