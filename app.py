from tkinter import *
from functions import *
import pandas as pd


def app():
    window_root = Tk()
    window_root.title("PC1D Calculator")
    crystal_name = "KRC 1"  # substitute for a menu
    calculate_action = "Absorption, Reflectance with Transmittance"  # substitute for a menu
    # checkbox for save image
    entry = make_form(window_root, crystal_name)
    button_evaluate(window_root, entry, calculate_action)
    window_root.mainloop()


def make_form(window_root, crystal_name):
    entries = {}
    for element in list(range(19)):
        row = Frame(window_root)
        lab = Label(row, width=38, text=data.index.values[element], anchor='w')
        entry = Entry(row, width=5)
        entry.insert(0, str(data[crystal_name][element]))
        row.pack(side=TOP, padx=10, pady=5)
        lab.pack(side=LEFT)
        entry.pack(side=RIGHT, ipadx=20)
        entries[data.index.values[element]] = entry
    return entries


def button_evaluate(window_root, entry, action):
    b = Button(window_root, text='Evaluate', command=(lambda: func_evaluate(entry, action)))
    b.pack(side=TOP, padx=10, pady=5)


if __name__ == '__main__':
    dataCSV = pd.read_csv("data.csv")
    data = pd.DataFrame(dataCSV).set_index("Index").rename_axis("Crystals name", axis=1)
    app()

# 2.9304+2.9996j
