import json

class MessageInfo:

    def __init__(self,errorno,msg,data):
        self.errorno = errorno              #0成功，非O失败。
        self.msg = msg
        self.data = data
    @staticmethod
    def success(msg='OK',data=''):
        msgInfo = MessageInfo(0,msg,data)
        return msgInfo

    @staticmethod
    def fail(errorCode=-1,data='FAIL'):
        msgInfo = MessageInfo(errorCode,data,"")
        return msgInfo



if __name__ == '__main__':
    print(json.dumps(MessageInfo.success().__dict__))