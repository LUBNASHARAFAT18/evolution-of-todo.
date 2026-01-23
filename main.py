import sys

# --- Data Store ---
tasks = []
current_id = 0

# --- Logic Layer ---

def add_task_logic(description):
    """Adds a new task and returns it."""
    global current_id
    current_id += 1
    new_task = {
        "id": current_id,
        "description": description,
        "status": "Incomplete"
    }
    tasks.append(new_task)
    return new_task

def get_all_tasks():
    """Returns the list of all tasks."""
    return tasks

def find_task(task_id):
    """Returns a task dictionary by ID, or None if not found."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def update_task_logic(task_id, new_description):
    """Updates a task's description. Returns True if successful, False otherwise."""
    task = find_task(task_id)
    if task:
        task["description"] = new_description
        return True
    return False

def delete_task_logic(task_id):
    """Deletes a task by ID. Returns True if successful, False otherwise."""
    task = find_task(task_id)
    if task:
        tasks.remove(task)
        return True
    return False

def toggle_status_logic(task_id):
    """Toggles task status. Returns new status string if successful, None otherwise."""
    task = find_task(task_id)
    if task:
        if task["status"] == "Incomplete":
            task["status"] = "Complete"
        else:
            task["status"] = "Incomplete"
        return task["status"]
    return None

# --- UI Layer ---

def print_banner():
    print("\n" + "="*30)
    print("   Evolution of Todo (Phase I)")
    print("="*30)

def print_menu():
    print("\nMain Menu:")
    print("1. Add Task")
    print("2. View Task List")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete/Incomplete")
    print("6. Exit")

def get_valid_id(prompt_text):
    """Prompts for ID until valid integer is entered."""
    while True:
        val = input(prompt_text)
        if val.isdigit():
            return int(val)
        print("Error: Invalid ID. Please enter a number.")

def add_task_ui():
    print("\n--- Add Task ---")
    description = input("Enter task description: ").strip()
    if not description:
        print("Error: Description cannot be empty.")
        return
    task = add_task_logic(description)
    print(f"Success: Task added with ID {task['id']}.")

def view_tasks_ui():
    print("\n--- Task List ---")
    all_tasks = get_all_tasks()
    if not all_tasks:
        print("No tasks found.")
    else:
        print(f"{'ID':<5} {'Status':<12} {'Description'}")
        print("-" * 40)
        for task in all_tasks:
            # Simple checkmark viz?
            status = task['status']
            print(f"{task['id']:<5} {status:<12} {task['description']}")

def update_task_ui():
    print("\n--- Update Task ---")
    task_id = get_valid_id("Enter Task ID to update: ")
    task = find_task(task_id)
    if not task:
        print(f"Error: Task with ID {task_id} not found.")
        return
    
    new_desc = input(f"Enter new description (current: {task['description']}): ").strip()
    if not new_desc:
        print("Error: Description cannot be empty.")
        return
    
    if update_task_logic(task_id, new_desc):
        print("Success: Task updated.")

def delete_task_ui():
    print("\n--- Delete Task ---")
    task_id = get_valid_id("Enter Task ID to delete: ")
    if delete_task_logic(task_id):
        print(f"Success: Task {task_id} deleted.")
    else:
        print(f"Error: Task with ID {task_id} not found.")

def toggle_status_ui():
    print("\n--- Toggle Status ---")
    task_id = get_valid_id("Enter Task ID to toggle status: ")
    new_status = toggle_status_logic(task_id)
    if new_status:
        print(f"Success: Task {task_id} is now {new_status}.")
    else:
        print(f"Error: Task with ID {task_id} not found.")

def main():
    print_banner()
    while True:
        print_menu()
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            add_task_ui()
        elif choice == "2":
            view_tasks_ui()
        elif choice == "3":
            update_task_ui()
        elif choice == "4":
            delete_task_ui()
        elif choice == "5":
            toggle_status_ui()
        elif choice == "6":
            print("Exiting application. Goodbye!")
            sys.exit()
        else:
            print("Error: Invalid option, please try again.")

if __name__ == "__main__":
    main()
