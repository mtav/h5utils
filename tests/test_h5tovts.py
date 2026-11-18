#!/usr/bin/env python3
import glob
import os
import sys
import tempfile
import unittest

import h5py
import numpy
import vtk

import h5utils.h5tovts
import h5utils.h5utils


class test_h5tovts(unittest.TestCase):
    def test_conversion(self):
        """
        Runs h5tovts on all .h5 files in data.

        Each file is converted in its own subTest, and the test fails at the end
        with an OK/FAILED listing of all files if any conversion failed.
        To also see the listing when everything passes, run:
          pytest -k test_conversion -s
        """
        print("Testing h5tovts conversion:")
        d = os.path.join(os.path.dirname(h5utils.__file__), "data")
        files = sorted(glob.glob(os.path.join(d, "*.h5")))
        print(f"files: {files}")
        self.assertTrue(files, f"No .h5 files found in {d}")

        # Convert each file separately, so that one failing file does not stop
        # the others from being tested, and each gets its own pass/fail result.
        results = {}
        for h5file in files:
            name = os.path.basename(h5file)
            with self.subTest(name):
                try:
                    sys.argv = ["h5tovts", h5file]
                    h5utils.h5tovts.main()
                except BaseException:
                    results[name] = "FAILED"
                    raise
                results[name] = "OK"

        summary = "\n".join(f"  {status:6} {name}" for name, status in results.items())
        print(f"h5tovts conversion summary:\n{summary}")

        failed = [name for name, status in results.items() if status != "OK"]
        if failed:
            self.fail(
                f"h5tovts conversion failed for {len(failed)}/{len(results)} files:\n"
                f"{summary}"
            )

    def test_2D_conversion(self):
        """2D datasets (e.g. shape (Nx, Ny)) are converted as a single-layer 3D grid, see issue #1."""
        Nx, Ny = 21, 7
        ref = numpy.arange(Nx * Ny, dtype="f8").reshape(Nx, Ny)
        with tempfile.TemporaryDirectory() as tmpdir:
            h5file = os.path.join(tmpdir, "test2d.h5")
            with h5py.File(h5file, "w") as f:
                f.create_group("Time_1").create_dataset("Rho", data=ref)
            h5utils.h5tovts.h5tovts(
                h5utils.h5tovts.h5tovts_parse_args([h5file, "-d", "Time_1/Rho"])
            )
            for reader in (
                vtk.vtkXMLImageDataReader(),
                vtk.vtkXMLStructuredGridReader(),
            ):
                reader.SetFileName(
                    os.path.join(
                        tmpdir,
                        "test2d."
                        + ("vti" if "Image" in reader.GetClassName() else "vts"),
                    )
                )
                reader.Update()
                out = reader.GetOutput()
                self.assertEqual(out.GetNumberOfPoints(), Nx * Ny)
                from vtk.util.numpy_support import vtk_to_numpy

                data = vtk_to_numpy(out.GetPointData().GetArray("Time_1/Rho"))
                self.assertTrue(numpy.allclose(data.reshape(Ny, Nx).T, ref))

    def test_readString_storage_types(self):
        """h5_readString must handle fixed-length and variable-length scalar strings."""
        cases = {
            "fixed_numpy_bytes": (numpy.bytes_("fixed len\0\0\0"), "fixed len"),
            "fixed_S20": (numpy.array(b"fixed2", dtype="S20"), "fixed2"),
            "vlen_utf8": (
                "vlen unicode",
                "vlen unicode",
                h5py.string_dtype("utf-8"),
            ),
            "vlen_ascii": (
                b"dielectric function, epsilon",
                "dielectric function, epsilon",
                h5py.string_dtype("ascii"),
            ),
            # Non-ASCII byte must not raise (this was the original crash).
            "vlen_ascii_nonascii": (
                b"\xb0 degrees",
                "\ufffd degrees",
                h5py.string_dtype("ascii"),
            ),
        }
        with (
            tempfile.TemporaryDirectory() as tmpdir,
            h5py.File(os.path.join(tmpdir, "strings.h5"), "w") as f,
        ):
            for name, case in cases.items():
                data, expected = case[0], case[1]
                dtype = case[2] if len(case) > 2 else None
                f.create_dataset(name, data=data, dtype=dtype)
                with self.subTest(name):
                    self.assertEqual(h5utils.h5utils.h5_readString(f[name]), expected)

    def test_variable_length_description(self):
        """Regression: MPB-style file with a variable-length 'description' dataset
        used to fail with UnicodeDecodeError in h5_setupLattice."""
        N = 4
        ref = numpy.arange(N**3, dtype="f8").reshape(N, N, N)
        with tempfile.TemporaryDirectory() as tmpdir:
            h5file = os.path.join(tmpdir, "vlen_desc.h5")
            with h5py.File(h5file, "w") as f:
                f.create_dataset(
                    "description",
                    data=b"dielectric function, epsilon",
                    dtype=h5py.string_dtype("ascii"),
                )
                f.create_dataset("lattice vectors", data=numpy.eye(3))
                f.create_dataset("data", data=ref)
            h5utils.h5tovts.h5tovts(h5utils.h5tovts.h5tovts_parse_args([h5file]))
            self.assertTrue(os.path.isfile(os.path.join(tmpdir, "vlen_desc.vts")))
            self.assertTrue(os.path.isfile(os.path.join(tmpdir, "vlen_desc.vti")))

    def test_listing(self):
        print("Testing h5tovts listing:")
        d = os.path.join(os.path.dirname(h5utils.__file__), "data")
        f = os.listdir(d)
        f = glob.glob(os.path.join(d, "*.h5"))
        print(f"f: {f}")
        sys.argv = ["h5tovts", "--list"] + f
        h5utils.h5tovts.main()


if __name__ == "__main__":
    print("===direct execution===")
    unittest.main()
