import json

class MessageInfo:

    def __init__(self,error,reason,data):
        self.error = error
        self.reason = reason
        self.data = data                #0出错，非O不出错
    @staticmethod
    def success(msg='OK',data=''):
        msgInfo = MessageInfo(200,msg,data)
        return msgInfo
    @staticmethod
    def fail(errorCode=0,data='FAIL'):
        msgInfo = MessageInfo(errorCode,data,"")
        return msgInfo


if __name__ == '__main__':
    print(json.dumps(MessageInfo.success().__dict__))