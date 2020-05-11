import threading
from time import sleep,ctime

loops=[4,2]
def loop(nloop,nsec):
    print("start loop",loop,"at:",ctime())
    sleep(nsec)
    print("start loop",loop,"at:",ctime())

def main():
    print("starting at",ctime())
    thread = []
    nloops = range(len(loops))

    for i in nloops:
        t = threading.Thread(target=loop,args=(i,loops[i]))
        thread.append(t)

    for i in nloops:
        thread[i].start()
    for i in nloops:
        thread[i].join()

    print("all done at",ctime())

if __name__ == '__main__':
    main()