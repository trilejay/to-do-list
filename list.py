import sqlite3
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()

#check to make sure table isnt already created
check_table_sql = """
    SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'
"""

cursor.execute(check_table_sql)
#if table exists, fetches it
table_exists = cursor.fetchone()

#if it doesnt exist, create the table in sql
if not table_exists:
    create_table_sql = """
       CREATE TABLE tasks (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           task_name TEXT NOT NULL,
           task_description TEXT,
           due_date DATE,
           completed BOOLEAN NOT NULL DEFAULT 0
       );
    """

    cursor.execute(create_table_sql)

conn.commit()


#function to add task
def add_task(task_name, task_description, due_date):

    sql = "INSERT INTO tasks (task_name, task_description, due_date) VALUES (?, ? , ?)"

    cursor.execute(sql, (task_name, task_description, due_date))

    conn.commit()

    print("Your task has has been added.")

#function to view task
def view_tasks():

    #selects all tasks stored in sql table
    sql = "SELECT * FROM tasks"
    cursor.execute(sql)

    #fetches the tasks from sql table and prints them ontopython.
    #rows = each individual tasks and  columns = attributes (id key, name, description, due date)
    tasks =  cursor.fetchall()
    for task in tasks:
        print(task)

def mark_task_as_complete(task_id):
    sql = "UPDATE tasks SET completed = ? WHERE id = ?"

    cursor.execute(sql, (True, task_id))

    conn.commit()
    print("Task has been marked as completed.")

def delete_task(task_id):
    sql = "DELETE FROM tasks WHERE id = ?"

    cursor.execute(sql, (task_id,))

    conn.commit()
    print("Task has been deleted.")

def main():
    while True:
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Add Task
            task_name = input("Enter task name: ")
            task_description = input("Enter task description: ")
            due_date = input("Enter day it is due: ")
            add_task(task_name, task_description, due_date)
        elif choice == "2":
            # View Tasks
            view_tasks()
        elif choice == "3":
            # Mark Task as Completed
            task_id = input("Enter task ID to mark as completed: ")
            mark_task_as_complete(task_id)
        elif choice == "4":
            # Delete Task
            task_id = input("Enter task ID to delete: ")
            delete_task(task_id)
        elif choice == "5":
            # Exit
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

conn.close()
