from tkinter import Tk, Frame, Label, Entry, TOP, RIGHT

from buttons import *


def app():
    window_root = Tk()
    window_root.geometry("900x500")
    window_root.title("PC1D Calculator")
    form = make_form(window_root, entry_fields)
    button_trans(window_root, form)
    button_ref(window_root, form)
    button_abs(window_root, form)
    button_ref_by_trans(window_root, form)
    button_trans_w_ref(window_root, form)
    button_trans_ref_w_abs(window_root, form)
    # button_multiple_lambdas(window_root, form)
    # button_lambda_bgs(window_root, form)
    # button_np_bgs(window_root, form)
    window_root.mainloop()


def make_form(window_root, fields):
    entries = {}
    for field in fields:
        row = Frame(window_root)
        lab = Label(row, width=20, text=field + ": ", anchor='w')
        entry = Entry(row)
        entry.insert(0, "0")
        row.pack(side=TOP, padx=10, pady=5)
        lab.pack(side=LEFT)
        entry.pack(side=RIGHT, ipadx=100)
        entries[field] = entry
    return entries


if __name__ == '__main__':
    app()
