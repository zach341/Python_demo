import cgi 
from urllib import parse
import codecs
import cgitb

cgitb.enable(display=1, context=5, format="html")

header = "Content-Type: text/html; charset='utf-8'\n\n"
url = '/cgi-bin/friendsC.py'
file_path = r'C:\Users\zach.zhang\Desktop\testzach\webtest\cgi-bin\result.txt'

commenthtml = """<html><head><title>
Comment Page</head></title>
<body>
<h3>欢迎输入您的评论</h3>
<form>
<textarea name = comment_content style = "width:300px; height:60px"></textarea>
<p><input type = "submit" value = "提交">
</form>
</body>
</html>
"""
errhtml = """<html><head><title>
Friends Cgi Demo></title></head>
<body><h3>ERROR</h3>
<B>%s<p></B>
<form><input type = button value = back onclick ="window.history.back()"></form>
</body></html>"""

feedbackhtml = """<html><head><title>
Comment Page</head></title>
<body>
<h3>欢迎输入您的反馈</h3>
<form>
<textarea name = feedback_content style = "width:300px; height:60px"></textarea>
<p><input type = "submit" value = "提交">
</form>
</body>
</html>
"""

def showError(error_str):
    print((header+errhtml) % error_str)

def showComment():
    print(header + commenthtml)

def showfeedback():
    print(header +feedbackhtml)

def showthank():
    print(header +"""
    <html><head><title>
    result</head></title>
    <body><h2>thank you</h2>
    </body>
    </html>
    """)

formhtml = """</html><head>
<title>Friends Cgi Demo</head></title>
<body><h3>Friends list for: <I>%s</I></h3>
<form action = "%s">
<B> Enter your name: </B>
<input type = hidden name = action value = edit>
<input type = text id = "txt" name = person value = "%s" size = 15>
<p><B> how many friends do you have </B>
%s
<p><input type = submit>
<p><input type = submit name = showCM value = "comment">
<p><input type = submit name = showFB value = "feedback">
</form></body></html>"""

fradio = '<input type = radio name = howmany value ="%s" %s> %s\n'

def showForm(who,howmany):
    friends = []
    for i in (0,10,25,50,100):
        check = ''
        if str(i) == howmany:
            check = 'checked'
        friends.append(fradio%(str(i),check,str(i)))

    print((header+formhtml)%(who,url,who,''.join(friends)))

reshtml = """<html><head><title>
Friends Cgi Demo </title></head>
<body><H3>Friends list for: <I>%s</I><H3>
your name is: <B>%s</B><p>
you have <B>%s</B> friends.
<p>Click <a href = "%s">here</a> to edit your data again.
<form><input type = button value = clear name = test></form>
</body></html>"""

def doResult(who,howmany):
    newurl = url + '?action=reedit&person=%s&howmany=%s'%\
        (parse.quote_plus(who), howmany)
    print((header + reshtml) % (who, who, howmany, newurl))

def process():
    error = ''
    form = cgi.FieldStorage()

    if 'comment_content' in form:
        cgitb.handler()
        test1 = form['comment_content'].value
        fp = open(file_path, 'a+',encoding="UTF-8")
        fp.write("%s%s" % (test1, '\n'))
        fp.close()
        with codecs.open(file_path, 'r', encoding="UTF-8") as f, codecs.open\
        ("C:\\Users\\zach.zhang\\Desktop\\testzach\\webtest\\cgi-bin\\result666.txt", 'w', encoding="gbk") as wf:
            for line in f:
                #lines = line.strip().split('\t')
                newline = line
                wf.write(newline)
        showthank()
        return
    if 'feedback_content' in form:
        test2 = form['feedback_content'].value
        # fp = open(file_path, 'a+')
        # test2 = bytes(test2, 'utf-8')
        # fp.write(test2)
        # fp.close()
        showthank()
        return
    if 'showCM' in form:
        showComment()
        return
    if 'showFB' in form:
        showfeedback()
        return
    if 'person' in form:
        who = form['person'].value
    else:
        who = 'New User'
    
    if 'howmany' in form:
        howmany = form['howmany'].value
    else:
        if 'action' in form and \
            form['action'].value == 'edit':
            error = 'Please select number of friends.'
        else:
            howmany = 0

    if not error:
        if 'action' in form and \
            form['action'].value != "reedit":
            doResult(who,howmany)
        else:
            showForm(who,howmany)
    else:
        showError(error)

    if 'test' in form:
        fp = open(r'C:\Users\zach.zhang\Desktop\testzach\webtest\cgi-bin\file.txt','r+')

if __name__ == "__main__":
    process()