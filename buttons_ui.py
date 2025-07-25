
# import tkinter as tk

# def create_buttons(left_pane, upload_cmd, run_cmd, delete_cmd,
#                    open_log_cmd, email_report_cmd, code_editor_cmd,
#                    select_all_cmd, deselect_all_cmd):
#     # === First Row Frame ===
#     top_frame = tk.Frame(left_pane)
#     top_frame.pack(anchor="w", padx=10, pady=10)

#     upload_button = tk.Button(
#         top_frame, text="📤 Upload Test Scripts", command=upload_cmd,
#         bg="#007bff", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5
#     )
#     upload_button.pack(side="left", padx=5)

#     run_button = tk.Button(
#         top_frame, text="▶️ Run Selected Tests", command=run_cmd,
#         bg="#28a745", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5
#     )
#     run_button.pack(side="left", padx=5)

#     delete_button = tk.Button(
#         top_frame, text="🗑️ Delete Selected Scripts", command=delete_cmd,
#         bg="#dc3545", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5
#     )
#     delete_button.pack(side="left", padx=5)

#     # === Second Row Frame ===
#     bottom_frame = tk.Frame(left_pane)
#     bottom_frame.pack(anchor="w", padx=10, pady=5)

#     open_log_button = tk.Button(
#         bottom_frame, text="📂 Open Log", command=open_log_cmd,
#         bg="#007ACC", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5
#     )
#     open_log_button.pack(side="left", padx=5)

#     email_entry = tk.Entry(bottom_frame, width=30, font=("Segoe UI", 10))
#     email_entry.insert(0, "Enter email address")
#     email_entry.pack(side="left", padx=5)
#     email_entry.bind("<FocusIn>", lambda e: email_entry.delete(0, tk.END))

#     email_button = tk.Button(
#         bottom_frame, text="📧 Send Email", command=email_report_cmd,
#         bg="#28a745", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5
#     )
#     email_button.pack(side="left", padx=5)

#     # === Third Row Frame ===
#     row3_frame = tk.Frame(left_pane)
#     row3_frame.pack(anchor="w", padx=10, pady=(0, 10))

#     code_writer_btn = tk.Button(
#         row3_frame, text="📝 Code Writer", command=code_editor_cmd,
#         bg="#6f42c1", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5
#     )
#     code_writer_btn.pack(side="left", padx=5)

#     select_all_btn = tk.Button(
#         row3_frame, text="Select All Scripts", command=select_all_cmd,
#         bg="orange", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5
#     )
#     select_all_btn.pack(side="left", padx=5)

#     deselect_all_btn = tk.Button(
#         row3_frame, text="Deselect All Scripts", command=deselect_all_cmd,
#         bg="gray", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5
#     )
#     deselect_all_btn.pack(side="left", padx=5)

#     return upload_button, run_button, delete_button, open_log_button, email_entry, email_button, select_all_btn, deselect_all_btn
import tkinter as tk

def create_buttons(left_pane, upload_cmd, run_cmd, delete_cmd,
                   open_log_cmd, email_report_cmd, code_editor_cmd,
                   select_all_cmd, deselect_all_cmd,generate_report_cmd,view_report_cmd):
    # === First Row Frame ===
    top_frame = tk.Frame(left_pane)
    top_frame.pack(anchor="w", padx=10, pady=10)

    upload_button = tk.Button(
        top_frame, text="📤 Upload Test Scripts", command=upload_cmd,
        bg="#007bff", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5
    )
    upload_button.pack(side="left", padx=5)

    run_button = tk.Button(
        top_frame, text="▶️ Run Selected Tests", command=run_cmd,
        bg="#28a745", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5
    )
    run_button.pack(side="left", padx=5)

    delete_button = tk.Button(
        top_frame, text="🗑️ Delete Selected Scripts", command=delete_cmd,
        bg="#dc3545", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5
    )
    delete_button.pack(side="left", padx=5)

    # === Second Row Frame (Now Code + Select Buttons) ===
    row2_frame = tk.Frame(left_pane)
    row2_frame.pack(anchor="w", padx=10, pady=5)

    code_writer_btn = tk.Button(
        row2_frame, text="📝 Code Writer", command=code_editor_cmd,
        bg="#6f42c1", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5
    )
    code_writer_btn.pack(side="left", padx=5)

    select_all_btn = tk.Button(
        row2_frame, text="Select All Scripts", command=select_all_cmd,
        bg="orange", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5
    )
    select_all_btn.pack(side="left", padx=5)

    deselect_all_btn = tk.Button(
        row2_frame, text="Deselect All Scripts", command=deselect_all_cmd,
        bg="gray", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5
    )
    deselect_all_btn.pack(side="left", padx=5)

    # === Third Row Frame (Now Log + Email) ===
    bottom_frame = tk.Frame(left_pane)
    bottom_frame.pack(anchor="w", padx=10, pady=(0, 10))

    open_log_button = tk.Button(
        bottom_frame, text="📂 Open Log", command=open_log_cmd,
        bg="#007ACC", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5
    )
    open_log_button.pack(side="left", padx=5)

    email_entry = tk.Entry(bottom_frame, width=30, font=("Segoe UI", 10))
    email_entry.insert(0, "Enter email address")
    email_entry.pack(side="left", padx=5)
    email_entry.bind("<FocusIn>", lambda e: email_entry.delete(0, tk.END))

    email_button = tk.Button(
        bottom_frame, text="📧 Send Email", command=email_report_cmd,
        bg="#28a745", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5
    )
    email_button.pack(side="left", padx=5)

        # === Fourth Row Frame (Reporting Buttons) ===
    report_frame = tk.Frame(left_pane)
    report_frame.pack(anchor="w", padx=10, pady=(0, 10))

    report_button = tk.Button(
        report_frame, text="📄 Generate Report", command=generate_report_cmd,
        bg="#17a2b8", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5
    )
    report_button.pack(side="left", padx=5)

    view_report_button = tk.Button(
        report_frame, text="📊 View Reports", command=view_report_cmd,
        bg="#6c757d", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5
    )
    view_report_button.pack(side="left", padx=5)


    return (
        upload_button,
        run_button,
        delete_button,
        open_log_button,
        email_entry,
        email_button,
        select_all_btn,
        deselect_all_btn,
        report_button,
        view_report_button 
    )
