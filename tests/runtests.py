from engines.pil_test import pil_test_suite
from engines.pgmagick_test import pgmagick_test_suite
import unittest


def watermark_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(pil_test_suite())
    suite.addTest(pgmagick_test_suite())
    return suite


if __name__ == "__main__":
    unittest.main(defaultTest="watermark_test_suite")
