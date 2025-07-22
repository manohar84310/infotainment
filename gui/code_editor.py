# import tkinter as tk
# from tkinter import filedialog, messagebox, ttk
# import subprocess
# import os
# import sys
# import threading
# import keyword
# import io
# import contextlib
# from tkinter import scrolledtext

# class CodeEditor(tk.Toplevel):
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.title("Python Code Editor")
#         self.geometry("1000x700")

#         self._create_widgets()
#         self._bind_events()

#     def _create_widgets(self):
#         self.paned_window = tk.PanedWindow(self, orient=tk.VERTICAL)
#         self.paned_window.pack(fill=tk.BOTH, expand=True)

#         # Toolbar
#         toolbar = tk.Frame(self)
#         toolbar.pack(fill=tk.X)
#         tk.Button(toolbar, text="Run", command=self._run_code).pack(side=tk.LEFT, padx=2)
#         tk.Button(toolbar, text="Clear Output", command=self._clear_output).pack(side=tk.LEFT, padx=2)
#         tk.Button(toolbar, text="Save", command=self._save_file).pack(side=tk.LEFT, padx=2)
#         tk.Button(toolbar, text="Open", command=self._open_file).pack(side=tk.LEFT, padx=2)

#         # Editor Area
#         editor_frame = tk.Frame(self.paned_window)
#         self.line_numbers = tk.Text(editor_frame, width=4, padx=4, takefocus=0, border=0, background='#f0f0f0', state='disabled')
#         self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

#         self.text = tk.Text(editor_frame, wrap=tk.NONE, undo=True)
#         self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

#         self.scrollbar = tk.Scrollbar(editor_frame, command=self._on_scroll)
#         self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#         self.text.config(yscrollcommand=self._on_scrollbar)

#         editor_frame.pack(fill=tk.BOTH, expand=True)
#         self.paned_window.add(editor_frame)

#         # Output Area
#         self.output = tk.Text(self.paned_window, height=10, bg="black", fg="lime", state='disabled')
#         self.paned_window.add(self.output)

#         # Autocomplete Dropdown
#         self.dropdown = tk.Listbox(self, height=5)
#         self.dropdown.bind("<Double-Button-1>", self._select_autocomplete)
#         self.dropdown_visible = False

#     def _bind_events(self):
#         self.text.bind("<KeyRelease>", self._on_key_release)
#         self.text.bind("<Button-1>", lambda e: self._hide_autocomplete())
#         self.text.bind("<Return>", lambda e: self._hide_autocomplete())
#         self.text.bind("<Tab>", self._insert_autocomplete)
#         self.text.bind("<MouseWheel>", self._on_scroll)

#     def _on_scroll(self, *args):
#         self.text.yview(*args)
#         self.line_numbers.yview(*args)

#     def _on_scrollbar(self, *args):
#         self.scrollbar.set(*args)
#         self.line_numbers.yview_moveto(args[0])

#     def run_code(self):
#         code = self.text.get("1.0", tk.END)

#         self.output.config(state=tk.NORMAL)
#         self.output.delete("1.0", tk.END)

#         stdout = io.StringIO()
#         stderr = io.StringIO()

#         try:
#             with contextlib.redirect_stdout(stdout):
#                 with contextlib.redirect_stderr(stderr):
#                     exec(code, {})
#         except Exception as e:
#             self.output.insert(tk.END, stderr.getvalue())
#             self.output.insert(tk.END, f"\n{e}")
#         else:
#             self.output.insert(tk.END, stdout.getvalue())

#         self.output.config(state=tk.DISABLED)



#     def _clear_output(self):
#         self.output.config(state='normal')
#         self.output.delete("1.0", tk.END)
#         self.output.config(state='disabled')

#     def _save_file(self):
#         file_path = filedialog.asksaveasfilename(defaultextension=".py")
#         if file_path:
#             with open(file_path, 'w') as f:
#                 f.write(self.text.get("1.0", tk.END))

#     def _open_file(self):
#         file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
#         if file_path:
#             with open(file_path, 'r') as f:
#                 self.text.delete("1.0", tk.END)
#                 self.text.insert(tk.END, f.read())

#     def _on_key_release(self, event=None):
#         self._update_line_numbers()
#         word = self._get_current_word()
#         if word:
#             matches = [k for k in keyword.kwlist if k.startswith(word)]
#             if matches:
#                 self._show_autocomplete(matches)
#             else:
#                 self._hide_autocomplete()
#         else:
#             self._hide_autocomplete()

#     def _get_current_word(self):
#         index = self.text.index(tk.INSERT)
#         line, col = map(int, index.split("."))
#         start = f"{line}.{max(0, col-20)}"
#         fragment = self.text.get(start, index)
#         return fragment.split()[-1] if fragment.strip() else ""

#     def _show_autocomplete(self, words):
#         if not self.dropdown_visible:
#             self.dropdown.place(x=100, y=100)
#             self.dropdown_visible = True
#         self.dropdown.delete(0, tk.END)
#         for w in words:
#             self.dropdown.insert(tk.END, w)

#     def _hide_autocomplete(self):
#         if self.dropdown_visible:
#             self.dropdown.place_forget()
#             self.dropdown_visible = False

#     def _insert_autocomplete(self, event):
#         if self.dropdown_visible:
#             selected = self.dropdown.get(tk.ACTIVE)
#             self.text.insert(tk.INSERT, selected[len(self._get_current_word()):])
#             self._hide_autocomplete()
#             return "break"

#     def _select_autocomplete(self, event):
#         self._insert_autocomplete(None)

#     def _update_line_numbers(self):
#         lines = self.text.get("1.0", tk.END).split("\n")
#         self.line_numbers.config(state='normal')
#         self.line_numbers.delete("1.0", tk.END)
#         for i in range(1, len(lines)):
#             self.line_numbers.insert(tk.END, f"{i}\n")
#         self.line_numbers.config(state='disabled')
import keyword
import re
import tkinter as tk
import io
import contextlib
from tkinter import filedialog
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator



class Autocomplete:
    def __init__(self, text_widget):


    
        self.text_widget = text_widget
        self.words = keyword.kwlist  # ✅ Add this line
        # ... your existing logic ...

        self.text = text_widget
        self.popup = None
        self.suggestions = sorted(set(keyword.kwlist))  # Python keywords
        self.text.bind("<KeyRelease>", self._on_key_release)

    def _hide_popup(self):
        if hasattr(self, "popup") and self.popup:
            self.popup.destroy()
            self.popup = None


    def _on_key_release(self, event=None):
        if event.keysym == "space":
            return  # Ignore space

        index = self.text.index(tk.INSERT)
        word_start = self.text.search(r'\w+$', index, regexp=True, backwards=True)
        word_end = self.text.index(f"{word_start} wordend")
        word = self.text.get(word_start, word_end)

        if word in self.words:
            self._show_popup(word)
        else:
            self._hide_popup()


    def _get_current_word(self):
        index = self.text.index(tk.INSERT)
        line = self.text.get(f"{index} linestart", index)
        match = re.search(r"(\w+)$", line)
        return match.group(1) if match else ""

    def _show_popup(self, matches, prefix):
        self._close_popup()

        try:
            x, y, _, _ = self.text.bbox(tk.INSERT)
        except:
            return

        x += self.text.winfo_rootx()
        y += self.text.winfo_rooty() + 20

        self.popup = tk.Toplevel()
        self.popup.wm_overrideredirect(True)
        self.popup.geometry(f"+{x}+{y}")

        listbox = tk.Listbox(self.popup, height=min(5, len(matches)))
        for match in matches:
            listbox.insert(tk.END, match)

        listbox.pack()
        listbox.focus_set()
        listbox.bind("<Return>", lambda e: self._insert_selection(listbox, prefix))
        listbox.bind("<Tab>", lambda e: self._insert_selection(listbox, prefix))
        listbox.bind("<Escape>", lambda e: self._close_popup())

        self.popup.listbox = listbox

    def _insert_selection(self, listbox, prefix):
        selection = listbox.get(tk.ACTIVE)
        if selection:
            self._delete_current_word(prefix)
            self.text.insert(tk.INSERT, selection)
        self._close_popup()

    def _delete_current_word(self, prefix):
        index = self.text.index(tk.INSERT)
        self.text.delete(f"{index} - {len(prefix)} chars", index)

    def _close_popup(self):
        if self.popup:
            self.popup.destroy()
            self.popup = None


class CodeEditor(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Code Editor")
        self.geometry("800x600")

        self._create_widgets()
        self.words = keyword.kwlist
        



    def _create_widgets(self):
    # Toolbar
        toolbar = tk.Frame(self)
        toolbar.pack(fill=tk.X)
        tk.Button(toolbar, text="Run", command=self._run_code_append_output).pack(side=tk.LEFT, padx=2)


        tk.Button(toolbar, text="Save", command=self._save_file).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="Clear Output", command=self._clear_output).pack(side=tk.LEFT, padx=2)

        



        # Editor frame (with line numbers + code area)
        editor_frame = tk.Frame(self)
        editor_frame.pack(fill=tk.BOTH, expand=True)

        self.line_numbers = tk.Text(editor_frame, width=4, padx=4, takefocus=0, border=0,
                                background='#f0f0f0', state='disabled')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.text = tk.Text(editor_frame, wrap=tk.NONE, undo=True)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(editor_frame, command=self.text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=scrollbar.set)


        # Syntax highlighting
        Percolator(self.text).insertfilter(ColorDelegator())

        scrollbar = tk.Scrollbar(editor_frame, command=self.text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=scrollbar.set)

        # Output area
        self.output = tk.Text(self, height=8, bg="black", fg="lime")
        self.output.pack(fill=tk.X)

        
        

        self.text.bind("<KeyRelease>", self._update_line_numbers)
        self.text.bind("<Return>", self._auto_indent)  # ✅ This should override newline and auto-indent


        # ✅ Add this line just like others
        self.autocomplete = Autocomplete(self.text)

        self._update_line_numbers()  # ✅ Call once to populate initially




    def _update_line_numbers(self, event=None):
        lines = self.text.get("1.0", tk.END).split("\n")
        self.line_numbers.config(state='normal')
        self.line_numbers.delete("1.0", tk.END)
        for i in range(1, len(lines)):
            self.line_numbers.insert(tk.END, f"{i}\n")
        self.line_numbers.config(state='disabled')

    # def _run_code(self):
    #     code = self.text.get("1.0", tk.END)
    #     self.output.config(state='normal')
    #     self.output.delete("1.0", tk.END)

    #     stdout = io.StringIO()
    #     stderr = io.StringIO()

    #     try:
    #         with contextlib.redirect_stdout(stdout):
    #             with contextlib.redirect_stderr(stderr):
    #                 exec(code, {})
    #     except Exception as e:
    #         self.output.insert(tk.END, stderr.getvalue())
    #         self.output.insert(tk.END, f"\n{e}")
    #     else:
    #         self.output.insert(tk.END, stdout.getvalue())

    #     self.output.config(state='disabled')

    def _save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py")
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.text.get("1.0", tk.END))

    def _auto_indent(self, event=None):
        current_line = self.text.get("insert linestart", "insert")
        indent = ""
        for char in current_line:
            if char in " \t":
                indent += char
            else:
                break

        if current_line.strip().endswith(":"):
            indent += "    "  # Smart indent

        self.text.insert("insert", "\n" + indent)
        self._update_line_numbers()
        return "break"
    
    def _clear_output(self):
        self.output.config(state='normal')
        self.output.delete("1.0", tk.END)
        self.output.config(state='disabled')


    def _run_code_append_output(self):
        code = self.text.get("1.0", tk.END)
        self.output.config(state='normal')

        # 👇 Move cursor to end before appending
        #self.output.insert(tk.END, "\n\n#---- Run Start ----#\n")

        stdout = io.StringIO()
        stderr = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                with contextlib.redirect_stderr(stderr):
                    exec(code, {})
    #     except Exception as e:
    #         self.output.insert(tk.END, stderr.getvalue())
    #         self.output.insert(tk.END, f"\n{e}")
    #     else:
    #         self.output.insert(tk.END, stdout.getvalue())

    #    # self.output.insert(tk.END, "\n#---- Run End ----#")
    #     self.output.config(state='disabled')

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            self.output.insert(tk.END, stderr.getvalue())
            self.output.insert(tk.END, "\nERROR!\n" + tb)
            self.output.insert(tk.END, "=== Code Exited With Errors ===\n")
        
        else:
            self.output.insert(tk.END, stdout.getvalue())
            self.output.insert(tk.END, "\n=== Code Execution Successful ===\n")

       # self.output.insert(tk.END, "\n#---- Run End ----#")
        self.output.config(state='disabled')






    
