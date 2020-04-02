from .ext import JsonSerializable

class ApiResponse(JsonSerializable):
    def __init__(self, code=None, msg=""):
        self.code = code
        self.msg = msg
    
    def json_serialize(self):
        print(self.__dict__)
        return self.__dict__

    @staticmethod
    def ok(data=None, msg="ok"):
        print("FUIUUUUUUUUK")
        print(data)
        print("FUIUUUUUUUUK")
        if data is not None:
            return DataApiResponse(code=200, msg=msg, data=data)

        return ApiResponse(code=200, msg=msg)

    @staticmethod
    def not_found(msg="not_found"):
        return ApiResponse(code=404, msg=msg)

    @staticmethod
    def bad_request(msg="bad_request"):
        return ApiResponse(code=400, msg=msg)

    @staticmethod
    def internal_error(msg="internal_error"):
        return ApiResponse(code=500, msg=msg)


class DataApiResponse(ApiResponse):
    def __init__(self, code=None, msg="", data=None):
        super().__init__(code, msg)
        self.data = data
