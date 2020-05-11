from cgi import FieldStorage
from os import environ
from urllib import parse
from io import StringIO

class AdvCGI(object):
    header = 'Content-Type: text/html\n\n'
    url = '/cgi-bin/advcgi.py'

    formhtml = """<html><head><title>
    Advanced Cgi Demo</title></head>
    <body><h2>Advanced Cgi Demo Form</h2>
    <form method = post action = "%s" enctype = "multipart/form-data">
    <h3>my cookie string</h3>
    <LI><code><B>CPPuser = %s </B></code>
    <h3>Enter cookie value<br>
    <input name = cookie value = "%s"> (<I>optional</I>)</h3>
    <h3>enter your name<br>
    <input name =person value = "%s"> (<I>required</I>)</h3>
    <h3>what languages can you program in?
    (<I>at least one required</I>)</h3>
    %s
    <h3>enter file to upload <small>(max size 4K)</small></h3>
    <input type = file name = upfile value = "%s" size = 45>
    <p><input type = submit>
    </form></body></html>"""

    langset = ('python','Ruby','Java','C++','PHP','C','JavaScript')
    langItem = '<input type = checkbox name = lang value = "%s"%s> %s\n'

    def getCPPCookies(self):
        if 'HTTP_COOKIE' in environ:
            cookies = [x.strip() for x in environ['HTTP_COOKIE'].split(';')]
            for eachCookie in cookies:
                if len(eachCookie)>6 and eachCookie[:3] =='CPP':
                    tag = eachCookie[3:7]
                    try:
                        self.cookies[tag] = eval(parse.unquote(eachCookie[8:]))
                    except (NameError, SyntaxError):
                        self.cookies[tag] = parse.unquote(eachCookie[8:])
                    if 'info' not in self.cookies:
                        self.cookies['info'] = ''
                    if 'user' not in self.cookies:
                        self.cookies['user'] = ''
                else:
                    self.cookies['info'] = self.cookies['user'] = ''
                if self.cookies['info'] != '':
                    self.who, langStr, self.fn = self.cookies['info'].split(':')
                    self.langs = langStr.split(',')
                else:
                    self.who = self.fn = ' '
                    self.langs = ['Python']
    
    def showForm(self):
        self.getCPPCookies()

        langStr = []
        for eachLang in AdvCGI.langset:
            langStr.append(AdvCGI.langItem%(eachLang, 'checked' if eachLang in self.langs else '', eachLang))

        if not ('user' in self.cookies and self.cookies['user']):
            cookStatus = '<I>(cookie has not been set yet)</I>'
            userCook = ''
        else:
            userCook = cookStatus = self.cookies['user']

        print('%s%s'%(AdvCGI.header,AdvCGI.formhtml % (AdvCGI.url, cookStatus, userCook, self.who, ''.join(langStr), self.fn)))

    errhtml = """<html><head><title>
    Advanced CGI Demo</title></head>
    <body><h3>error</h3>
    <B>%s</B><p>
    <form><input type = button value = back
    onclick = "window.history.back()"></form>
    </body></html>"""

    def showError(self):
        print((AdvCGI.header+AdvCGI.errhtml)%(self.error))

    reshtml = """<html><head><title>
    Advanced Cgi Demo</title></head>
    <body><h2>Your Uploaded Data</h2>
    <h3>your cookie value is: <B>%s</B></h3>
    <h3>your name is: <B>%s</B></h3>
    <h3>you can program in the following languages:</h3>
    <ul>%s<ul>
    <h3>your uploaded file...<br>
    Name: <I>%s</I><br>
    Contents:</h3>
    <pre>%s</pre>
    Click <a href="%s"><B>here</B></a> to return to form
    </body></html>"""

    def setCPPCookies(self):
        for eachCookie in self.cookies.keys():
            print('Set-Cookie: CPP%s=%s; path=/' % \
                (eachCookie,parse.quote(self.cookies[eachCookie])))
    
    def doResults(self):
        MAXBYTES = 4096
        langlist = ''.join('<LI>%s<br>'% eachLang for eachLang in self.langs)
        filedata = self.fp.read(MAXBYTES)
        if len(filedata) == MAXBYTES and fp.read():
            filedata = '%s%s' % (filedata , '...<B><I>(file truncated due to size)</I></B>')
        self.fp.close()
        if filedata == b'':
            filedata ='<B><I>(file not given or upload error)</I></B>'
        filename = self.fn

        if not ('user' in self.cookies and self.cookies['user']):
            cookStatus = '<I>(cookie has not been set yet)</I>'
            userCook = ''
        else:
            userCook = cookStatus = self.cookies['user']

        self.cookies['info'] = ':'.join((self.who,','.join(self.langs),filename))
        self.setCPPCookies()

        print('%s%s' % (AdvCGI.header, AdvCGI.reshtml % (cookStatus, self.who, langlist, filename ,filedata , AdvCGI.url)))

    def go(self):
        self.cookies = {}
        self.error = ''
        form = FieldStorage()
        if not form.keys():
            self.showForm()
            return
        if 'person' in form:
            self.who = form['person'].value.strip().title()
            if self.who == '':
                self.error = 'Your name is required. (blank)'
        else:
            self.error = 'Your name is required. (missing)'

        self.cookies['user'] = parse.unquote(form['cookie'].value.strip()) if 'cookie' in form else ''
        if 'lang' in form:
            langData = form['lang']
            if isinstance(langData, list):
                self.langs = [eachLang.value for eachLang in langData]
            else:
                self.langs = [langData.value]
        else:
            self.error = 'At least one language required.'

        if 'upfile' in form:
            upfile = form['upfile']
            self.fn = upfile.filename or ''
            if upfile.file:
                self.fp = upfile.file
            else:
                self.fp = StringIO('(no data)')
        else:
            self.fp = StringIO('(no file)')
            self.fn = ''

        if not self.error:
            self.doResults()
        else:
            self.showError()

if __name__ == '__main__':
    page = AdvCGI()
    page.go()






