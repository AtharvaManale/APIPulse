class AuthException(Exception):
    status_code = 400

    def __init__(self, message):
        self.message = message
        super().__init__(message)

class ExistingUserException(AuthException):
    status_code=409

    def __init__(self):
        super().__init__(
            "User Already Exists, Use Different Username."
        )

class ExistingEmailException(AuthException):
    status_code=409

    def __init__(self):
        super().__init__(
            "Email Already Used, Use Different Email."
        )

class UserNotFoundException(AuthException):
    status_code=404

    def __init__(self):
        super().__init__(
            "No Such User Exists."
        )
        
class UserNotAuthenticatedException(AuthException):
    status_code=401
    def __init__(self):
            super().__init__(
                "Invalid Credentials. Try Again."
            )

class InvalidTokenException(AuthException):
    status_code=401
    def __init__(self):
                super().__init__(
                    "Invalid Auth Bearer Token."
            )