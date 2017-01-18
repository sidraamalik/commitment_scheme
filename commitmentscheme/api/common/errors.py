class APIError(Exception):
    def __init__(self, message, status_code):
        self.status_code = status_code
        super(APIError, self).__init__(message)
