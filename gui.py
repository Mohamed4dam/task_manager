import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as messagebox
from datetime import datetime

class TaskView:
    """
    View class for the Task Reminder application GUI.

    Attributes:
        root (tk.Tk): The root Tkinter window.
        tree (ttk.Treeview): Treeview widget for displaying tasks.
        task_entry (tk.Entry): Entry widget for entering task names.
        due_date_entry (tk.Entry): Entry widget for entering due dates.
        is_completed_var (tk.BooleanVar): BooleanVar for the completion status checkbox.
        is_completed_checkbox (tk.Checkbutton): Checkbutton for indicating task completion.
        add_button (tk.Button): Button for adding tasks.
        edit_button (tk.Button): Button for editing tasks.
        clear_button (tk.Button): Button for clearing all tasks.
        controller (TaskController): The controller for handling user interactions.
    """

    def __init__(self, root):
        """
        Initialize the TaskView.

        Parameters:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("Task Reminder")
        self.root.resizable(False, False)  # Make the window not resizable

        self.tree = ttk.Treeview(root, columns=('Task', 'Due Date', 'Status'))
        self.tree.heading('#0', text='ID')
        self.tree.heading('#1', text='Task')
        self.tree.heading('#2', text='Due Date')
        self.tree.heading('#3', text='Status')
        self.tree.pack()

        self.task_entry = tk.Entry(root)
        self.task_entry.pack()

        self.due_date_entry = tk.Entry(root)
        self.due_date_entry.pack()

        self.is_completed_var = tk.BooleanVar()
        self.is_completed_checkbox = tk.Checkbutton(root, text="Is the task completed", variable=self.is_completed_var)
        self.is_completed_checkbox.pack()

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.edit_button = tk.Button(root, text="Edit Task", command=self.edit_task)
        self.edit_button.pack()

        # Add a button to clear tasks
        self.clear_button = tk.Button(root, text="Clear All Tasks", command=self.confirm_clear_tasks, bg='red')
        self.clear_button.pack()

    def add_task(self):
        """
        Add a new task based on user input.
        """
        try:
            task = self.task_entry.get()
            due_date_str = self.due_date_entry.get()

            # Basic input validation
            if not task or not due_date_str:
                raise ValueError("Task and Due Date cannot be empty.")

            # Validate the due date format
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

            is_completed = self.is_completed_var.get()
            done_status = 'Yes' if is_completed else 'No'

            self.controller.add_task({'Task': task, 'Due Date': due_date.strftime('%Y-%m-%d'), 'Done': done_status})
            self.clear_entries()
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))

    def edit_task(self):
        """
        Edit the selected task based on user input.
        """
        try:
            selected_items = self.tree.selection()
            if not selected_items:
                raise ValueError("Please select a task to edit.")

            # Check if multiple items are selected
            if len(selected_items) > 1:
                raise ValueError("Please select only one task to edit.")

            selected_item = selected_items[0]
            task_values = self.tree.item(selected_item, 'values')
            if not task_values:
                raise ValueError("Selected task is invalid.")

            task, due_date, done = task_values
            self.task_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
            self.task_entry.insert(0, task)
            self.due_date_entry.insert(0, due_date)
            self.is_completed_var.set(done == 'Yes')  # Set the checkbox based on the 'Done' status
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))

    def clear_entries(self):
        """
        Clear all input fields.
        """
        self.task_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.is_completed_var.set(False)  # Reset the checkbox

    def confirm_clear_tasks(self):
        """
        Prompt a confirmation message and clear all tasks if confirmed.
        """
        confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to clear all tasks?")
        if confirmed:
            self.controller.clear_all_tasks()
