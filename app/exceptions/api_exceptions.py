class APIException(Exception):
    status_code = 400
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class UserNotAuthorizedException(APIException):
    status_code=403
    
    def __init__(self):
        super().__init__(
            "User not authorized to access other users Api endpoints."
        )

class APINotFoundException(APIException):
    status_code=404

    def __init__(self):
        super().__init__(
            "No Such API endpoint Exists."
        )

class ExistingEndpointException(APIException):
    status_code = 409

    def __init__(self):
        super().__init__(
            "This API endpoint is already registered."
        )


class NoAPIRegisteredException(APIException):
    status_code = 204

    def __init__(self):
        super().__init__(
            "No API registered by the user."
        )