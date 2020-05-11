from twisted.internet import protocol,reactor

DEFAULT_HOST= '172.18.111.179'
DEFAULT_PORT = 21567

HOST = input("请输入服务器IP:")
PORT = input("请输入端口号:")

if not HOST or not PORT:
    HOST = DEFAULT_HOST
    PORT = DEFAULT_PORT

class TSClntProtocol(protocol.Protocol):
    def sendData(self):
        data = input(">")
        if data:
            print("sending %s..."%data)
            self.transport.write(bytes(data,encoding='utf-8'))
        else:
            self.transport.loseConnection()

    def connectionMade(self):
        self.sendData()

    def dataReceived(self,data):
        print(data)
        self.sendData()
class TSClntFactory(protocol.ClientFactory):
    protocol = TSClntProtocol
    clientConnectionLost = clientConnectionFailed = lambda self,connector,reason:reactor.stop()

reactor.connectTCP(HOST,PORT,TSClntFactory())
reactor.run()