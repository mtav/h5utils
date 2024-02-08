import math
import meep as mp
from meep import mpb

num_bands = 1
resolution = 32
geometry_lattice = mp.Lattice(size=mp.Vector3(1, 1, 1),
                              basis1=mp.Vector3(math.sqrt(3)/2, 0.5),
                              basis2=mp.Vector3(math.sqrt(3)/2, -0.5),
                              basis3=mp.Vector3(0,0,1))
geometry = [mp.Cylinder(0.2, material=mp.Medium(epsilon=12))]

k_points = []

ms = mpb.ModeSolver(
    geometry=geometry,
    geometry_lattice=geometry_lattice,
    k_points=k_points,
    resolution=resolution,
    num_bands=num_bands
)

ms.init_params(p=mp.NO_PARITY, reset_fields=True)
ms.output_epsilon()
