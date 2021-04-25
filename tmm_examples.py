from __future__ import division, print_function, absolute_import
from numpy import pi, linspace, inf, array
from tmm_core_functions import (coh_tmm, position_resolved, find_in_structure_with_inf)
import matplotlib.pyplot as plt

d_list = [inf, 100, 300, inf]  # in nm
n_list = [1, 2.2 + 0.2j, 3.3 + 0.3j, 1]
th_0 = pi / 4
lam_vac = 400
pol = 'p'
coh_tmm_data = coh_tmm(pol, n_list, d_list, th_0, lam_vac)
ds = linspace(-50, 400, num=1000)  # position in structure
poyn = []
absor = []
for d in ds:
    layer, d_in_layer = find_in_structure_with_inf(d_list, d)
    data = position_resolved(layer, d_in_layer, coh_tmm_data)
    poyn.append(data['poyn'])
    absor.append(data['absor'])
# convert data to numpy arrays for easy scaling in the plot
poyn = array(poyn)
absor = array(absor)
plt.figure()
plt.plot(ds, poyn, 'blue', ds, 200 * absor, 'purple')
plt.xlabel('depth (nm)')
plt.ylabel('AU')
plt.title('Local absorption (purple), Poynting vector (blue)')
plt.show()
