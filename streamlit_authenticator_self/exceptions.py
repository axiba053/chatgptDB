class CredentialsError(Exception):
    """
    Exception raised for incorrect credentials.
    """
    def __init__(self):
        super().__init__('注册邮箱不正确！')

class ResetError(Exception):
    """
    Exceptions raised for the password reset widget.

    Attributes
    ----------
    message: str
        The custom error message to display.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class RegisterError(Exception):
    """
    Exceptions raised for the register user widget.

    Attributes
    ----------
    message: str
        The custom error message to display.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ForgotError(Exception):
    """
    Exceptions raised for the forgotten username/password widgets.

    Attributes
    ----------
    message: str
        The custom error message to display.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class UpdateError(Exception):
    """
    Exceptions raised for the update user details widget.

    Attributes
    ----------
    message: str
        The custom error message to display.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)