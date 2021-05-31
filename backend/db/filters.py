class BaseFilter:
    def get_query_condition(self):
        return ''


class FilterEquals(BaseFilter):
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def get_query_condition(self, bucket_query_name: str = 'b'):
        return f'{bucket_query_name}.{self.field} == "{self.value}" '


class FilterIn(BaseFilter):
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def get_query_condition(self, bucket_query_name: str = 'b'):
        return f'{bucket_query_name}.{self.field} IN {self.value} '


class FilterAny(BaseFilter):
    def __init__(self, array_field: str, value: list, check_field: str = ''):
        self.array_field = array_field
        self.check_field = check_field
        self.value = value

    def get_query_condition(self, bucket_query_name: str = 'b'):
        condition_string = f'ANY arr_el in {bucket_query_name}.{self.array_field} SATISFIES arr_el'
        if self.check_field != '':
            condition_string += f'.{self.check_field}'
        condition_string += f' IN {self.value} END '
        return condition_string
