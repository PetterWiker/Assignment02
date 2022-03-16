import laminatelib
import copy


class Laminate:

    def __init__(self, layup, name, width, damage_allowed=False, damage_reduction_factor=0.1):
        self.is_broken = False
        self.layup = layup
        self.name = name
        self.width = width
        self.damage_allowed = damage_allowed
        self.damage_reduction_factor = damage_reduction_factor
        self.thickness = laminatelib.laminateThickness(self.layup)
        self.A = laminatelib.computeA(self.layup)
        self.B = laminatelib.computeB(self.layup)
        self.D = laminatelib.computeD(self.layup)
        self.ABD = laminatelib.laminateStiffnessMatrix(self.layup)
        self.loads, self.defor = [], []
        self.EI = self.compute_bending_stiffness()

        self.kappa_x = 0
        self.displacement = 0
        self.damage_state = ["active" for layer in self.layup]
        pass

    def update_state(self, **kwargs):
        self.loads, self.defor = laminatelib.solveLaminateLoadCase(self.ABD, **kwargs)
        pass

    def check_ply_stress_states(self):

        # Go through the layers, check for damage
        layer_results = laminatelib.layerResults(self.layup, self.defor)
        for idx, layer in enumerate(self.layup):
            layer_state = layer_results[idx]
            if (layer_state["fail"]["MS"]["top"] > 1 or layer_state["fail"]["MS"]["bot"] > 1) and self.damage_allowed:
                self.damage_state[idx] = "broken"
                old_material = layer["mat"]
                updated_material = copy.deepcopy(layer["mat"])
                updated_material["E1"] = old_material["E1"]*self.damage_reduction_factor
                updated_material["E2"] = old_material["E2"]*self.damage_reduction_factor
                updated_material["E3"] = old_material["E3"]*self.damage_reduction_factor
                layer["mat"] = updated_material

                # Recalculate the stiffness matrices
                self.A = laminatelib.computeA(self.layup)
                self.B = laminatelib.computeB(self.layup)
                self.D = laminatelib.computeD(self.layup)
                self.ABD = laminatelib.laminateStiffnessMatrix(self.layup)

                # ...and recalculate the bending stiffness
                self.EI = self.compute_bending_stiffness()

        if self.damage_state.count("broken") == len(self.damage_state):
            self.is_broken = True

        pass

    # Specific methods for the three-point bending load case in A02
    def compute_bending_stiffness(self):
        D_xx = self.D[0][0]
        D_yy = self.D[1][1]
        D_xy = self.D[0][1]
        return self.width*(D_xx - D_xy**2/D_yy)

    def deflection_to_load(self, s, L):
        return 48*self.EI*s/(L**3)

    @staticmethod
    def deflection_to_midplane_curvature(s, L):
        k_xx = 12*s/(L**2)
        return k_xx

    def update_displacement(self, s, L):
        self.displacement = s
        k_xx = self.deflection_to_midplane_curvature(s, L)
        self.update_state(Kx=k_xx)
        pass
