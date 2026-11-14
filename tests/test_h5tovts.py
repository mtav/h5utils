#!/usr/bin/env python3
import os
import sys
import glob
import unittest
import tempfile
import numpy
import h5py
import vtk
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
    def test_2D_conversion(self):
      '''2D datasets (e.g. shape (Nx, Ny)) are converted as a single-layer 3D grid, see issue #1.'''
      Nx, Ny = 21, 7
      ref = numpy.arange(Nx*Ny, dtype='f8').reshape(Nx, Ny)
      with tempfile.TemporaryDirectory() as tmpdir:
        h5file = os.path.join(tmpdir, 'test2d.h5')
        with h5py.File(h5file, 'w') as f:
          f.create_group('Time_1').create_dataset('Rho', data=ref)
        h5utils.h5tovts.h5tovts(h5utils.h5tovts.h5tovts_parse_args([h5file, '-d', 'Time_1/Rho']))
        for reader in (vtk.vtkXMLImageDataReader(), vtk.vtkXMLStructuredGridReader()):
          reader.SetFileName(os.path.join(tmpdir, 'test2d.' + ('vti' if 'Image' in reader.GetClassName() else 'vts')))
          reader.Update()
          out = reader.GetOutput()
          self.assertEqual(out.GetNumberOfPoints(), Nx*Ny)
          from vtk.util.numpy_support import vtk_to_numpy
          data = vtk_to_numpy(out.GetPointData().GetArray('Time_1/Rho'))
          self.assertTrue(numpy.allclose(data.reshape(Ny, Nx).T, ref))
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
