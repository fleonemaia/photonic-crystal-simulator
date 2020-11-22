from tkinter import Tk, Frame, Label, Entry, Button, TOP, LEFT, RIGHT
from modules import *


def app():
    root = Tk()
    root.geometry("500x500")
    root.title("Welcome PC1D calculator!")
    form = make_form(root, entry_fields)
    button_trans(root, form)
    button_ref(root, form)
    button_abs(root, form)
    button_ref_x_trans(root, form)
    button_trans_ref(root, form)
    button_multiple_lambdas(root, form)
    button_lambda_bgs(root, form)
    button_np_bgs(root, form)
    root.mainloop()


def make_form(root, fields):
    entries = {}
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=20, text=field + ": ", anchor='w')
        entry = Entry(row)
        entry.insert(0, "0")
        row.pack(side=TOP, padx=10, pady=5)
        lab.pack(side=LEFT)
        entry.pack(side=RIGHT, ipadx=100)
        entries[field] = entry
    return entries


def button_ref(root, form):
    b = Button(root, text='Reflect', command=(lambda entry_data=form: func_ref(entry_data)))
    b.pack(side=LEFT, padx=10, pady=5)


def button_trans(root, form):
    b = Button(root, text='Trans', command=(lambda entry_data=form: func_trans(entry_data)))
    b.pack(side=LEFT, padx=10, pady=5)


def button_abs(root, form):
    b = Button(root, text='Abs', command=(lambda entry_data=form: func_abs(entry_data)))
    b.pack(side=LEFT, padx=10, pady=5)


def button_ref_x_trans(root, form):
    b = Button(root, text='RefXTrans', command=(lambda entry_data=form: func_ref_x_trans(entry_data)))
    b.pack(side=LEFT, padx=10, pady=5)


def button_trans_ref(root, form):
    b = Button(root, text='TransReflect', command=(lambda entry_data=form: func_trans_ref(entry_data)))
    b.pack(side=LEFT, padx=10, pady=5)


def button_multiple_lambdas(root, form):
    b = Button(root, text='MultipleLam', command=(lambda entry_data=form: func_multiple_lambdas(entry_data)))
    b.pack(side=LEFT, padx=10, pady=5)


def button_lambda_bgs(root, form):
    b = Button(root, text='LamBGS', command=(lambda entry_data=form: func_lambda_bgs(entry_data)))
    b.pack(side=LEFT, padx=10, pady=5)


def button_np_bgs(root, form):
    b = Button(root, text='NpBGS', command=(lambda entry_data=form: func_np_bgs(entry_data)))
    b.pack(side=LEFT, padx=10, pady=5)


if __name__ == '__main__':
    app()
