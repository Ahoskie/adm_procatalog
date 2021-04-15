class DatabaseException(Exception):
    """Causes when some suspicious operation is being applied to database."""
    def __init__(self, payload):
        self.message = self.get_message(payload)
        # logger.error(self.message) IMPLEMENT LOGGING LATER!
        super(DatabaseException, self).__init__(self.message)

    @staticmethod
    def get_message(payload):
        return f'Database operation error occurred. Payload: {payload}.'


class BucketNotFound(DatabaseException):
    def get_message(self, payload):
        return f'Bucket with name "{payload}" was not found. You may need to create it.'
