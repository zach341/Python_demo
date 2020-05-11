import threading
from time import sleep,ctime

loops=[2,4]

class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name
        self.result = self.func(*self.args) 

    def getResult(self):
        return self.result
    def run(self):
        print("Starting ",self.name,"at:",ctime())
        self.result = self.func(*self.args)
        print(self.name,"finish at",ctime())

def loop(nloops,nsec):
    print("starting loop",nloops,"at:",ctime())
    sleep(nsec)
    print("starting loop",nloops,"at:",ctime())
    return '666'

def main():
    print("starting at",ctime())
    threads=[]
    nloops=range(len(loops))

    for i in nloops:
        t = MyThread(loop,(i,loops[i]),loop.__name__)
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()
        print(threads[i].getResult())

    print("all done at",ctime())

if __name__=="__main__":
    main()


