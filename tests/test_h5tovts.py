#!/usr/bin/env python3
import unittest

import h5utils.h5tovts

class test_h5tovts(unittest.TestCase):
    def test_is_string(self):
      print('Testing h5tovts')
      import os
      import sys
      import glob
      d = os.path.join(os.path.dirname(h5utils.__file__), 'data')
      f = os.listdir(d)
      f = glob.glob(os.path.join(d,'*.h5'))
      print(f'f: {f}')
      sys.argv = ['h5tovts']+f
      h5utils.h5tovts.main()

if __name__ == '__main__':
  print('===direct execution===')
  unittest.main()
