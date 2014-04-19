#!/usr/bin/env python
# Adapted for numpy/ma/cdms2 by convertcdms.py
"""
Test reading data with cdms.

@author: Stephen Pascoe
"""

import os
import unittest, pkg_resources, cdms2 as cdms, sys

here = os.path.dirname(__file__)

class CdmsTests(unittest.TestCase):

    def testNetCDF(self):
        f = os.path.join(os.path.dirname(here), 'tas_mo_clim.nc')
        d = cdms.open(f)
        vars = d.listvariables()
        vars.sort()
        self.assert_(vars == ['bounds_latitude', 'bounds_longitude', 'climseas'])

