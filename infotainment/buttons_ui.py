import tkinter as tk


def create_buttons(left_pane, upload_cmd, run_cmd, delete_cmd, open_log_cmd, email_report_cmd, code_editor_cmd):
    # === First Row Frame ===
    top_frame = tk.Frame(left_pane)
    top_frame.pack(anchor="w", padx=10, pady=10)  # <-- anchor to the west (left)

    upload_button = tk.Button(
        top_frame,
        text="📤 Upload Test Scripts",
        command=upload_cmd,
        bg="#007bff", fg="white",
        font=("Arial", 10, "bold"),
        padx=10, pady=5
    )
    upload_button.pack(side="left", padx=5)

    run_button = tk.Button(
        top_frame,
        text="▶️ Run Selected Tests",
        command=run_cmd,
        bg="#28a745", fg="white",
        font=("Arial", 10, "bold"),
        padx=10, pady=5
    )
    run_button.pack(side="left", padx=5)

    delete_button = tk.Button(
        top_frame,
        text="🗑️ Delete Selected Scripts",
        command=delete_cmd,
        bg="#dc3545", fg="white",
        font=("Arial", 10, "bold"),
        padx=10, pady=5
    )
    delete_button.pack(side="left", padx=5)

    # === Second Row Frame ===
    bottom_frame = tk.Frame(left_pane)
    bottom_frame.pack(anchor="w", padx=10, pady=5)  # <-- anchor to the west (left)

    open_log_button = tk.Button(
        bottom_frame,
        text="📂 Open Log",
        command=open_log_cmd,
        bg="#007ACC", fg="white",
        font=("Segoe UI", 10, "bold"),
        padx=10, pady=5
    )
    open_log_button.pack(side="left", padx=5)

    email_entry = tk.Entry(
        bottom_frame,
        width=30,
        font=("Segoe UI", 10)
    )
    email_entry.insert(0, "Enter email address")
    email_entry.pack(side="left", padx=5)
    email_entry.bind("<FocusIn>", lambda e: email_entry.delete(0, tk.END))

    email_button = tk.Button(
        bottom_frame,
        text="📧 Send Email",
        command=email_report_cmd,
        bg="#28a745", fg="white",
        font=("Segoe UI", 10, "bold"),
        padx=10, pady=5
    )
    email_button.pack(side="left", padx=5)


    # Row 3 - Code Writer Button
    row3_frame = tk.Frame(left_pane)
    row3_frame.pack(anchor="w", padx=10, pady=(0, 10))

    code_writer_btn = tk.Button(
    row3_frame,
    text="📝 Code Writer",
    command=code_editor_cmd,   # ✅ Now wired properly
    bg="#6f42c1",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    padx=10,
    pady=5
    )
    code_writer_btn.pack(side="left")



    # Return all buttons/entry (optional: helpful if you want access to them)
    return upload_button, run_button, delete_button, open_log_button, email_entry, email_button
