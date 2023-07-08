import tkinter as tk
from tkinter import messagebox

import pickle

class Notebook:
    def __init__(self, file):
        self.file = file
        self.notes = self.load_notes()

    def add_note(self, title, content):
        self.notes[title] = content
        self.save_notes()

    def delete_note(self, title):
        if title in self.notes:
            del self.notes[title]
            self.save_notes()
            return True
        else:
            return False

    def show_notes(self):
        return self.notes

    def save_notes(self):
        with open(self.file, 'wb') as f:
            pickle.dump(self.notes, f)

    def load_notes(self):
        try:
            with open(self.file, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}

class NotebookApp(tk.Tk):
    def __init__(self, notebook):
        super().__init__()

        self.notebook = notebook
        self.title("Notebook App")

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Notebook App", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        self.note_frame = tk.Frame(self)
        self.note_frame.pack(padx=20, pady=10)

        self.note_listbox = tk.Listbox(self.note_frame, width=40)
        self.note_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.note_scrollbar = tk.Scrollbar(self.note_frame)
        self.note_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.note_listbox.config(yscrollcommand=self.note_scrollbar.set)
        self.note_scrollbar.config(command=self.note_listbox.yview)

        self.refresh_notes()

        self.note_listbox.bind("<<ListboxSelect>>", self.on_note_select)

        self.view_button = tk.Button(self, text="View Note", command=self.view_note)
        self.view_button.pack(pady=5)

        self.add_button = tk.Button(self, text="Add Note", command=self.show_add_note_window)
        self.add_button.pack(pady=5)

        self.delete_button = tk.Button(self, text="Delete Note", command=self.delete_note)
        self.delete_button.pack(pady=5)

    def refresh_notes(self):
        self.note_listbox.delete(0, tk.END)
        notes = self.notebook.show_notes()
        for title in notes:
            self.note_listbox.insert(tk.END, title)

    def show_add_note_window(self):
        self.add_note_window = tk.Toplevel(self)
        self.add_note_window.title("Add Note")

        self.add_title_label = tk.Label(self.add_note_window, text="Title:")
        self.add_title_label.pack()

        self.add_title_entry = tk.Entry(self.add_note_window)
        self.add_title_entry.pack(pady=5)

        self.add_content_label = tk.Label(self.add_note_window, text="Content:")
        self.add_content_label.pack()

        self.add_content_text = tk.Text(self.add_note_window, height=5, width=30)
        self.add_content_text.pack(pady=5)

        self.add_button = tk.Button(self.add_note_window, text="Add", command=self.add_note)
        self.add_button.pack(pady=5)

    def add_note(self):
        title = self.add_title_entry.get()
        content = self.add_content_text.get("1.0", tk.END).strip()

        if title and content:
            self.notebook.add_note(title, content)
            self.refresh_notes()
            self.add_note_window.destroy()
            messagebox.showinfo("Success", "Note added successfully!")
        else:
            messagebox.showerror("Error", "Please enter a title and content for the note.")

    def on_note_select(self, event):
        selected_index = self.note_listbox.curselection()
        if selected_index:
            self.selected_note = self.note_listbox.get(selected_index)
        else:
            self.selected_note = None

    def view_note(self):
        if self.selected_note:
            view_window = tk.Toplevel(self)
            view_window.title("View Note")

            note_content = self.notebook.show_notes()[self.selected_note]

            note_label = tk.Label(view_window, text=f"Title: {self.selected_note}\n\nContent:\n{note_content}", font=("Arial", 12))
            note_label.pack(padx=10, pady=10)
        else:
            messagebox.showerror("Error", "Please select a note to view.")

    def delete_note(self):
        if self.selected_note:
            confirmed = messagebox.askyesno("Confirm", "Are you sure you want to delete this note?")
            if confirmed:
                success = self.notebook.delete_note(self.selected_note)
                if success:
                    self.refresh_notes()
                    messagebox.showinfo("Success", "Note deleted successfully!")
                else:
                    messagebox.showerror("Error", "Note not found.")
        else:
            messagebox.showerror("Error", "Please select a note to delete.")

if __name__ == '__main__':
    notebook = Notebook("notes.pkl")
    app = NotebookApp(notebook)
    app.mainloop()
