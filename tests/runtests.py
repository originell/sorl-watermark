# coding: utf-8
# author: v.bazhin@gmail.com

import unittest



from engines import pil_test, pgmagick_test

def suite():
    suite = unittest.TestSuite()
    suite.addTest(pil_test.suite())
    suite.addTest(pgmagick_test.suite())
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')



