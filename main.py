import matlib
from Laminate import Laminate
from Assignment02.UniversalTestMachine import UniversalTestMachine


# We can start by defining our laminates for assignment A02 and store them in a list
laminates = []

# The single layer unidirectional carbon fibre laminate
material_B = matlib.get("material_B")
layup_B = [{'mat': material_B, 'ori': 0, "thi": 1.5}]
laminates.append(Laminate(layup_B, name="B", width=15.5))

# The symmetric and inbalanced E-glass/epoxy laminate
material_C = matlib.get("material_C")
layup_C = [{'mat': material_C, 'ori': 45, "thi": 0.064*3.3},
              {'mat': material_C, 'ori': -45, "thi": 0.064*3.3},
              {'mat': material_C, 'ori': 0, "thi": 1/3*0.74*3.3},
              {'mat': material_C, 'ori': 0, "thi": 1/3*0.74*3.3},
              {'mat': material_C, 'ori': 0, "thi": 1/3*0.74*3.3},
              {'mat': material_C, 'ori': -45, "thi": 0.064*3.3},
              {'mat': material_C, 'ori': 45, "thi": 0.064*3.3}]
laminates.append(Laminate(layup_C, name="C", width=22.0))

# The symmetric and balanced E-glass/epoxy laminate
material_D = matlib.get("material_D")
layup_D = [{'mat': material_D, 'ori': 45, "thi": 0.13*4},
              {'mat': material_D, 'ori': -45, "thi": 0.13*4},
              {'mat': material_D, 'ori': 0, "thi": 0.5*0.48*4},
              {'mat': material_D, 'ori': 0, "thi": 0.5*0.48*4},
              {'mat': material_D, 'ori': -45, "thi": 0.13*4},
              {'mat': material_D, 'ori': 45, "thi": 0.13*4}]
laminates.append(Laminate(layup_D, name="D", width=25.0))

# The symmetric and balanced E-glass/polypropylene laminate
material_E = matlib.get("material_E")
layup_E = [{'mat': material_E, 'ori': 0, "thi": 3.8/8},
              {'mat': material_E, 'ori': 90, "thi": 3.8/8},
              {'mat': material_E, 'ori': 45, "thi": 3.8/8},
              {'mat': material_E, 'ori': -45, "thi": 3.8/8},
              {'mat': material_E, 'ori': -45, "thi": 3.8/8},
              {'mat': material_E, 'ori': 45, "thi": 3.8/8},
              {'mat': material_E, 'ori': 90, "thi": 3.8/8},
              {'mat': material_E, 'ori': 0, "thi": 3.8/8}]
laminates.append(Laminate(layup_E, name="E", width=20.0))


def main():
    UTM = UniversalTestMachine(span=100, resolution=0.01)
    UTM.perform_bending_test(laminates)
    #UTM.plot_data()
    UTM.save_data_to_excel()
    UTM.reset_data()
    pass


if __name__ == "__main__":
    main()