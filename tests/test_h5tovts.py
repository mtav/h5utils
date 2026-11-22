#!/usr/bin/env python3
import contextlib
import glob
import io
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

    def test_getDataSets_skips_metadata(self):
        """Metadata (incl. 1D 'Bloch wavevector') must not be treated as field data."""
        with (
            tempfile.TemporaryDirectory() as tmpdir,
            h5py.File(os.path.join(tmpdir, "meta.h5"), "w") as f,
        ):
            f.create_dataset("Bloch wavevector", data=numpy.array([-1 / 3, 1 / 3, 0.0]))
            f.create_dataset("description", data=numpy.bytes_("e field"))
            f.create_dataset("lattice vectors", data=numpy.eye(3))
            f.create_dataset("some 1D metadata", data=numpy.arange(5.0))
            f.create_dataset("z.i", data=numpy.zeros((4, 4)))
            f.create_dataset("z.r", data=numpy.zeros((4, 4)))
            f.create_dataset("data", data=numpy.zeros((4, 4, 4)))
            self.assertEqual(
                sorted(h5utils.h5utils.h5_getDataSets(f)), ["data", "z.i", "z.r"]
            )

    def test_MPB_2D_field_with_bloch_wavevector(self):
        """Regression: MPB 2D field files (e.g. tri-rods-e.k11.b01.z.tm.h5) contain a
        'Bloch wavevector' dataset of shape (3,) which was used to determine the grid size."""
        N = 8
        zr = numpy.arange(N * N, dtype="f8").reshape(N, N)
        with tempfile.TemporaryDirectory() as tmpdir:
            h5file = os.path.join(tmpdir, "mpb2d.h5")
            with h5py.File(h5file, "w") as f:
                f.create_dataset("Bloch wavevector", data=[-1 / 3, 1 / 3, 0.0])
                f.create_dataset("description", data=numpy.bytes_("e field, kpoint 11"))
                f.create_dataset(
                    "lattice vectors",
                    data=[[0.8660254, 0.5, 0], [0.8660254, -0.5, 0], [0, 0, 1]],
                )
                f.create_dataset("z.r", data=zr)
                f.create_dataset("z.i", data=-zr)
            h5utils.h5tovts.h5tovts(h5utils.h5tovts.h5tovts_parse_args([h5file]))
            reader = vtk.vtkXMLStructuredGridReader()
            reader.SetFileName(os.path.join(tmpdir, "mpb2d.vts"))
            reader.Update()
            out = reader.GetOutput()
            self.assertEqual(out.GetNumberOfPoints(), N * N)
            pd = out.GetPointData()
            names = sorted(pd.GetArrayName(i) for i in range(pd.GetNumberOfArrays()))
            self.assertEqual(names, ["z.i", "z.r"])
            from vtk.util.numpy_support import vtk_to_numpy

            for name, expected in (("z.r", zr), ("z.i", -zr)):
                with self.subTest(name):
                    self.assertTrue(
                        numpy.allclose(
                            vtk_to_numpy(pd.GetArray(name)).reshape(N, N).T, expected
                        )
                    )

    @staticmethod
    def _convert_and_read(h5file, extra_args=()):
        """Convert h5file and return (stdout, {ext: (npoints, {array name: ntuples})})."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            h5utils.h5tovts.h5tovts(
                h5utils.h5tovts.h5tovts_parse_args([h5file, *extra_args])
            )
        result = {}
        for ext, reader in (
            ("vts", vtk.vtkXMLStructuredGridReader()),
            ("vti", vtk.vtkXMLImageDataReader()),
        ):
            reader.SetFileName(os.path.splitext(h5file)[0] + "." + ext)
            reader.Update()
            grid = reader.GetOutput()
            pd = grid.GetPointData()
            arrays = {
                pd.GetArrayName(i): pd.GetArray(i).GetNumberOfTuples()
                for i in range(pd.GetNumberOfArrays())
            }
            result[ext] = (grid.GetNumberOfPoints(), arrays)
        return out.getvalue(), result

    def test_mismatching_shapes_skipped(self):
        """The first dataset defines the grid. Datasets of a different shape are skipped
        with a message instead of producing truncated or invalid VTK files."""
        cases = {
            # name: ({dataset: shape}, expected points, expected datasets, skipped dataset)
            "2D_first": ({"a_2d": (4, 4), "b_3d": (4, 4, 3)}, 16, ["a_2d"], "b_3d"),
            "3D_first": ({"a_3d": (4, 4, 3), "b_2d": (4, 4)}, 48, ["a_3d"], "b_2d"),
            "both_3D": ({"a": (4, 4, 3), "b": (5, 4, 3)}, 48, ["a"], "b"),
        }
        for case, (datasets, npoints, expected, skipped) in cases.items():
            with self.subTest(case), tempfile.TemporaryDirectory() as tmpdir:
                h5file = os.path.join(tmpdir, "mixed.h5")
                with h5py.File(h5file, "w") as f:
                    for name, shape in datasets.items():
                        f.create_dataset(name, data=numpy.zeros(shape))
                stdout, result = self._convert_and_read(h5file)
                self.assertIn(f"Skipping {skipped}", stdout)
                for ext in ("vts", "vti"):
                    self.assertEqual(
                        result[ext], (npoints, dict.fromkeys(expected, npoints))
                    )

    def test_2D_and_single_layer_3D_compatible(self):
        """A 2D dataset (Nx, Ny) and a 3D dataset (Nx, Ny, 1) describe the same grid."""
        with tempfile.TemporaryDirectory() as tmpdir:
            h5file = os.path.join(tmpdir, "compatible.h5")
            with h5py.File(h5file, "w") as f:
                f.create_dataset("a_2d", data=numpy.zeros((4, 3)))
                f.create_dataset("b_3d", data=numpy.zeros((4, 3, 1)))
            stdout, result = self._convert_and_read(h5file)
            self.assertNotIn("Skipping", stdout)
            for ext in ("vts", "vti"):
                self.assertEqual(result[ext], (12, {"a_2d": 12, "b_3d": 12}))

    def test_requested_mismatching_shapes_raise(self):
        """Explicitly requested datasets with different shapes are an error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            h5file = os.path.join(tmpdir, "requested.h5")
            with h5py.File(h5file, "w") as f:
                f.create_dataset("a_2d", data=numpy.zeros((4, 4)))
                f.create_dataset("b_3d", data=numpy.zeros((4, 4, 3)))
            args = h5utils.h5tovts.h5tovts_parse_args([h5file, "-d", "a_2d", "b_3d"])
            with self.assertRaisesRegex(ValueError, "b_3d.*does not match"):
                h5utils.h5tovts.h5tovts(args)

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
