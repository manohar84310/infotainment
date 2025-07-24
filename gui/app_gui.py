# ----------------------------
# Standard Library Imports
# ----------------------------
import datetime
import io
import os
import smtplib
import subprocess
import sys
import tempfile
import traceback

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ----------------------------
# Third-Party Library Imports
# ----------------------------
from fpdf import FPDF
from tkcode import CodeEditor

# ----------------------------
# Tkinter and IDLE Imports
# ----------------------------
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator

# ----------------------------
# Local Application Imports
# ----------------------------
from .code_editor import CodeEditor
from core.runner import run_test_script
from buttons_ui import create_buttons
from output_pane import create_output_pane





class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Infotainment Test Automation Tool")

        self.uploaded_files = {}       # filename: full_path
        self.checkbox_vars = {}        # filename: BooleanVar

        self.main_pane = tk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        self.left_pane = tk.Frame(self.main_pane, bg="white")
        self.right_pane = tk.Frame(self.main_pane, bg="white")

        self.main_pane.add(self.left_pane, width=600)   # left side
        self.main_pane.add(self.right_pane,width =450)            # right side





#         # Frame for Checkboxes with Scrollbar
#         checkbox_frame = tk.Frame(root)
#         #checkbox_frame.pack(padx=10, pady=5)
#         checkbox_frame.pack(side="top", anchor="nw", fill="x", padx=10, pady=5)

#         self.canvas = tk.Canvas(
#         checkbox_frame,
#         height=200,
#         width=600,
#         bg="white",                # ✅ White background
#         highlightthickness=0
#         )

#         self.scrollbar = ttk.Scrollbar(
#         checkbox_frame,
#         orient="vertical",
#         command=self.canvas.yview
#         )

#         self.checkbox_container = tk.Frame(
#         self.canvas,
#         bg="white"                 # ✅ Container background
#         )

#         self.checkbox_container.bind(
#         "<Configure>",
#         lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#         )

#         self.canvas.create_window((0, 0), window=self.checkbox_container, anchor="nw")
#         self.canvas.configure(yscrollcommand=self.scrollbar.set)

#         self.canvas.pack(side="left", fill="y")
#         self.scrollbar.pack(side="right", fill="y")

#         self.upload_button, self.run_button, self.delete_button, self.open_log_button, self.email_entry, self.email_button = create_buttons(
#         self.left_pane,                 # ✅ Should match the first param name in the function
#         self.upload_test_scripts,
#         self.run_selected_tests,
#         self.delete_selected_scripts,
#         self.open_log_file,
#         self.email_report,
#         self.open_code_editor
#         )


#         # 👇 Pass None instead of the refresh function
#         self.output_box, self.left_pane = create_output_pane(
#         root, self.clear_output,  None
# )

        
#         #self.refresh_log_dropdown()



#         self.log_dropdown_var = tk.StringVar()
#         self.log_dropdown = ttk.Combobox(
#         root, textvariable=self.log_dropdown_var,
#         state="readonly", width=60
#         )
#         self.refresh_log_dropdown()

#         self.log_dropdown.pack(pady=5)
#         self.log_dropdown.bind("<<ComboboxSelected>>", self.display_selected_log)

        # Frame for Checkboxes with Scrollbar
        checkbox_frame = tk.Frame(self.left_pane)
        # checkbox_frame.pack(padx=10, pady=5)
        checkbox_frame.pack(side="top", anchor="nw", fill="x", padx=10, pady=5)

        self.canvas = tk.Canvas(
    checkbox_frame,
    height=200,
    width=600,
    bg="white",  # ✅ White background
    highlightthickness=0
)

        self.scrollbar = ttk.Scrollbar(
            checkbox_frame,
            orient="vertical",
            command=self.canvas.yview
        )

        self.checkbox_container = tk.Frame(
            self.canvas,
            bg="white"  # ✅ Container background
        )

        self.checkbox_container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.checkbox_container, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="y")
        self.scrollbar.pack(side="right", fill="y")

        # ✅ Moved OUTPUT BOX just ABOVE the buttons, changed root ➜ self.left_pane
        #self.output_box, _ = create_output_pane(
            #self.left_pane, self.clear_output, None
        #)

        # ✅ Buttons come AFTER the output box now
        self.upload_button, self.run_button, self.delete_button, self.open_log_button, self.email_entry, self.email_button = create_buttons(
            self.left_pane,
            self.upload_test_scripts,
            self.run_selected_tests,
            self.delete_selected_scripts,
            self.open_log_file,
            self.email_report,
            self.open_code_editor
        )

        # self.refresh_log_dropdown()

        self.log_dropdown_var = tk.StringVar()
        self.log_dropdown = ttk.Combobox(
            root, textvariable=self.log_dropdown_var,
            state="readonly", width=60
        )
        self.refresh_log_dropdown()

        self.log_dropdown.pack(pady=5)
        self.log_dropdown.bind("<<ComboboxSelected>>", self.display_selected_log)


        
        # # Output Label
        # tk.Label(root, text="Test Output:", font=("Arial", 12)).pack(pady=(10, 0))

        # self.output_box = tk.Text(root, height=10, width=180)
        # self.output_box.pack(pady=(5, 10))

        # self.clear_button = tk.Button(
        # root,
        # text="🧹 Clear Output",
        # command=self.clear_output,
        # bg="#6c757d",
        # fg="white",
        # activebackground="#5a6268",
        # font=("Arial", 10, "bold"),
        # padx=10,
        # pady=5
        # )
        # self.clear_button.pack(pady=(0, 10))

        # self.clear_button.bind("<Enter>", lambda e: self.clear_button.config(bg="#5a6268"))
        # self.clear_button.bind("<Leave>", lambda e: self.clear_button.config(bg="#6c757d"))

        

        # Output Label in right pane
        tk.Label(self.right_pane, text="Test Output:", font=("Arial", 12)).pack(pady=(10, 0))

        self.output_box = tk.Text(self.right_pane, height=25, width=70)
        self.output_box.pack(pady=(5, 10), padx=10, fill="both", expand=True)

        self.clear_button = tk.Button(
        self.right_pane,
        text="🧹 Clear Output",
        command=self.clear_output,
        bg="#6c757d",
        fg="white",
        activebackground="#5a6268",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=5
        )
        self.clear_button.pack(pady=(0, 10))

        self.clear_button.bind("<Enter>", lambda e: self.clear_button.config(bg="#5a6268"))
        self.clear_button.bind("<Leave>", lambda e: self.clear_button.config(bg="#6c757d"))




    def open_code_editor(self):
        CodeEditor(self.root)


    def upload_test_scripts(self):
        files = filedialog.askopenfilenames(
            title="Select Python Test Files",
            filetypes=[("Python Files", "*.py")]
        )

        invalid_files = []

        for file_path in files:
            filename = file_path.split("/")[-1]

            # ✅ Only accept files starting with 'test' and ending with .py
            if not (filename.startswith("test") and filename.endswith(".py")):
                invalid_files.append(filename)
                continue

            if filename not in self.uploaded_files:
                self.uploaded_files[filename] = file_path

                var = tk.BooleanVar()

                cb = tk.Checkbutton(
                self.checkbox_container,
                text=filename,
                variable=var,
                bg="white",          # ✅ White checkbox
                fg="black",
                font=("Arial", 10),
                anchor="w",
                selectcolor="white",
                activebackground="white",
                highlightthickness=0
                )
            cb.pack(anchor="w", padx=10, pady=2)

            self.checkbox_vars[filename] = (var, cb)  # Store both var and widget

        if invalid_files:
            messagebox.showwarning(
                "Invalid Files",
                "Only files starting with 'test' and ending with '.py' are allowed.\n\n"
                + "\n".join(invalid_files)
            )


    def run_selected_tests(self):
        selected_files = [f for f, (var, _) in self.checkbox_vars.items() if var.get()]

        if not selected_files:
            messagebox.showwarning("No Selection", "Please select at least one test to run.")
            return

        self.output_box.config(state="normal")
        log_data = ""  # Collect log output in a string

        for filename in selected_files:
            full_path = self.uploaded_files[filename]
            header = f"\nRunning: {filename}\n{'-'*50}\n"
            self.output_box.insert(tk.END, header)
            log_data += header

            results = run_test_script(full_path)

            # Counters
            pass_count = fail_count = error_count = 0

            for fn_name, status, log in results:
                line = f"{fn_name}: {status}\n"
                self.output_box.insert(tk.END, line)
                log_data += line
                if status == "PASS":
                    pass_count += 1
                elif status == "FAIL":
                    fail_count += 1
                elif status == "ERROR":
                    error_count += 1

            summary = f"\nSummary for {filename} -> PASS: {pass_count} | FAIL: {fail_count} | ERROR: {error_count}\n"
            timestamp = f"=== Run started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n"
            self.output_box.insert(tk.END, summary + timestamp)
            log_data += summary + timestamp

        self.output_box.insert(tk.END, "\n" + "="*80 + "\n")
        log_data += "\n" + "="*80 + "\n"

        self.output_box.see(tk.END)

        # ✅ Auto-save logs to timestamped file
        os.makedirs("logs", exist_ok=True)
        log_filename = datetime.datetime.now().strftime("test_log_%Y-%m-%d_%H-%M-%S.txt")
        log_path = os.path.join("logs", log_filename)

        with open(log_path, "w") as f:
            f.write(log_data)

        messagebox.showinfo("Logs Saved", f"Logs automatically saved to:\n{log_path}")



    def clear_output(self):
        self.output_box.config(state="normal")   # Step 1: Enable editing
        self.output_box.delete(1.0, tk.END)      # Step 2: Clear all content
        self.output_box.config(state="disabled") # Step 3: Optionally disable again








    def clear_output(self):
        self.output_box.delete(1.0, tk.END)
    

    def delete_selected_scripts(self):
        to_delete = [filename for filename, (var, _) in self.checkbox_vars.items() if var.get()]

        if not to_delete:
            messagebox.showinfo("No Selection", "Please select at least one script to delete.")
            return

        for filename in to_delete:
            var, widget = self.checkbox_vars.get(filename, (None, None))
            if widget:
                widget.destroy()

            if filename in self.uploaded_files:
                del self.uploaded_files[filename]

            if filename in self.checkbox_vars:
                del self.checkbox_vars[filename]

        self.checkbox_container.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    


    def refresh_log_dropdown(self):
        import os
        log_files = sorted([
            f for f in os.listdir("logs") if f.endswith(".txt")
        ], reverse=True)

        self.log_dropdown["values"] = log_files
        if log_files:
            self.log_dropdown.set("Select a log file to view...")


    def display_selected_log(self, event=None):
        selected_file = self.log_dropdown_var.get()
        if not selected_file:
            return

        try:
            with open(f"logs/{selected_file}", "r", encoding="utf-8") as f:
                content = f.read()

            self.output_box.delete(1.0, tk.END)
            self.output_box.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read log: {e}")



    def email_report(self):
        recipient = self.email_entry.get().strip()
        if not recipient:
            messagebox.showerror("Error", "Please enter a recipient email address.")
            return

        # 1. Get the output content
        content = self.output_box.get("1.0", tk.END).strip()
        if not content:
            messagebox.showerror("Error", "No content to send.")
            return

        # 2. Convert to PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in content.splitlines():
            pdf.cell(200, 10, txt=line, ln=True)

        pdf_path = "test_report.pdf"
        pdf.output(pdf_path)

        # 3. Email it
        try:
            sender_email = "manohargc2650@gmail.com"
            sender_password = "mumnswbsgzkbsiii"  # Use App Password if Gmail
            subject = "Infotainment Test Report"

            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient
            msg["Subject"] = subject

            body = "Please find attached the infotainment test report."
            msg.attach(MIMEText(body, "plain"))

            # Attach PDF
            with open(pdf_path, "rb") as f:
                part = MIMEApplication(f.read(), _subtype="pdf")
                part.add_header("Content-Disposition", "attachment", filename="test_report.pdf")
                msg.attach(part)

            # SMTP Server (Gmail example)
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)

            messagebox.showinfo("Success", f"Report sent to {recipient} successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {e}")


    def open_log_file(self):
        file_path = filedialog.askopenfilename(
            title="Open Log File",
            filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    self.output_box.config(state="normal")
                    self.output_box.delete("1.0", tk.END)
                    self.output_box.insert(tk.END, content)
                    self.output_box.config(state="normal")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")




    


    

    