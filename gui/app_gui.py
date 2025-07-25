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
from collections import OrderedDict
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import datetime
import os
import chardet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from tkinter import simpledialog
from report_viewer import create_report_viewer_window


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
        #self.checkbuttons = {}         # filename: Checkbutton widget
        self.checkbox_widgets = {}  # filename: Checkbutton widget
        self.test_method_results = []




        self.main_pane = tk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        self.left_pane = tk.Frame(self.main_pane, bg="white")
        self.right_pane = tk.Frame(self.main_pane, bg="white")

        self.main_pane.add(self.left_pane, width=600)   # left side
        self.main_pane.add(self.right_pane,width =450)            # right side



        
#        

        # Frame for Checkboxes with Scrollbar
        #checkbox_frame = tk.Frame(self.left_pane)
        checkbox_frame = tk.Frame(
            self.left_pane,
            bd=1,
            relief="solid",
            background="white",
            highlightbackground="black",  # outer black border
            highlightthickness=1
        )
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

        # # Report Generation Button
        # report_btn = tk.Button(
        # root, text="Generate Test Report (PDF)",
        # command=self.generate_pdf_report,
        # bg="lightblue", fg="black"
        # )
        # report_btn.pack(pady=5)

        
        self.upload_button, self.run_button, self.delete_button, self.open_log_button, self.email_entry, self.email_button, self.select_all_button,self.deselect_all_button,self.report_btn,self.view_report_btn = create_buttons(
            self.left_pane,
            self.upload_test_scripts,
            self.run_selected_tests,
            self.delete_selected_scripts,
            self.open_log_file,
            self.email_report,
            self.open_code_editor,
            self.select_all_scripts,        # NEW
            self.deselect_all_scripts,
            generate_report_cmd=self.generate_pdf_report,
            view_report_cmd=self.open_report_viewer
        )


        # self.refresh_log_dropdown()

        self.log_dropdown_var = tk.StringVar()
        self.log_dropdown = ttk.Combobox(
            root, textvariable=self.log_dropdown_var,
            state="readonly", width=60
        )
        self.refresh_log_dropdown()

     

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

    def select_all_scripts(self):
        for var in self.checkbox_vars.values():
            if isinstance(var, tk.BooleanVar):
                var.set(True)


    def deselect_all_scripts(self):
        for var in self.checkbox_vars.values():
            if isinstance(var, tk.BooleanVar):
                var.set(False)

    def open_report_viewer(self):
        from report_viewer import create_report_viewer_window  # 📁 your viewer module
        create_report_viewer_window(self.root)


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

            self.checkbox_vars[filename] = var  # Store both var and widget
            self.checkbox_widgets[filename] = cb 

        if invalid_files:
            messagebox.showwarning(
                "Invalid Files",
                "Only files starting with 'test' and ending with '.py' are allowed.\n\n"
                + "\n".join(invalid_files)
            )


    def clear_output(self):
        self.output_box.config(state="normal")   # Step 1: Enable editing
        self.output_box.delete(1.0, tk.END)      # Step 2: Clear all content
        self.output_box.config(state="disabled") # Step 3: Optionally disable again


    def clear_output(self):
        self.output_box.delete(1.0, tk.END)

    def delete_selected_scripts(self):
        to_delete = [filename for filename, var in self.checkbox_vars.items() if var.get()]

        if not to_delete:
            messagebox.showinfo("No Selection", "Please select at least one script to delete.")
            return

        for filename in to_delete:
            # Get and destroy the Checkbutton widget
            widget = self.checkbox_widgets.get(filename)
            if widget:
                widget.destroy()

            # Remove entries from dictionaries
            self.uploaded_files.pop(filename, None)
            self.checkbox_vars.pop(filename, None)
            self.checkbox_widgets.pop(filename, None)

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
            file_path = f"logs/{selected_file}"
        
        # Step 1: Read as binary
            with open(file_path, "rb") as f:
                raw_data = f.read()

        # Step 2: Detect encoding
            detected = chardet.detect(raw_data)
            encoding = detected['encoding'] or 'utf-8'  # fallback to utf-8 if detection fails

        # Step 3: Decode with replacement for any bad characters
            content = raw_data.decode(encoding, errors="replace")

        # Step 4: Show in output box
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


    import chardet

    def open_log_file(self):
        file_path = filedialog.askopenfilename(
            title="Open Log File",
            filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            try:
            # Try UTF-8 first
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
            except UnicodeDecodeError:
                try:
                # Detect encoding using chardet
                    with open(file_path, "rb") as raw_file:
                        raw_data = raw_file.read()
                        detected_encoding = chardet.detect(raw_data)['encoding']
                        content = raw_data.decode(detected_encoding)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to read log file: {e}")
                    return

        # Display in GUI
            self.output_box.config(state="normal")
            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, content)
            self.output_box.config(state="normal")



    def save_structured_log(self, script_name, results, adb_logs):
        import datetime
        import os

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_lines = []

        log_lines.append("=" * 60)
        log_lines.append(f"🧪 Test Script      : {script_name}")
        log_lines.append(f"🕒 Log Timestamp    : {timestamp}")
        log_lines.append("=" * 60)
        log_lines.append("")

        failed_methods = [m for m, r in results.items() if r == "FAIL"]
        if failed_methods:
            log_lines.append("❌ Failed Methods:")
            log_lines.append("-" * 60)
            for i, method in enumerate(failed_methods, 1):
                log_lines.append(f"{i}. {method}")
            log_lines.append("-" * 60)
            log_lines.append("")

        log_lines.append("📦 Summary:")
        log_lines.append(f"- Total Methods     : {len(results)}")
        log_lines.append(f"- Passed            : {sum(1 for r in results.values() if r == 'PASS')}")
        log_lines.append(f"- Failed            : {sum(1 for r in results.values() if r == 'FAIL')}")
        log_lines.append("")
        log_lines.append("=" * 60)
        log_lines.append("")

        if adb_logs:
            log_lines.append("🔍 Logs per Failed Method:\n")
            for method, log in adb_logs.items():
                log_lines.append("-" * 60)
                log_lines.append(f"🧪 Method: {method}")
                log_lines.append("[BEGIN ADB LOG]")
                log_lines.append(log.strip())
                log_lines.append("[END ADB LOG]")
                log_lines.append("")

            log_lines.append("=" * 60)

     # Save to file
        os.makedirs("logs", exist_ok=True)
        fname = f"logcat_{script_name}_failed_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path = os.path.join("logs", fname)

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(log_lines))

        return fname




    def run_selected_tests(self):
        self.test_start_time = datetime.datetime.now()
        selected_files = [f for f, var in self.checkbox_vars.items() if var.get()]

        if not selected_files:
            messagebox.showwarning("No Selection", "Please select at least one test to run.")
            return

        self.output_box.config(state="normal")
        log_data = ""

        for filename in selected_files:
            full_path = self.uploaded_files[filename]
            header = f"\nRunning: {filename}\n{'-'*50}\n"
            self.output_box.insert(tk.END, header)
            log_data += header

            raw_results = run_test_script(full_path)

            pass_count = fail_count = error_count = 0
            summary_results = OrderedDict()
            adb_logs = {}
            self.test_end_time = datetime.datetime.now()

            for fn_name, status, log in raw_results:
                line = f"{fn_name}: {status}\n"
                # Extract test case ID from method name like TC_101_check_bt_connection
               # Extract test case ID and format name nicely
                # Default values
                test_case_id = "N/A"
                display_name = fn_name

                # Extract test case ID and clean name
                if fn_name.startswith("TC_") and "_" in fn_name:
                    parts = fn_name.split("_", 2)  # Split into max 3 parts
                    if len(parts) >= 3:
                        test_case_id = parts[1]
                        display_name = f"TC_{parts[1]}: {parts[2]}"
                    elif len(parts) == 2:
                        test_case_id = parts[1]
                        display_name = f"TC_{parts[1]}"

                self.test_method_results.append({
                    "method_name": display_name,
                    "test_case_id": test_case_id,
                    "status": status
                })



                self.output_box.insert(tk.END, line)
                log_data += line

                summary_results[fn_name] = status

                if status == "PASS":
                    pass_count += 1
                elif status in ["FAIL", "ERROR"]:
                    fail_count += 1 if status == "FAIL" else 0
                    error_count += 1 if status == "ERROR" else 0

                    # 🔄 Replaces old self.save_adb_log_file(fn_name)
                    try:
                        import subprocess
                        adb_raw = subprocess.check_output(["adb", "logcat", "-d", "-v", "time"], timeout=5)
                        adb_logs[fn_name] = adb_raw.decode("utf-8", errors="ignore")
                    except Exception as e:
                        adb_logs[fn_name] = f"Could not capture ADB log: {str(e)}"

            summary = f"\nSummary for {filename} -> PASS: {pass_count} | FAIL: {fail_count} | ERROR: {error_count}\n"
            timestamp = f"=== Run started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n"
            self.output_box.insert(tk.END, summary + timestamp)
            log_data += summary + timestamp

            # ✅ Save ADB log only if failures happened
            if adb_logs:
                saved_file = self.save_structured_log(filename, summary_results, adb_logs)
                note = f"📁 Structured ADB log saved: {saved_file}\n"
                self.output_box.insert(tk.END, note)



    def generate_pdf_report(self):
        if not self.test_method_results:
            messagebox.showinfo("No Data", "No test results available to generate report.")
            return
        
        input_data = {}

        fields = [
        ("Tester Name", "tester_name"),
        ("Software Version", "software_version"),
        ("Hardware Version", "hardware_version"),
        ("Hardware Connected", "hardware_connected")
        ]

        for label, key in fields:
            value = simpledialog.askstring("Input", f"Enter {label}:", parent=self.root)
            if value is None:  # User cancelled
                messagebox.showwarning("Cancelled", "Report generation cancelled.")
                return
            input_data[key] = value


        # Save to self for later use in PDF
        self.tester_name = input_data["tester_name"]
        self.software_version = input_data["software_version"]
        self.hardware_version = input_data["hardware_version"]
        self.hardware_connected = input_data["hardware_connected"]


        # ========== 1. SETUP ==========
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Test_Report_{now}.pdf"
        reports_dir = "reports"
        os.makedirs(reports_dir, exist_ok=True)
        filepath = os.path.join(reports_dir, filename)

        styles = getSampleStyleSheet()
        content = []

        # ========== 2. HEADER DATA ==========
        tester_name = self.tester_name  # Set via GUI
        sw_version = self.software_version  # Set via GUI
        hw_version = self.hardware_version  # Set via GUI
        hw_connected = self.hardware_connected  # Set via GUI
        test_start_time = self.test_start_time.strftime("%d-%m-%Y %H:%M:%S")  # Set when test starts
        test_end_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")  # Set now

        header_data = [
            ["Tester Name", tester_name],
            ["Date of Test start", test_start_time],
            ["Date of Test Completion", test_end_time],
            ["Software Version", sw_version],
            ["Hardware Version", hw_version],
            ["Hardware connected", hw_connected]
        ]

        header_table = Table(header_data, colWidths=[150, 350])
        header_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (1, 0), colors.lightblue),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ]))

        content.append(Paragraph("Infotainment System Test Report", styles['Heading2']))
        content.append(Spacer(1, 12))
        content.append(header_table)
        content.append(Spacer(1, 12))

        # ========== 3. TEST RESULT SUMMARY ==========
        pass_count = sum(1 for r in self.test_method_results if r['status'].upper() == 'PASS')
        fail_count = sum(1 for r in self.test_method_results if r['status'].upper() == 'FAIL')
        total_count = len(self.test_method_results)

        summary_data = [
            ["Test Results", "Test Result Count"],
            ["Pass", pass_count],
            ["Fail", fail_count],
            ["Total Count", total_count],
        ]

        summary_table = Table(summary_data, colWidths=[200, 150])
        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
            ("BACKGROUND", (0, 1), (-1, 1), colors.lightgreen),
            ("BACKGROUND", (0, 2), (-1, 2), colors.red),
            ("BACKGROUND", (0, 3), (-1, 3), colors.lightgrey),
        ]))

        content.append(summary_table)
        content.append(Spacer(1, 12))

        # ========== 4. DETAILED TEST CASE RESULTS ==========
        detailed_data = [["Sl. No", "Test Case Name with ID", "Result"]]
        for idx, result in enumerate(self.test_method_results, start=1):
            name_with_id = f"{result['method_name']} (TC_ID: {result['test_case_id']})"
            detailed_data.append([idx, name_with_id, result['status']])

        detail_table = Table(detailed_data, colWidths=[50, 350, 80])
        detail_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ]))

        content.append(detail_table)

        # ========== 5. SAVE PDF ==========
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        doc.build(content)

        self.last_pdf_report_path = filepath
        messagebox.showinfo("Report Generated", f"PDF Report saved as:\n{filepath}")







    


    

    