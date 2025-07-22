import tkinter as tk
from tkinter import filedialog, messagebox
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator
from core.runner import run_test_script
import os
from tkinter import filedialog, messagebox, ttk
import datetime
import subprocess
import tempfile
import sys
import io
import traceback
from tkcode import CodeEditor
from .code_editor import CodeEditor
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText


class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Infotainment Test Automation Tool")

        self.uploaded_files = {}       # filename: full_path
        self.checkbox_vars = {}        # filename: BooleanVar

      
        
       

        # Upload Button
        self.upload_button = tk.Button(
        root,
        text="📤 Upload Test Scripts",
        command=self.upload_test_scripts,
        bg="#007bff",       # Blue
        fg="white",
        activebackground="#0056b3",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=5
        )
        self.upload_button.pack(pady=10)

        # Hover effect
        self.upload_button.bind("<Enter>", lambda e: self.upload_button.config(bg="#0056b3"))
        self.upload_button.bind("<Leave>", lambda e: self.upload_button.config(bg="#007bff"))

        # # Email Entry Label + Box
        # tk.Label(root, text="Recipient Email:", font=("Arial", 12)).pack(pady=(10, 0))
        # self.email_entry = tk.Entry(root, width=50)
        # self.email_entry.pack(pady=(5, 10))

        # # Email Button
        # self.email_button = tk.Button(
        #     root,
        #     text="📧 Email Report",
        #     command=self.email_report,
        #     bg="#007bff",
        #     fg="white",
        #     activebackground="#0056b3",
        #     font=("Arial", 10, "bold"),
        #     padx=10,
        #     pady=5
        # )
        # self.email_button.pack(pady=(0, 10))











        # Frame for Checkboxes with Scrollbar
        checkbox_frame = tk.Frame(root)
        checkbox_frame.pack(padx=10, pady=5)

        self.canvas = tk.Canvas(
        checkbox_frame,
        height=200,
        width=800,
        bg="white",                # ✅ White background
        highlightthickness=0
        )

        self.scrollbar = ttk.Scrollbar(
        checkbox_frame,
        orient="vertical",
        command=self.canvas.yview
        )

        self.checkbox_container = tk.Frame(
        self.canvas,
        bg="white"                 # ✅ Container background
        )

        self.checkbox_container.bind(
        "<Configure>",
        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.checkbox_container, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")


       # Frame to hold Run & Delete buttons side by side
        action_frame = tk.Frame(root)
        action_frame.pack(pady=10)

        self.run_button = tk.Button(
        action_frame,
        text="▶️ Run Selected Tests",
        command=self.run_selected_tests,
        bg="#28a745",        # Green
        fg="white",
        activebackground="#218838",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=5
        )
        self.run_button.pack(side="left", padx=10)

        self.delete_button = tk.Button(
        action_frame,
        text="🗑️ Delete Selected Scripts",
        command=self.delete_selected_scripts,
        bg="#dc3545",        # Red
        fg="white",
        activebackground="#bd2130",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=5
        )
        self.delete_button.pack(side="left", padx=10)

        # Hover effects for Run button
        self.run_button.bind("<Enter>", lambda e: self.run_button.config(bg="#218838"))
        self.run_button.bind("<Leave>", lambda e: self.run_button.config(bg="#28a745"))

        # Hover effects for Delete button
        self.delete_button.bind("<Enter>", lambda e: self.delete_button.config(bg="#bd2130"))
        self.delete_button.bind("<Leave>", lambda e: self.delete_button.config(bg="#dc3545"))

        code_writer_btn = tk.Button(root, text="Code Writer", command=self.open_code_editor)

        code_writer_btn.pack(pady=10)

        # Frame for Save Log, Email Entry, and Send Email Button
        action_frame = tk.Frame(root)
        action_frame.pack(pady=10)

        # 💾 Save Log Button
        self.save_log_button = tk.Button(
        action_frame,
        text="💾 Save Log",
        bg="#007ACC",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        command=self.save_log_to_file
        )
        self.save_log_button.pack(side="left", padx=5)

        # 📧 Email Entry
        self.email_entry = tk.Entry(
        action_frame,
        width=30,
        font=("Segoe UI", 10)
        )
        self.email_entry.insert(0, "Enter email address")
        self.email_entry.pack(side="left", padx=5)
        self.email_entry.bind("<FocusIn>", lambda e: self.email_entry.delete(0, tk.END))

        # 📤 Send Email Button
        self.email_button = tk.Button(
        action_frame,
        text="📧 Send Email",
        bg="#28a745",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        command=self.email_report  # ← uses your existing method
        )
        self.email_button.pack(side="left", padx=5)



      

        

        # self.save_log_button = tk.Button(
        #     action_frame, text="💾 Save Log",
        #     bg="#007ACC", fg="white", font=("Segoe UI", 10, "bold"),
        #     command=self.save_log_to_file
        # )
        # self.save_log_button.pack(side="left", padx=5)

        self.log_dropdown_var = tk.StringVar()
        self.log_dropdown = ttk.Combobox(
        root, textvariable=self.log_dropdown_var,
        state="readonly", width=60
        )
        self.log_dropdown.pack(pady=5)
        self.log_dropdown.bind("<<ComboboxSelected>>", self.display_selected_log)

        
        # Output Label
        tk.Label(root, text="Test Output:", font=("Arial", 12)).pack(pady=(10, 0))

        self.output_box = tk.Text(root, height=10, width=180)
        self.output_box.pack(pady=(5, 10))

        self.clear_button = tk.Button(
        root,
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

        self.refresh_log_dropdown()

        



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

        #self.output_box.delete(1.0, tk.END)  # Clear previous output
        # Always make sure output box is writable
        self.output_box.config(state="normal")

        for filename in selected_files:
            full_path = self.uploaded_files[filename]
            self.output_box.insert(tk.END, f"\nRunning: {filename}\n{'-'*50}\n")

            results = run_test_script(full_path)

            # Individual counters per file
            pass_count = fail_count = error_count = 0

            for fn_name, status, log in results:
                self.output_box.insert(tk.END, f"{fn_name}: {status}\n")
                if status == "PASS":
                    pass_count += 1
                elif status == "FAIL":
                    fail_count += 1
                elif status == "ERROR":
                    error_count += 1

            # Show final result line for that file
            self.output_box.insert(
                tk.END,
                f"\nSummary for {filename} -> PASS: {pass_count} | FAIL: {fail_count} | ERROR: {error_count}\n"
            )
            self.output_box.insert(
                tk.END,
                f"=== Run started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n"
            )

        self.output_box.see(tk.END)
            
        #self.output_box.config(state="disabled")
        self.output_box.insert(tk.END, "\n" + "="*80 + "\n")

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

    def save_log_to_file(self):
        
        log_text = self.output_box.get(1.0, tk.END).strip()
        if not log_text:
            messagebox.showwarning("Empty Output", "There is no output to save.")
            return

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"logs/log_{timestamp}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(log_text)

        messagebox.showinfo("Log Saved", f"Log saved to {filename}")
        self.refresh_log_dropdown()


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



    


    

    