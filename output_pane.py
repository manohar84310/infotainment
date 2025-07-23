import tkinter as tk

def create_output_pane(root, clear_callback, refresh_log_dropdown_callback):
    # Create horizontal split pane (left/right)
    pane = tk.PanedWindow(root, orient=tk.HORIZONTAL)
    pane.pack(fill=tk.BOTH, expand=True)

    # LEFT pane for UI/buttons (you'll pack frames here later)
    left_frame = tk.Frame(pane, width=400)
    pane.add(left_frame)

    # RIGHT pane for output box
    right_frame = tk.Frame(pane, bg="white", width=600)
    pane.add(right_frame)

    # Add label
    label = tk.Label(right_frame, text="Test Output:", font=("Arial", 12), bg="white")
    label.pack(pady=(10, 0), anchor="w")

    # Output Text box
    output_box = tk.Text(right_frame, height=25, width=80, bg="white")
    output_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Clear Output Button
    clear_button = tk.Button(
        right_frame,
        text="🧹 Clear Output",
        command=clear_callback,
        bg="#6c757d",
        fg="white",
        activebackground="#5a6268",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=5
    )
    clear_button.pack(pady=(0, 10), anchor="e")

    # Optionally refresh logs
    if refresh_log_dropdown_callback:
        refresh_log_dropdown_callback()

    return output_box, left_frame
