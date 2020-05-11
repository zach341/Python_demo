from ftplib import FTP

fp =open(r"C:\Users\zach.zhang\Desktop\Dial\testzc.zip",'rb')

buffer_size = 8096
ftp = FTP()
x = ftp.connect('172.18.113.212',21)
print(x)
login = ftp.login('test','test')
print(login)
y = ftp.cwd('/zach/')
print(y)
z =ftp.nlst()
print(z)
res = ftp.storbinary('STOR' + '/zach/testzc.zip',fp,buffer_size)
fp.close()