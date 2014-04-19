#!/usr/bin/env python
"""
Test importing sub-packages.

@author: Stephen Pascoe
"""

import unittest

class ImportTests(unittest.TestCase):

    def tryImport(self, moduleName):
        try:
            exec ("import %s" % moduleName) in globals()
        except:
            raise self.failureException

    def testCdms(self): self.tryImport('cdms2')
    def testCdtime(self): self.tryImport('cdtime')


