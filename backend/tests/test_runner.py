import unittest
from typing import Union
from tests import test_attributes, test_tags, test_brands, test_products

from tests.utils import initialize_database_for_test, remove_test_consequences


class CatalogTestRunner(unittest.TextTestRunner):
    def run(self, test: Union[unittest.suite.TestSuite, unittest.case.TestCase]) -> unittest.result.TestResult:
        print('Starting database initializing.')
        initialize_database_for_test()
        print('Database is initialized with start data.')
        results = super(CatalogTestRunner, self).run(test)
        print('Starting database flush.')
        remove_test_consequences()
        print('Database flush command executed.')
        return results


test_cases = [test_attributes.TestAttributes, test_tags.TestTags, test_brands.TestBrands, test_products.TestProducts]

test_load = unittest.TestLoader()

suites = []
for test_case in test_cases:
    suites.append(test_load.loadTestsFromTestCase(test_case))
suite = unittest.TestSuite(suites)

runner = CatalogTestRunner(verbosity=1)
runner.run(suite)
