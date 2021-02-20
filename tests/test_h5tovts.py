#!/usr/bin/env python3
import os
import sys
import glob
import unittest
import h5utils.h5tovts

class test_h5tovts(unittest.TestCase):
    def test_conversion(self):
      print('Testing h5tovts conversion:')
      d = os.path.join(os.path.dirname(h5utils.__file__), 'data')
      f = os.listdir(d)
      f = glob.glob(os.path.join(d,'*.h5'))
      print(f'f: {f}')
      sys.argv = ['h5tovts']+f
      h5utils.h5tovts.main()
    def test_listing(self):
      print('Testing h5tovts listing:')
      d = os.path.join(os.path.dirname(h5utils.__file__), 'data')
      f = os.listdir(d)
      f = glob.glob(os.path.join(d,'*.h5'))
      print(f'f: {f}')
      sys.argv = ['h5tovts', '--list']+f
      h5utils.h5tovts.main()

if __name__ == '__main__':
  print('===direct execution===')
  unittest.main()
