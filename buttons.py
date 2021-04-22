from tkinter import Button, LEFT

from functions import *


def button_ref(window_root, form):
    b = Button(window_root, text='Reflectance',
               command=(lambda entry_data=form: func_ref(entry_data)))
    b.pack(side=LEFT, padx=10, pady=5)


def button_trans(window_root, form):
    b = Button(window_root, text='Transmittance',
               command=(lambda entry_data=form: func_trans(entry_data)))
    b.pack(side=LEFT, padx=10, pady=5)


def button_abs(window_root, form):
    b = Button(window_root, text='Absorption',
               command=(lambda entry_data=form: func_abs(entry_data)))
    b.pack(side=LEFT, padx=10, pady=5)


def button_ref_by_trans(window_root, form):
    b = Button(window_root, text='ReflectanceByTransmittance',
               command=(lambda entry_data=form: func_ref_by_trans(entry_data)))
    b.pack(side=LEFT, padx=10, pady=5)


def button_trans_w_ref(window_root, form):
    b = Button(window_root, text='TransmittanceAndReflectance',
               command=(lambda entry_data=form: func_trans_w_ref(entry_data)))
    b.pack(side=LEFT, padx=10, pady=5)


def button_trans_ref_w_abs(window_root, form):
    b = Button(window_root, text='TransmittanceReflectanceAndAbsorption',
               command=(lambda entry_data=form: func_trans_ref_w_abs(entry_data)))
    b.pack(side=LEFT, padx=10, pady=5)


# def button_multiple_lambdas(window_root, form):
#     b = Button(window_root, text='MultipleLam',
#                command=(lambda entry_data=form: func_multiple_lambdas(entry_data)))
#     b.pack(side=LEFT, padx=10, pady=5)
#
#
# def button_lambda_bgs(window_root, form):
#     b = Button(window_root, text='LamBGS',
#                command=(lambda entry_data=form: func_lambda_bgs(entry_data)))
#     b.pack(side=LEFT, padx=10, pady=5)
#
#
# def button_np_bgs(window_root, form):
#     b = Button(window_root, text='NpBGS',
#                command=(lambda entry_data=form: func_np_bgs(entry_data)))
#     b.pack(side=LEFT, padx=10, pady=5)
