import unittest
from mock import patch, MagicMock
from soktest.base import TestCase, TestCaseType
from soktest.error import NameAlreadyExists


class TestCaseTypeTests(unittest.TestCase):

    @patch('soktest.base.TestCase')
    def test_assign_groups_new(self, TestCaseMock):
        class Test1(TestCase):
            groups = ['one', 'two']

        TestCaseMock._alltests_groups = {}
        TestCaseType.assign_groups(Test1)

        self.assertEqual({
            'one': [Test1, ],
            'two': [Test1, ],
        }, TestCaseMock._alltests_groups)

    @patch('soktest.base.TestCase')
    def test_assign_groups_existing(self, TestCaseMock):
        class Test2(TestCase):
            groups = ['one', 'two']

        TestCaseMock._alltests_groups = {
            'one': [1, ]
        }
        TestCaseType.assign_groups(Test2)

        self.assertEqual({
            'one': [1, Test2, ],
            'two': [Test2, ],
        }, TestCaseMock._alltests_groups)

    @patch('soktest.base.TestCase')
    def test_validate_name_success(self, TestCaseMock):
        TestCaseMock._alltests_dict = {}

        TestCaseType.validate_name('module.cls')

    @patch('soktest.base.TestCase')
    def test_validate_name_name_already_exists(self, TestCaseMock):
        TestCaseMock._alltests_dict = {
            'module.cls': None,
        }

        self.assertRaises(
            NameAlreadyExists, TestCaseType.validate_name, 'module.cls')

    @patch('soktest.base.TestCase')
    def test_add_test_to_alltests(self, TestCaseMock):
        TestCaseMock._alltests_dict = {}

        TestCaseType.add_test_to_alltests('name1', 2)
        self.assertEqual({'name1': 2}, TestCaseMock._alltests_dict)

    @patch('soktest.base.TestCase')
    def test_add_test_to_alltests_name_already_exists(self, TestCaseMock):
        TestCaseMock._alltests_dict = {
            'name2': 3,
        }

        TestCaseType.add_test_to_alltests('name2', 4)
        self.assertEqual({'name2': None}, TestCaseMock._alltests_dict)

    def test_get_full_name(self):
        dct = {
            '__module__': 'elo.module',
        }
        result = TestCaseType.get_full_name(dct, 'name3')
        self.assertEqual('elo.module.name3', result)

    @patch('soktest.base.TestCase')
    def test_create_without_base(self, TestCaseMock):
        TestCaseMock._alltests = []
        TestCaseMock._alltests_dict = {}
        TestCaseMock._alltests_groups = {}
        test = MagicMock()
        test.groups = ['unittest']

        TestCaseType.init_task(test, 'name4', {'__module__': 'module4'})

        self.assertEqual([test], TestCaseMock._alltests)
        self.assertEqual({
            'name4': test,
            'module4.name4': test
        }, TestCaseMock._alltests_dict)
        self.assertEqual(
            {'unittest': [test, ]}, TestCaseMock._alltests_groups)

    @patch('soktest.base.TestCase')
    def test_create_with_base_false(self, TestCaseMock):
        TestCaseMock._alltests = []
        TestCaseMock._alltests_dict = {}
        TestCaseMock._alltests_groups = {}
        test = MagicMock()
        test.groups = ['unittest']

        TestCaseType.init_task(
            test, 'name5', {'__module__': 'module5', 'base': False})

        self.assertEqual([test], TestCaseMock._alltests)
        self.assertEqual({
            'name5': test,
            'module5.name5': test
        }, TestCaseMock._alltests_dict)
        self.assertEqual(
            {'unittest': [test, ]}, TestCaseMock._alltests_groups)

    @patch('soktest.base.TestCase')
    def test_create_with_base_true(self, TestCaseMock):
        TestCaseMock._alltests = []
        TestCaseMock._alltests_dict = {}
        TestCaseMock._alltests_groups = {}
        test = MagicMock()
        test.groups = ['unittest']

        TestCaseType.init_task(
            test, 'name6', {'__module__': 'module6', 'base': True})

        self.assertEqual([], TestCaseMock._alltests)
        self.assertEqual({}, TestCaseMock._alltests_dict)
        self.assertEqual({}, TestCaseMock._alltests_groups)


class TestCaseTest(unittest.TestCase):

    def test_class_vars(self):
        self.assertEqual([], TestCase._alltests)
        self.assertEqual({}, TestCase._alltests_dict)
        self.assertEqual({}, TestCase._alltests_groups)
        self.assertEqual(True, TestCase.base)
        self.assertEqual(('unit',), TestCase.groups)
