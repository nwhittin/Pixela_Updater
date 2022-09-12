import requests
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import time
import webbrowser
import os

PIXELA_ENDPOINT = "https://pixe.la/v1/users"
USERNAME = "nwhittin"
TOKEN = os.environ.get("TOKEN")
TODAY = datetime.now().strftime("%Y%m%d")
GRAPHS_ENDPOINT = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs"
HEADER = {
    "X-USER-TOKEN": TOKEN,
}
FONT = ("Arial", 12, "normal")


def get_graphs():
    while True:
        response = requests.get(url=GRAPHS_ENDPOINT, headers=HEADER)
        print(response)
        if response.status_code in (200, 201):
            return response.json()["graphs"]
        elif response.status_code in (400, 404):
            messagebox.showerror(title="Pixela Updater",
                                 message="Connection Error\nPlease try again later.\nClick OK to exit.")
            quit()
        else:
            time.sleep(3)


class UpdateButton:

    def __init__(self, index):
        self.index = index
        self.update_button = Button(text="Create/Update Pixel", font=FONT, command=self.check_inputs)
        self.update_button.grid(row=self.index, column=3, padx=5, pady=2)

    def check_inputs(self):
        value = entries[self.index].get()
        if graphs[self.index]["type"] == "int":
            try:
                value = int(value)
            except ValueError:
                messagebox.showerror(title="", message="Please enter a positive integer. ex: 1, 2, 3...")
                entries[self.index].delete(0, END)
            else:
                if value <= 0:
                    messagebox.showerror(title="", message="Please enter a positive integer. ex: 1, 2, 3...")
                    entries[self.index].delete(0, END)
                else:
                    self.update_pixel(value)
        elif graphs[self.index]["type"] == "float":
            try:
                value = float(value)
            except ValueError:
                messagebox.showerror(title="", message="Please enter a positive number. ex: 1, 2.7, 3.49...")
                entries[self.index].delete(0, END)
            else:
                if value <= 0:
                    messagebox.showerror(title="", message="Please enter a positive number. ex: 1, 2.7, 3.49...")
                    entries[self.index].delete(0, END)
                else:
                    self.update_pixel(value)

    def update_pixel(self, value):
        update_url = f"{GRAPHS_ENDPOINT}/{graphs[self.index]['id']}/{TODAY}"
        update_params = {
            "quantity": str(value),
        }
        while True:
            response = requests.put(url=update_url, json=update_params, headers=HEADER)
            print(response)
            if response.status_code in (200, 201):
                messagebox.showinfo(title="", message=f"{graphs[self.index]['name'].title()} graph updated")
                entries[self.index].delete(0, END)
                break
            elif response.status_code in (400, 404):
                messagebox.showerror(title="Pixela Updater",
                                     message="Connection Error\nPlease try again later.\nClick OK to exit.")
                quit()
            else:
                time.sleep(3)


class URLButton:

    def __init__(self, index):
        self.index = index
        self.url_button = Button(text="View Graph", font=FONT, command=self.view_graph)
        self.url_button.grid(row=self.index, column=4)

    def view_graph(self):
        view_graph_url = f"{GRAPHS_ENDPOINT}/{graphs[self.index]['id']}.html"
        webbrowser.open(url=view_graph_url)


# ---------- GET GRAPH INFORMATION ---------- #
graphs = get_graphs()

# ---------- UI SETUP ---------- #
window = Tk()

window.title("Pixela Updater")
window.config(padx=50, pady=50)

id_labels = []
uom_labels = []
entries = []
update_buttons = []
url_buttons = []
for x in range(len(graphs)):
    id_label = Label(text=graphs[x]["name"], font=FONT)
    id_label.grid(row=x, column=0)
    id_labels.append(id_label)
    entry = Entry(width=7, font=FONT)
    entry.grid(row=x, column=1)
    entries.append(entry)
    uom_label = Label(text=graphs[x]["unit"], font=FONT)
    uom_label.grid(row=x, column=2)
    uom_labels.append(uom_label)
    update_button = UpdateButton(x)
    update_buttons.append(update_button)
    url_button = URLButton(x)
    url_buttons.append(url_button)

window.mainloop()
