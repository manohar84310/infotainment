# # report_viewer.py

# import tkinter as tk

# def create_report_viewer_window(root):
#     viewer = tk.Toplevel(root)
#     viewer.title("Test Report Viewer")
#     viewer.geometry("500x400")

#     label = tk.Label(viewer, text="Report viewer coming soon...", font=("Arial", 14))
#     label.pack(pady=20)
# report_viewer.py

import tkinter as tk
from tkinter import messagebox
import os
import webbrowser

def create_report_viewer_window(root):
    viewer = tk.Toplevel(root)
    viewer.title("Test Report Viewer")
    viewer.geometry("500x400")

    tk.Label(viewer, text="Available Reports", font=("Arial", 14, "bold")).pack(pady=10)

    report_dir = "reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    files = [f for f in os.listdir(report_dir) if f.endswith((".pdf", ".csv"))]

    if not files:
        tk.Label(viewer, text="No reports found.", font=("Arial", 12)).pack(pady=20)
        return

    listbox = tk.Listbox(viewer, font=("Arial", 11), width=60, height=15)
    for file in files:
        listbox.insert(tk.END, file)
    listbox.pack(pady=10)

    def open_selected_file():
        selection = listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Please select a report to view.")
            return
        filename = files[selection[0]]
        filepath = os.path.abspath(os.path.join(report_dir, filename))
        webbrowser.open(filepath)

    tk.Button(viewer, text="Open Selected Report", command=open_selected_file, bg="#007bff", fg="white").pack(pady=10)
