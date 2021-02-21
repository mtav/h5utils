========
Tutorial
========

This tutorial will show you how to use MPB to generate .h5 files, convert them to .vts and then view them using paraview.

Instructions for installing MPB can be found here: https://mpb.readthedocs.io/en/latest/Installation/

Paraview can be downloaded and installed from here: https://www.paraview.org/

.. If you want to do a quick test without installing MPB, skip ahead to the end of :ref:`this section <generateHDF5>`.

If you want to do a quick test without installing MPB, skip ahead to :ref:`here <hdf5-download-label>`.

Define the geometry
===================

Create (or download) :download:`lattice-non-cartesian.ctl <../h5utils/data/lattice-non-cartesian.ctl>` with the following contents:

.. literalinclude:: ../h5utils/data/lattice-non-cartesian.ctl
  :language: scheme

The first part defines a lattice with the following basis vectors:

* :math:`\vec{a_1} = \frac{1}{2}[0,2,3]`
* :math:`\vec{a_2} = \frac{1}{2}[1,0,3]`
* :math:`\vec{a_3} = \frac{1}{2}[1,2,0]`

The second part defines a geometry made of cylinders along the edges of the unit-cell. Since MPB simulates periodic structures, only 3 cylinders are needed to visualize all 12 edges of the unit-cell.

The cylinders all have different permittivity values in order to distinguish them more easily later on.

The expected geometry should look as in this picture:

.. image:: /images/non-cartesian-design-annotated.png
   :scale: 50 %
   :alt: annotated non-cartesian design
   :align: center

.. _generateHDF5:

Generate the HDF5 files by running MPB
======================================

.. code:: bash

        mpb ./lattice-non-cartesian.ctl

This should generate a `./lattice-non-cartesian-epsilon.h5` file:

.. code:: bash

        ls ./lattice-non-cartesian-epsilon.h5

.. _hdf5-download-label:

.. note::
  If you do not have MPB available, you can simply download the corresponding .h5 file here: :download:`h5utils/data/lattice-non-cartesian-epsilon.h5 <../h5utils/data/lattice-non-cartesian-epsilon.h5>`.

Convert the HDF5 file to a VTS file
====================================
.. code:: bash

        h5tovts ./lattice-non-cartesian-epsilon.h5

This should generate a `./lattice-non-cartesian-epsilon.vts` file:

.. code:: bash

        ls ./lattice-non-cartesian-epsilon.vts

View the VTS file in Paraview
=============================

Open the VTS file in Paraview and then:

1. Click apply.
2. Select "Volume" rendering.
3. Activate the colorbar.
4. Enable Axes Grid

See picture below for reference:

.. image:: /images/paraview.1.annotated.png
   :scale: 50 %
   :align: center

Alternatively, you could add threshold filters for permittivity ranges corresponding to the values used (2, 3 and 4) and choose red, green and blue colors to render the geometry like this:

.. image:: /images/non-cartesian-colored.cropped.png
   :scale: 100 %
   :align: center

You can try out those settings more easily using this saved state file: :download:`h5utils/data/lattice-visualization-non-cartesian.pvsm <../h5utils/data/lattice-visualization-non-cartesian.pvsm>`.
