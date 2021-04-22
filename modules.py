from cmath import exp
from math import sin, cos, asin, pi

from numpy import reshape, identity
from numpy.linalg import pinv

entry_fields = (
    # 'polarization',
    'angle_of_incidence',
    'initial_wavelength',
    'final_wavelength',
    'number_of_pairs',
    'n_inc',
    'n_1',
    'n_2',
    'n_subs',
    'lam_vac',
    'w_n_1',
    'w_n_2',
    'number_of_defects',
    'inter_pairs',
    'n_defects',
    'w_n_defects')


def pc1d(data):
    # Entry
    # polarization = float(data['polarization'].get())
    # All reproductions and simulations are currently in the polarization 's'.
    global matrix_layer_1, matrix_layer_2, matrix_layer_defect
    angle_of_incidence = float(data['angle_of_incidence'].get())
    lam_vac = float(data['lam_vac'].get())
    initial_wavelength = float(data['initial_wavelength'].get())
    final_wavelength = float(data['final_wavelength'].get())
    number_of_pairs = int(data['number_of_pairs'].get())
    n_inc = float(data['n_inc'].get())
    n_1 = float(data['n_1'].get())
    n_2 = float(data['n_2'].get())
    n_subs = float(data['n_subs'].get())
    w_n_1 = float(data['w_n_1'].get())
    w_n_2 = float(data['w_n_2'].get())
    number_of_defects = int(data['number_of_defects'].get())
    inter_pairs = int(data['inter_pairs'].get())
    n_defects = float(data['n_defects'].get())
    w_n_defects = float(data['w_n_defects'].get())

    if lam_vac != 0.0 and w_n_1 == 0.0:
        w_n_1 = lam_vac / (4.0 * n_1)
    if lam_vac != 0.0 and w_n_2 == 0.0:
        w_n_2 = lam_vac / (4.0 * n_2)
    if lam_vac != 0.0 and w_n_defects == 0.0:
        w_n_defects = lam_vac / (4.0 * n_defects)

    # Data
    theta_inc = angle_of_incidence * (pi / 180)
    # numbers_of_layers = 2 * number_of_pairs
    numbers_of_layers = 2 * (number_of_pairs + inter_pairs) + number_of_defects
    steps = int(1000)
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

    # Calculus
    data_wavelength = []
    data_reflectance_by_wavelength = []
    data_transmittance_by_wavelength = []
    for step in range(steps):
        step_wavelength = initial_wavelength + (step * (final_wavelength - initial_wavelength)) / float(steps)
        matrix = identity(2)
        # Matrix layers construction
        for i in range(3):
            if (i + 1) == 1:
                n = n_1
                w = w_n_1
            elif (i + 1) == 2:
                n = n_2
                w = w_n_2
            else:
                n = n_defects
                w = w_n_defects
            theta = asin(snell / n)
            const_k = cos(theta) * n * ((2.0 * pi) / step_wavelength)
            const_phi = const_k * w
            propagation_matrix = reshape([exp(1j * const_phi), 0, 0, exp(-1j * const_phi)], (2, 2))
            delta_layer = reshape([1, 1, n * cos(theta), -n * cos(theta)], (2, 2))
            capital_delta_layer = pinv(delta_layer)
            if (i + 1) == 1:
                matrix_layer_1 = delta_layer.dot(propagation_matrix).dot(capital_delta_layer)
            elif (i + 1) == 2:
                matrix_layer_2 = delta_layer.dot(propagation_matrix).dot(capital_delta_layer)
            else:
                matrix_layer_defect = delta_layer.dot(propagation_matrix).dot(capital_delta_layer)
        # MMT
        for layer in range(numbers_of_layers):
            if number_of_defects == 1:
                if (layer + 1) == number_of_pairs + 1:
                    matrix = matrix_layer_defect.dot(matrix)
                elif (layer + 1) % 2 != 0:
                    matrix = matrix_layer_1.dot(matrix)
                else:
                    matrix = matrix_layer_2.dot(matrix)
            elif number_of_defects == 2:
                if (layer + 1) == number_of_pairs + 1:
                    matrix = matrix_layer_defect.dot(matrix)
                elif (layer + 1) == number_of_pairs + 2 + (inter_pairs * 2):
                    matrix = matrix_layer_defect.dot(matrix)
                elif (layer + 1) % 2 != 0:
                    matrix = matrix_layer_1.dot(matrix)
                else:
                    matrix = matrix_layer_2.dot(matrix)
            elif (layer + 1) % 2 != 0:
                matrix = matrix_layer_1.dot(matrix)
            else:
                matrix = matrix_layer_2.dot(matrix)
        matrix = delta_inc.dot(matrix).dot(capital_delta_subs)
        data_wavelength.append(step_wavelength)
        data_reflectance_by_wavelength.append((abs(matrix[1][0]) / abs(matrix[0][0])) ** 2)
        data_transmittance_by_wavelength.append(((1 / abs(matrix[0][0])) ** 2) * (cos(theta_subs) / cos(theta_inc)))
    return data_wavelength, data_reflectance_by_wavelength, data_transmittance_by_wavelength
