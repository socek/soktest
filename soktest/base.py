import unittest


class TestCaseType(type):

    def __init__(cls, name, bases, dct):
        super(TestCaseType, cls).__init__(name, bases, dct)
        fullname = '.'.join([str(dct['__module__']), name])
        if 'base' not in dct or dct['base'] == False:
            keys = TestCase.alltests_dict.keys()
            if fullname in keys:
                raise RuntimeError(
                    'Name "%s" defined more the once.' % (name,))
            if name in keys:
                TestCase.alltests_dict[name] = None
            else:
                TestCase.alltests_dict[name] = cls
            TestCase.alltests.append(cls)
            TestCase.alltests_dict[fullname] = cls


class TestCase(unittest.TestCase):

    __metaclass__ = TestCaseType
    base = True
    alltests = []
    alltests_dict = {}
