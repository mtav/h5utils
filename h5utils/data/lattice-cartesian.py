import meep as mp
from meep import mpb

ms = mpb.ModeSolver()

ms.init_params(p=mp.NO_PARITY, reset_fields=True)
ms.output_epsilon()
