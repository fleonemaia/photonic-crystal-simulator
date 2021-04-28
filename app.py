from tkinter import *
from functions import *
import pandas as pd


def app():
    window_root = Tk()
    window_root.title("PC1D Calculator")
    crystal_name = "Default"
    entry = make_form(window_root, crystal_name)
    make_evaluation(window_root, entry)
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


def make_evaluation(window_root, entry):
    click_action = StringVar()
    click_action.set(options_action[0])
    menu_action = OptionMenu(window_root, click_action, *options_action)
    menu_action.pack(side=TOP, padx=10, pady=5)
    b = Button(window_root, text='Evaluate', command=(lambda: func_evaluate(entry, click_action.get())))
    b.pack(side=TOP, padx=10, pady=5)


if __name__ == '__main__':
    dataCSV = pd.read_csv("data.csv")
    data = pd.DataFrame(dataCSV).set_index("Index").rename_axis("Crystals name", axis=1)
    options_action = [
        "Transmittance",
        "Reflectance",
        "Absorption",
        "Reflectance with Transmittance",
        "Absorption, Reflectance with Transmittance",
        "Reflectance and Transmittance",
        "Reflectance by Transmittance"
    ]
    app()
