class ArgumentFormatException(Exception):
    def __init__(self, message):
        self.message = message


class SessionDontExistException(Exception):
    def __init__(self):
        self.message = 'You are trying to access controls of non-existing terminal'
