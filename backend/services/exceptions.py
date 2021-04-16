from db.exceptions import DatabaseException


class DocumentAlreadyExists(DatabaseException):
    def get_message(self, document):
        return f'Document \'{document}\' already exists.'


class DocumentNotFound(DatabaseException):
    def get_message(self, document):
        return f'Document \'{document}\' was not found.'


class InvalidVariantAttribute(DatabaseException):
    def get_message(self, attribute):
        available_attrs = []
        if 'available_attrs' in self.kwargs:
            available_attrs = self.kwargs['available_attrs']
        return f'Attribute \'{attribute}\' can not be set to this product. Available are: \'{available_attrs}\'.'
