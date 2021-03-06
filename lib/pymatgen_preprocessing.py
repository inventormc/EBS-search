import numpy as np
import pymatgen

def path_1D(k):
    """
    Fold out path in 3D along a 1D line by taking the norm between each set of points.
    """
    norm_path = [0]
    for i in range(len(k)-1):
        norm_path.append(np.linalg.norm(k[i+1]-k[i]))
    return np.cumsum(norm_path)


def interpolate(x, line, dimensions):
    """
    Interpolate so that we have the number of dimensions if there are too few points.
    """
    if len(x) != dimensions:
        new_x = np.linspace(np.min(x), np.max(x), dimensions)
        line = np.interp(new_x, x, line)
    return line


def interpolate_normalize(k, E, dimensions):
    """
    First interpolate (see interpolate). Next, subtract the mean and normalize a single band.
    """
    E_interp = interpolate(k, E, dimensions)
    E_interp = E_interp - E_interp.mean()
    if np.linalg.norm(E_interp) > 1e-5:
        E_interp = E_interp / np.linalg.norm(E_interp)
    return E_interp

from lib import pymatgen
from pymatgen import MPRester
import matplotlib.pyplot as plt

def plot_band_structure(mpid, band_index, width, k_highlight, pattern):
    """
    - Plots two bands (which one is indicated by band_index)
    - Highlights a window of width `width` at k `k_highlight`
    """
    mpr = MPRester('4JzM8sNnMkyVJceK')
    bs = mpr.get_bandstructure_by_material_id(mpid)
    dos = mpr.get_dos_by_material_id(mpid)

    kpoints = pymatgen.Kpoints(bs)
    doscar = pymatgen.Doscar(dos)
    fermi_energy = doscar.fermi_energy
    eigenval = pymatgen.Eigenval(bs, fermi_energy)

    bands = eigenval.spin_up
    lower_fermi_band_index = np.argmax(np.nanmax(bands,axis=1) > 0) - 1

    """
    segment_sizes = kpoints.segment_sizes
    segmented_lower_band = np.split(bands[lower_fermi_band_index+band_index], np.cumsum(segment_sizes))[:-1]
    segmented_upper_band = np.split(bands[lower_fermi_band_index+band_index+1], np.cumsum(segment_sizes))[:-1]
    segmented_kpoints = np.split(eigenval.k_points, np.cumsum(segment_sizes))[:-1]

    last_k = 0
    """

    k = eigenval.k_points
    band_l = bands[lower_fermi_band_index+band_index]
    band_u = bands[lower_fermi_band_index+band_index+1]
    #for k, band_l, band_u in zip(segmented_kpoints, segmented_lower_band, segmented_upper_band):
    #k_1D = np.array(path_1D(k)) + last_k
    k_1D = np.array(path_1D(k))
    plt.plot(k_1D, band_l, 'k')
    plt.plot(k_1D, band_u, 'k')
    #last_k = np.max(k_1D)
    plt.axvspan(float(k_highlight), float(k_highlight)+width, color='red', alpha=0.5)
    # Collect axis ticks (high symmetry points) from KPOINTS.gz
    last_k = 0
    label_k = []
    label_names = []

    #NOTE: Labels for none are question marks
    for left_k, right_k in pymatgen.chunks(kpoints.k_points, 2):
        if len(label_names) == 0:
            label_k.append(last_k)
            #label_names.append(left_k[0])
        #elif label_names[-1] != left_k[0]:
            #label_names[-1] += (';' + left_k[0])
        last_k += np.linalg.norm(right_k[1] - left_k[1])
        label_k.append(last_k)
        #label_names.append(right_k[0])

    #plt.xticks(label_k, label_names)
    #plt.xticks(label_k)

    plt.ylabel('Energy')
    plt.xlabel('k')
    plt.grid(True)
    plt.title('material ' + mpid)
    plt.savefig('misc/'+pattern+'_search_result.png')
    plt.show()
