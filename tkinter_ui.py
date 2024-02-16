import tkinter as tk
from list import add_task, view_tasks, mark_task_as_complete, delete_task
import sqlite3
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()

class ToDoAppUI:
    def __init__(self, master):
        self.master = master
        master.title("To-Do List App")

        self.label = tk.Label(master, text="Keep Busy!")
        self.label.pack()

        self.add_button = tk.Button(master, text="Add Task", command=self.create_task_window)
        self.add_button.pack()

        self.view_button = tk.Button(master, text="View Tasks", command=self.view_tasks_ui)
        self.view_button.pack()

        self.mark_button = tk.Button(master, text="Mark Task as Completed", command=self.mark_task_completed)
        self.mark_button.pack()

        self.delete_button = tk.Button(master, text="Delete Task", command=self.open_delete_window)
        self.delete_button.pack()

    def create_task_window(self):
        add_task_window = tk.Toplevel(self.master)
        add_task_window.title("Add Task")

        task_name_label = tk.Label(add_task_window, text="Task Name:")
        task_name_label.pack()
        task_name_entry = tk.Entry(add_task_window)
        task_name_entry.pack()

        task_description_label = tk.Label(add_task_window, text="Task Description:")
        task_description_label.pack()
        task_description_entry = tk.Entry(add_task_window)
        task_description_entry.pack()

        due_date_label = tk.Label(add_task_window, text="Due Date:")
        due_date_label.pack()
        due_date_entry = tk.Entry(add_task_window)
        due_date_entry.pack()

        add_button = tk.Button(add_task_window, text="Add Task",
                               command=lambda: self.add_task(task_name_entry.get(),
                                                             task_description_entry.get(), due_date_entry.get()))
        add_button.pack()
        add_button.pack()
    def add_task(self, task_name, task_description, due_date):
        add_task(task_name, task_description, due_date)
        print("Task has been added.")

    def view_tasks_ui(self):
        view_tasks_window = tk.Toplevel(self.master)
        view_tasks_window.title("View Tasks")
        tasks_label = tk.Label(view_tasks_window, text="Tasks:")
        tasks_label.pack()

        tasks_text_display = tk.Text(view_tasks_window, height=10, width=50)
        tasks_text_display.pack()

        tasks = view_tasks()

        for task in tasks:
            tasks_text_display.insert(tk.END, f"{task}\n")

        tasks_text_display.config(state=tk.DISABLED)

    def mark_task_completed(self):
        mark_tasks_window = tk.Toplevel(self.master)
        mark_tasks_window.title("Mark Tasks as Completed")

        # Retrieve tasks from the database
        sql = "SELECT * FROM tasks"
        cursor.execute(sql)
        tasks = cursor.fetchall()

        for task in tasks:
            task_id, task_name, task_description, due_date, completed = task
            task_label = tk.Label(mark_tasks_window, text=f"{task_name} - {task_description}")
            task_label.pack()

            # Create a button to mark the task as completed
            mark_button = tk.Button(mark_tasks_window, text="Mark as Completed",
                                    command=lambda id=task_id: self.mark_single_task_completed(id))
            mark_button.pack()

    def mark_task_completed(self):
        mark_tasks_window = tk.Toplevel(self.master)
        mark_tasks_window.title("Mark Tasks as Completed")

        sql = "SELECT * FROM tasks"
        cursor.execute(sql)
        tasks = cursor.fetchall()

        for task in tasks:
            task_id, task_name, task_description, due_date, completed = task
            task_label = tk.Label(mark_tasks_window, text=f"{task_name} - {task_description}")
            task_label.pack()

            # Create a button to mark the task as completed
            mark_button = tk.Button(mark_tasks_window, text="Mark as Completed",
                                    command=lambda id=task_id: self.mark_single_task_completed(id))
            mark_button.pack()

    def mark_single_task_completed(self, task_id):
        # Update the task status in the database
        sql = "UPDATE tasks SET completed = 1 WHERE id = ?"
        cursor.execute(sql, (task_id,))
        conn.commit()

    def delete_task(self,task_id):
        delete_task(task_id)  # Delete the task from the database
    def open_delete_window(self):
        delete_window = tk.Toplevel(self.master)
        delete_window.title("Delete Tasks")

        tasks = view_tasks()  # Get the list of tasks from the database

        for task_id, task_name, task_description, due_date, completed in tasks:
            task_label = tk.Label(delete_window, text=f"{task_name} - {task_description} - {due_date}")
            task_label.pack()

            delete_button = tk.Button(delete_window, text="Delete", command=lambda id=task_id: self.delete_task(id))
            delete_button.pack()


root = tk.Tk()
app = ToDoAppUI(root)
root.mainloop()

