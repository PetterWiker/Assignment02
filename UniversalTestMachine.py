import xlsxwriter
import matplotlib.pyplot as plt
import time
import plotlib
import laminatelib
import numpy as np


class UniversalTestMachine:

    def __init__(self, span, resolution=0.01, max_load=1000):
        self.span = span
        self.resolution = resolution
        self.max_load = max_load
        self.data = {}

        #self.perform_bending_test()
        #self.save_data_to_excel()
        pass

    def perform_bending_test(self, laminates, break_crit=0.8):
        for laminate in laminates:
            loads = []
            displacements = []

            displacement = 0
            load = 0
            max_load = 0
            while not laminate.is_broken and load < self.max_load and displacement <= 20:
                load = laminate.deflection_to_load(displacement, L=self.span)
                loads.append(load)
                displacements.append(displacement)
                displacement += self.resolution

                laminate.kappa_x = laminate.deflection_to_midplane_curvature(s=displacement, L=self.span)
                laminate.update_state(Kx=laminate.kappa_x)
                laminate.check_ply_stress_states()

                if load > max_load:
                    max_load = load
                if load < break_crit*max_load:
                    break

            self.data[laminate.name] = {}
            self.data[laminate.name]["loads"] = loads
            self.data[laminate.name]["displacements"] = displacements
        pass

    def save_data_to_excel(self):
        timestamp = time.strftime("%Y%m%d%H%M%S")
        workbook = xlsxwriter.Workbook("data/3pt_bending_{}.xlsx".format(timestamp))

        for name, laminate in self.data.items():
            worksheet = workbook.add_worksheet(name=name)
            worksheet.write(0, 0, "Displacement [mm]")
            worksheet.write(0, 1, "Load [N]")

            for idx, value in enumerate(laminate["displacements"]):
                worksheet.write(idx+1, 0, value)
                worksheet.write(idx+1, 1, laminate["loads"][idx])
        workbook.close()
        pass

    def plot_data(self):
        legend = []
        for name, laminate in self.data.items():
            legend.append(name)
            plt.plot(laminate["displacements"], laminate["loads"])

        plt.title("3pt-Bending_{}_{}_{}".format(self.span, self.resolution, self.max_load))
        plt.xlabel("Displacement [mm]")
        plt.ylabel("Load [N]")
        plt.legend(legend)
        plt.show()
        pass

    def reset_data(self):
        self.data = {}
        pass