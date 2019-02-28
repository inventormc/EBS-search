import logging
import numpy as np

class Eigenval:
    def __init__(self, bs, fermi_level=None):
        #bs = mpr.get_bandstructure_by_material_id(mpid)
        self.k_points = []
        for k in bs.kpoints:
            self.k_points.append(k.frac_coords)
            #NOTE: Label shouldn't matter even if it's none
            #NOTE: Using fcoords for now
        self.nbands = bs.nb_bands
        #add logger.error
        #add subtraction for fermi level (pymatgen, if the argument is not none, have it override pymatgen)
        try:
            if fermi_level == None:
                self.spin_up = np.array(bs.as_dict()['bands']['1'])-bs.efermi
            else:
                self.spin_up = np.array(bs.as_dict()['bands']['1'])-fermi_level
        except KeyError:
            self.spin_up = [[]]
            logging.error('No spin up band found')

        try:
            if fermi_level == None:
                self.spin_down = np.array(bs.as_dict()['bands']['-1'])-bs.efermi
            else:
                self.spin_down = np.array(bs.as_dict()['bands']['-1'])-fermi_level
        except KeyError:
            self.spin_up = [[]]
            logging.error('No spin down band found')

class Doscar:
    def __init__(self,dos):
        #dos = mpr.get_dos_by_material_id(mpid)
        #NOTE: Assume calculations are converged
        self.converged = True
        self.fermi_energy = dos.efermi

# https://stackoverflow.com/a/312464
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

class Kpoints:
    def __init__(self, bs):
        #bs = mpr.get_bandstructure_by_material_id(mpid)
        self.k_points = []
        for k in bs.kpoints:
            name = k.label
            if name == "\Gamma":
                name = "Γ"
            if name == None:
                name = ""
            self.k_points.append((k.label,k.frac_coords)) #label can be none and are coords cartesian?
            #NOTE: Label shouldn't matter even if it's none
            #NOTE: Using fcoords for now
        #what is intersection? - Number of kpoints (see pymatgen doc)
        #are kpoints line mode?
        last_k = None
        self.segment_sizes=[]
        self.intersections = len(self.k_points)
        for segment in chunks(self.k_points,2):
            if np.array_equal(segment[0][1], last_k):
                self.segment_sizes[-1] += self.intersections
            else:
                self.segment_sizes.append(self.intersections)
            last_k = segment[1][1]


