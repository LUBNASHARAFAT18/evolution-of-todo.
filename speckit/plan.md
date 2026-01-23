# Phase I Technical Plan - Evolution of Todo

This plan describes HOW Phase I will be implemented in Python, adhering strictly to the Specification and Global Constitution.

## 1. Application Structure
- **File**: `main.py` (Single file as per "High-level application structure" suggestion).
- **Entry Point**: `if __name__ == "__main__": main()` block.
- **Architecture**:
    - **Data Layer**: In-memory list.
    - **Logic Layer**: Functions for CRUD operations.
    - **Presentation Layer**: CLI loop and input/print functions.

## 2. Data Structures
- **Tasks Storage**: A global list of dictionaries.
    ```python
    # Example structure
    tasks = [
        {"id": 1, "description": "Buy milk", "status": "Incomplete"},
        {"id": 2, "description": "Walk dog", "status": "Complete"}
    ]
    ```
- **ID Generation**: A global counter variable (e.g., `current_id = 0`) incremented on each add.

## 3. Control Flow
1.  Initialize empty `tasks` list and `current_id` counter.
2.  Enter `while True:` loop.
3.  Print Menu options.
4.  Get user input (`input("> ")`).
5.  Match input to function calls:
    - "1" -> `add_task_ui()`
    - "2" -> `view_tasks_ui()`
    - "3" -> `update_task_ui()`
    - "4" -> `delete_task_ui()`
    - "5" -> `toggle_status_ui()`
    - "6" -> `sys.exit()`
6.  Handle invalid input with `else:` block printing error.

## 4. Separation of Responsibilities
To maintain clean architecture even in a single file, we will separate Logic from UI.

### Logic Functions (Pure-ish)
- `add_task(description)`: Returns new task dict.
- `get_all_tasks()`: Returns list of tasks.
- `find_task(task_id)`: Returns task dict or None.
- `delete_task_id(task_id)`: Returns boolean success.
- `update_task_desc(task_id, new_desc)`: Returns boolean success/updated task.
- `toggle_task_status(task_id)`: Returns boolean success/updated status.

### UI Functions (Side-effects)
- `add_task_ui()`: Prompts for desc, calls logic, prints result.
- `view_tasks_ui()`: Calls logic, formats and prints table.
- `update_task_ui()`: Prompts for ID and desc, calls logic.
- ... etc.

## 5. Error Handling Strategy
- **Input Validation**: `try/except ValueError` when parsing IDs.
- **Logic Validation**: Check if description is empty. Check if ID exists.
- **User Feedback**: Print clear messages (e.g., "Error: Task ID not found") without crashing.

## 6. Constraints Check
- No Database imports.
- No File I/O operations.
- Pure Python 3.13+ syntax.
