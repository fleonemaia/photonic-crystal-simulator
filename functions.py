from matplotlib.pyplot import figure, plot, xlabel, ylabel, show, subplot, subplots
from numpy import ones

from modules import *


def func_ref(data):
    x, y_ref, y_trans = pc1d(data)
    figure()
    plot(x, y_ref, 'blue')
    xlabel('nm')
    ylabel('Reflectância')
    show()


def func_trans(data):
    x, y_ref, y_trans = pc1d(data)
    figure()
    plot(x, y_trans, 'red')
    xlabel('nm')
    ylabel('Transmitância')
    show()


def func_abs(data):
    x, y_ref, y_trans = pc1d(data)
    figure()
    y_abs = ones(len(x))
    y_abs = y_abs - y_ref - y_trans
    plot(x, y_abs, 'purple')
    xlabel('nm')
    ylabel('Absorção')
    show()


def func_ref_by_trans(data):
    x, y_ref, y_trans = pc1d(data)
    figure()
    plot(y_ref, y_trans, 'orange')
    xlabel('Reflectância')
    ylabel('Transmitância')
    show()


def func_trans_w_ref(data):
    x, y_ref, y_trans = pc1d(data)
    subplot(2, 1, 1)
    plot(x, y_trans, 'red')
    ylabel('Transmitância')
    subplot(2, 1, 2)
    plot(x, y_ref, 'blue')
    xlabel('nm')
    ylabel('Reflectância')
    show()


def func_trans_ref_w_abs(data):
    x, y_ref, y_trans = pc1d(data)
    plot(x, y_trans, 'red')
    plot(x, y_ref, 'blue')
    y_abs = ones(len(x))
    y_abs = y_abs - y_ref - y_trans
    plot(x, y_abs, 'purple')
    xlabel('nm')
    ylabel('TRA')
    show()


# def func_multiple_lambdas(data):
#     initial_wavelength = int(data['initial_wavelength'].get())
#     final_wavelength = int(data['final_wavelength'].get())
#     step = int((final_wavelength - initial_wavelength) / 5)
#     ran = range(initial_wavelength + step, final_wavelength, step)
#     # fig, ax = subplots()
#     for lam_vac in ran:
#         size = len(data['lam_vac'].get())
#         data['lam_vac'].delete(0, last=size)
#         data['lam_vac'].insert(0, lam_vac)
#         x, y_ref, y_trans = pc1d(data)
#         ax.plot(x, y_trans)
#     xlabel('nm')
#     ylabel('Transmitância')
#     show()
#
#
# def func_lambda_bgs(data):
#     initial_wavelength = int(data['initial_wavelength'].get())
#     final_wavelength = int(data['final_wavelength'].get())
#     step = int((final_wavelength - initial_wavelength) / 10)
#     fig, ax = subplots()
#     bgs = []
#     lambda_c = []
#     for lam_vac in range(initial_wavelength + step, final_wavelength - step - step, step):
#         size = len(data['lam_vac'].get())
#         data['lam_vac'].delete(0, last=size)
#         data['lam_vac'].insert(0, lam_vac)
#         x, y_ref, y_trans = pc1d(data)
#
#         pos = 0
#         pos_i = 0
#         pos_f = 0
#         bigger = 0
#         for element in y_ref:
#             if element >= 0.95:
#                 pos_f = pos
#             else:
#                 if x[pos_f] - x[pos_i] > bigger:
#                     bigger = x[pos_f] - x[pos_i]
#                 pos_i = pos
#             pos += 1
#         if x[pos_f] - x[pos_i] > bigger:
#             bigger = x[pos_f] - x[pos_i]
#         bgs.append(bigger)
#         lambda_c.append(lam_vac)
#     ax.plot(lambda_c, bgs)
#     xlabel('nm (Capital Lambda for quarter wave structure)')
#     ylabel('BGS')
#     show()
#
#
# def func_np_bgs(data):
#     fig, ax = subplots()
#     bgs = []
#     par_c = []
#     for par in range(30):
#         pp = par + 1
#         size = len(data['number_of_pairs'].get())
#         data['number_of_pairs'].delete(0, last=size)
#         data['number_of_pairs'].insert(0, pp)
#         x, y_ref, y_trans = pc1d(data)
#
#         pos = 0
#         pos_i = 0
#         pos_f = 0
#         bigger = 0
#         for element in y_ref:
#             if element >= 0.95:
#                 pos_f = pos
#             else:
#                 if x[pos_f] - x[pos_i] > bigger:
#                     bigger = x[pos_f] - x[pos_i]
#                 pos_i = pos
#             pos += 1
#         if x[pos_f] - x[pos_i] > bigger:
#             bigger = x[pos_f] - x[pos_i]
#         bgs.append(bigger)
#         par_c.append(pp)
#     ax.plot(par_c, bgs)
#     xlabel('pp')
#     ylabel('BGS')
#     show()
