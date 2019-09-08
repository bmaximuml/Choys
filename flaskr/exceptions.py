class DistanceMatrixAPIError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidModeError(DistanceMatrixAPIError):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class RequestError(DistanceMatrixAPIError):
    def __init__(self, value, status_code):
        self.status_code = status_code
        self.value = value

    def __str__(self):
        return repr(self.value) + ': ' + self.status_code
