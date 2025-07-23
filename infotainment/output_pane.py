# # import tkinter as tk

# # def create_output_pane(root, clear_callback, refresh_log_dropdown_callback):
# #     # Horizontal split: left (for controls), right (for output)
# #     pane = tk.PanedWindow(root, orient=tk.HORIZONTAL)
# #     pane.pack(fill=tk.BOTH, expand=True)

# #     # LEFT pane for test controls
# #     left_frame = tk.Frame(pane, width=400)
# #     pane.add(left_frame)

# #     # >>> Add your checkboxes, buttons, etc. INSIDE left_frame like this:
# #     tk.Label(left_frame, text="Test Scripts").pack(anchor="w", padx=10, pady=(10, 0))
# #     # (You can pack your listbox, checkbox container, editor, etc. here.)

# #     # RIGHT pane for test output
# #     right_frame = tk.Frame(pane, bg="white", width=600)
# #     pane.add(right_frame)

# #     # Create vertical container inside right_frame
# #     vertical_frame = tk.Frame(right_frame, bg="white")
# #     vertical_frame.pack(fill=tk.BOTH, expand=True, anchor="n")  # anchor top

# #     # Add label
# #     label = tk.Label(vertical_frame, text="Test Output:", font=("Arial", 12), bg="white")
# #     label.pack(pady=(10, 0), anchor="w")

# #     # Output Text box
# #     output_box = tk.Text(vertical_frame, bg="white")
# #     output_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# #     # Clear Output Button
# #     clear_button = tk.Button(
# #         vertical_frame,
# #         text="🧹 Clear Output",
# #         command=clear_callback,
# #         bg="#6c757d",
# #         fg="white",
# #         activebackground="#5a6268",
# #         font=("Arial", 10, "bold"),
# #         padx=10,
# #         pady=5
# #     )
# #     clear_button.pack(pady=(0, 10), anchor="e")


# #     if refresh_log_dropdown_callback:
# #         refresh_log_dropdown_callback()

# #     return output_box, left_frame

# import tkinter as tk

# def create_output_pane(root, clear_callback, refresh_log_dropdown_callback):
#     # Create horizontal split pane
#     pane = tk.PanedWindow(root, orient=tk.HORIZONTAL)
#     pane.pack(fill=tk.BOTH, expand=True)

#     # LEFT pane
#     left_frame = tk.Frame(pane, width=400)
#     pane.add(left_frame)

#     # RIGHT pane
#     right_frame = tk.Frame(pane, bg="white")
#     pane.add(right_frame)

#     # ✅ Use grid for perfect top alignment
#     right_frame.grid_rowconfigure(1, weight=1)
#     right_frame.grid_columnconfigure(0, weight=1)

#     # Label at top
#     label = tk.Label(right_frame, text="Test Output:", font=("Arial", 12), bg="white")
#     label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))

#     # Output box in middle, expands fully
#     output_box = tk.Text(right_frame, bg="white", wrap=tk.WORD)
#     output_box.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

#     # Clear button at bottom right
#     clear_button = tk.Button(
#         right_frame,
#         text="🧹 Clear Output",
#         command=clear_callback,
#         bg="#6c757d",
#         fg="white",
#         activebackground="#5a6268",
#         font=("Arial", 10, "bold"),
#         padx=10,
#         pady=5
#     )
#     clear_button.grid(row=2, column=0, sticky="e", padx=10, pady=(0, 10))

#     # Optional log dropdown refresh
#     if refresh_log_dropdown_callback:
#         refresh_log_dropdown_callback()

#     return output_box, left_frame

import tkinter as tk

def create_output_pane(root, clear_callback, refresh_log_dropdown_callback):
    # Create horizontal split pane
    pane = tk.PanedWindow(root, orient=tk.HORIZONTAL)
    pane.pack(fill=tk.BOTH, expand=True)

    # LEFT pane for UI/buttons
    left_frame = tk.Frame(pane, width=400, bg="white")
    pane.add(left_frame)

    # RIGHT pane for output
    right_frame = tk.Frame(pane, bg="white")
    pane.add(right_frame)

    # 👇 Frame to hold output box & button (packs from top)
    # output_container = tk.Frame(right_frame, bg="white")
    # output_container.pack(fill="both", expand=True, anchor="n")  # anchor to top

    # label = tk.Label(output_container, text="Test Output:", font=("Arial", 12), bg="white")
    # label.pack(pady=(10, 0), anchor="w")

    # output_box = tk.Text(output_container, height=25, width=80, bg="white")
    # output_box.pack(padx=10, pady=10, fill="both", expand=True)

    # clear_button = tk.Button(
    #     output_container,
    #     text="🧹 Clear Output",
    #     command=clear_callback,
    #     bg="#6c757d",
    #     fg="white",
    #     activebackground="#5a6268",
    #     font=("Arial", 10, "bold"),
    #     padx=10,
    #     pady=5
    # )
    # clear_button.pack(pady=(0, 10), anchor="e")

    if refresh_log_dropdown_callback:
        refresh_log_dropdown_callback()

    return left_frame, right_frame

