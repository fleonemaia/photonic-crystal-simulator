from cProfile import label
import tkinter as tk
import pandas as pd
from numpy import identity, reshape, ones
import matplotlib.pyplot as plt
from math import sin, cos, pi, asin
from numpy.linalg import pinv
from cmath import exp

def pcs(data):
    
    initial_wavelength = float(data[0])
    final_wavelength   = float(data[1])
    polarization       = data[2]
    angle_of_incidence = float(data[3])
    n_inc              = float(data[4])
    n_1                = float(data[5])
    n_2                = float(data[6])
    n_subs             = float(data[7])
    number_of_pairs    = int(data[8])
    is_quarter_wave    = int(data[9])
    lam_vac1           = float(data[10])
    lam_vac2           = float(data[11])
    w_n_1              = float(data[12])
    w_n_2              = float(data[13])
    number_of_defects  = int(data[14])
    n_defects          = float(data[15])
    lam_vac_def        = float(data[16])
    w_n_defects        = float(data[17])
    inter_pairs        = int(data[18])
    

    # Barriers
    number_of_materials = 2
    if number_of_defects == 1 or number_of_defects == 2:
        number_of_materials = 3
    elif number_of_defects != 0:
        tk.messagebox.showwarning("Warning", "The answer for 'Are there any defects?' must be 0, 1 or 2.")
        return
    if is_quarter_wave == 1:
        w_n_1 = lam_vac1 / (4.0 * n_1)
        w_n_2 = lam_vac2 / (4.0 * n_2)
        if number_of_defects == 1 or number_of_defects == 2:
            w_n_defects = lam_vac_def / (4.0 * n_defects)

    # VARIABLES
    data_wavelength = []
    data_reflectance_by_wavelength = []
    data_transmittance_by_wavelength = []
    steps = 1000
    matrix_layer_1 = identity(2)
    matrix_layer_2 = identity(2)
    matrix_layer_defect = identity(2)

    # EVALUATION
    numbers_of_layers = 2 * (number_of_pairs + inter_pairs) + number_of_defects
    theta_inc = angle_of_incidence * (pi / 180)
    snell = n_inc * sin(theta_inc)
    delta_inc = reshape([1.0, 1.0, n_inc * cos(theta_inc), - n_inc * cos(theta_inc)], (2, 2))
    if numbers_of_layers % 2 != 0:
        capital_theta = asin(snell / n_1)
        capital_eta = n_1
    else:
        capital_theta = asin(snell / n_2)
        capital_eta = n_2
    theta_subs = asin((capital_eta * sin(capital_theta)) / n_subs)
    delta_subs = reshape([1, 1, n_subs * cos(theta_subs), -n_subs * cos(theta_subs)], (2, 2))
    capital_delta_subs = pinv(delta_subs)
    for step in range(steps):
        step_wavelength = initial_wavelength + (step * (final_wavelength - initial_wavelength)) / float(steps)
        # Matrix layers construction
        n = 0.0
        w = 0.0
        for i in range(number_of_materials):
            if i == 0:
                n = n_1
                w = w_n_1
            elif i == 1:
                n = n_2
                w = w_n_2
            elif i == 2:
                n = n_defects
                w = w_n_defects
            theta = asin(snell / n)
            const_k = cos(theta) * n * ((2.0 * pi) / step_wavelength)
            const_phi = const_k * w
            propagation_matrix = reshape([exp(1j * const_phi), 0, 0, exp(-1j * const_phi)], (2, 2))
            delta_layer = reshape([1, 1, n * cos(theta), -n * cos(theta)], (2, 2))
            capital_delta_layer = pinv(delta_layer)
            if i == 0:
                matrix_layer_1 = delta_layer.dot(propagation_matrix).dot(capital_delta_layer)
            elif i == 1:
                matrix_layer_2 = delta_layer.dot(propagation_matrix).dot(capital_delta_layer)
            elif i == 2:
                matrix_layer_defect = delta_layer.dot(propagation_matrix).dot(capital_delta_layer)
        # MMT
        matrix = identity(2)
        for layer in range(numbers_of_layers):
            if number_of_defects == 0:
                if (layer + 1) % 2 != 0:
                    matrix = matrix_layer_1.dot(matrix)
                else:
                    matrix = matrix_layer_2.dot(matrix)
            elif number_of_defects == 1:
                if (layer + 1) == number_of_pairs + 1:
                    matrix = matrix_layer_defect.dot(matrix)
                elif (layer + 1) % 2 != 0:
                    matrix = matrix_layer_1.dot(matrix)
                else:
                    matrix = matrix_layer_2.dot(matrix)
            elif number_of_defects == 2:
                if (layer + 1) == number_of_pairs + 1:
                    matrix = matrix_layer_defect.dot(matrix)
                elif (layer + 1) == number_of_pairs + 1 + (inter_pairs * 2) + 1:
                    matrix = matrix_layer_defect.dot(matrix)
                elif (layer + 1) % 2 != 0:
                    matrix = matrix_layer_1.dot(matrix)
                else:
                    matrix = matrix_layer_2.dot(matrix)
        matrix = delta_inc.dot(matrix).dot(capital_delta_subs)

        data_wavelength.append(step_wavelength)
        data_reflectance_by_wavelength.append((abs(matrix[1][0]) / abs(matrix[0][0])) ** 2)
        data_transmittance_by_wavelength.append((((1 / abs(matrix[0][0])) ** 2) * (cos(theta_subs) / cos(theta_inc))
                                                 # .real
                                                 ))

    return data_wavelength, data_reflectance_by_wavelength, data_transmittance_by_wavelength

def make_plots(action, x, y_ref, y_trans):
    if action == "Transmittance":
        plt.plot(x, y_trans, 'red', label='Transmittance')
        plt.xlabel('Nanometers')
        plt.ylabel('Transmittance')
        plt.show()
    elif action == "Reflectance":
        plt.plot(x, y_ref, 'blue', label='Reflectance')
        plt.xlabel('Nanometers')
        plt.ylabel('Reflectância')
        plt.show()
    elif action == "Absorption":
        plt.plot(x, ones(len(x)) - y_ref - y_trans, 'purple', label='Absorption')
        plt.xlabel('Nanometers')
        plt.ylabel('Absorção')
        plt.show()
    elif action == "Reflectance and Transmittance":
        plt.plot(x, y_ref, 'blue', label='Reflectance')
        plt.plot(x, y_trans, 'red', label='Transmittance')
        plt.xlabel('Nanometers')
        plt.ylabel('Intensidade')
        plt.show()
    elif action == "Reflectance, Absorption and Transmittance":
        plt.plot(x, y_ref, 'blue', label='Reflectance')
        plt.plot(x, y_trans, 'red', label='Transmittance')
        plt.plot(x, ones(len(x)) - y_ref - y_trans, 'purple', label='Absorption')
        plt.xlabel('Nanometers')
        plt.ylabel('Intensidade')
        plt.show()

def button_action(variables, entries, action):
    e_values = [entries[variable].get() for variable in variables]
    w, r, t = pcs(e_values)
    make_plots(action, w, r, t)

def window(variables, actions):
    HEIGHT = 700
    WIDTH = 600
    
    root = tk.Tk()
    
    root.title("Photonic Crystal Simulator")

    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()

    shell = tk.Frame(root, bg='#80c1ff', bd=5)
    shell.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)

    frame = tk.Frame(root, bg='#80c1ff', bd=5)
    frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

    entries = {}
    line = 0.0
    for variable in variables:
        lab = tk.Label(frame, width=20, text=variable)
        lab.place(relx=0.0, rely=line, relwidth=0.5, relheight=0.05)

        entries[variable] = tk.Entry(frame, width=5)
        entries[variable].insert(0, '0')
        entries[variable].place(relx=0.5, rely=line, relwidth=0.5, relheight=0.05)
        line += 0.05

    click_action = tk.StringVar()
    click_action.set('Choose action')
    menu_action = tk.OptionMenu(frame, click_action, *actions)
    menu_action.place(relx=0.0, rely=line, relwidth=0.5, relheight=0.05)
    
    button = tk.Button(shell, text='Evaluate', command=(lambda: button_action(variables, entries, click_action.get())))
    button.place(relx=0.25, rely=line, relwidth=0.5, relheight=0.05)

    root.mainloop()

def app():
    variables = ['Initial wavelength', 
    'Final wavelength', 
    'Wave polarization', 
    'Wave incidence angle', 
    'Refractive index of the incident layer',
    'Refractive index of odd layer', 
    'Refractive index of even layer', 
    'Refractive index of the substrate layer',
    'Number of pairs of crystal layers', 
    'Is structure a quarter-wave?', 
    'Odd layer resonant wavelength',
    'Even layer resonant wavelength', 
    'Odd layer width', 
    'Even layer width', 
    'Are there any defects?',
    'Refractive index of the defect layer', 
    'Defect layer resonant wavelength', 
    'Defect layer width',
    'Number of pairs of crystal layers between defects']

    actions = ["Transmittance",
    "Reflectance",
    "Absorption",
    "Reflectance and Transmittance",
    "Reflectance, Absorption and Transmittance"]

    window(variables, actions)

if __name__ == '__main__':
    app()
