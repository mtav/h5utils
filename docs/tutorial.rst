========
Tutorial
========

.. Using h5tovts to visualize geometry defined in MPB:
.. ===================================================

This tutorial will show you how to use MPB to generate .h5 files, convert them to .vts and then view them using paraview.

Instructions for installing MPB can be found here: https://mpb.readthedocs.io/en/latest/Installation/

Paraview can be downloaded and installed from here: https://www.paraview.org/

.. note::
  You can also find the corresponding .h5 file in :download:`h5utils/data/lattice-non-cartesian-epsilon.h5 <../h5utils/data/lattice-non-cartesian-epsilon.h5>`.

Define the geometry
===================

Create (or download) :download:`lattice-visualization.ctl <../h5utils/data/lattice-visualization.ctl>` with the following contents:

.. `h5utils/data/lattice-visualization.ctl`

.. Example code::

.. .. literalinclude:: conf.py
..   :language: python
.. 
.. .. literalinclude:: ../setup.py
..   :language: python

.. literalinclude:: ../h5utils/data/lattice-visualization.ctl
  :language: scheme
..   .. include:: ../h5utils/data/lattice-visualization.ctl
