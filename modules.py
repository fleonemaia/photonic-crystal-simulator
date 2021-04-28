from cmath import exp
from math import sin, cos, asin, pi
from numpy import reshape, identity
from numpy.linalg import pinv
from tkinter import messagebox


# noinspection PyTypeChecker
def pc1d(data):
    # INPUT
    initial_wavelength = float(data['Initial wavelength for analysis'].get())
    final_wavelength = float(data['Final wavelength for analysis'].get())
    # polarization = str(data['Wave polarization'].get())
    angle_of_incidence = float(data['Wave incidence angle'].get())
    number_of_pairs = int(data['Number of pairs of crystal layers'].get())
    is_quarter_wave = int(data['Is structure a quarter-wave?'].get())
    lam_vac1 = float(data['Odd layer resonant wavelength'].get())
    lam_vac2 = float(data['Odd layer resonant wavelength'].get())
    w_n_1 = float(data['Odd layer width'].get())
    w_n_2 = float(data['Even layer width'].get())
    number_of_defects = int(data['Are there any defects?'].get())
    lam_vac_def = float(data['Defect layer resonant wavelength'].get())
    w_n_defects = float(data['Defect layer width'].get())
    inter_pairs = int(data['Number of pairs of crystal layers between defects'].get())
    n_inc = float(data['Refractive index of the incident layer'].get())
    n_1 = float(data['Refractive index of odd layer'].get())
    n_2 = float(data['Refractive index of even layer'].get())
    n_subs = float(data['Refractive index of the substrate layer'].get())
    n_defects = float(data['Refractive index of the defect layer'].get())

    # Barriers
    number_of_materials = 2
    if number_of_defects == 1 or number_of_defects == 2:
        number_of_materials = 3
    elif number_of_defects != 0:
        messagebox.showwarning("Warning", "The answer for 'Are there any defects?' must be 0, 1 or 2.")
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
