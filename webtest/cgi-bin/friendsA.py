import cgi

reshtml = """Content-Type: text/html\n
<html><head><title>
Friends CGI Demo (dynamic screen)
</title></head>
<body><h3>Friends list for: <I>%s</I></h3>
your name is: <b>%s</b><p>
your have: <b>%s</b> friends
</body></html>"""

form = cgi.FieldStorage()
who = form['person'].value
howmany = form['howmany'].value
print(reshtml%(who,who,howmany))
