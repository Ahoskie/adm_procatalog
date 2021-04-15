from db.exceptions import DatabaseException


class DocumentAlreadyExists(DatabaseException):
    def get_message(self, document):
        return f'Document \'{document}\' already exists.'


class DocumentNotFound(DatabaseException):
    def get_message(self, document):
        return f'Document \'{document}\' was not found.'
