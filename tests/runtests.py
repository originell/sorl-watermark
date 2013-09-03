from engines import pil_test, pgmagick_test
import unittest


def suite():
    suite = unittest.TestSuite()
    suite.addTest(pil_test.suite())
    suite.addTest(pgmagick_test.suite())
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')



