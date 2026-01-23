# Phase I Specification - Evolution of Todo

**Scope**: In-memory Python console application. Single user. No persistence beyond runtime.

## 1. Features & User Stories

### Feature 1: Add Task
- **User Story**: As a user, I want to add a new task so that I can remember what to do.
- **Details**: User enters a description. System assigns a unique ID and default status (Incomplete).

### Feature 2: View Task List
- **User Story**: As a user, I want to view all my tasks so that I can see what is pending or completed.
- **Details**: Displays a table or list of tasks with ID, Description, and Status.

### Feature 3: Update Task
- **User Story**: As a user, I want to update the description of a task in case I made a mistake or details changed.
- **Details**: User selects task by ID and provides new description.

### Feature 4: Delete Task
- **User Story**: As a user, I want to remove a task that is no longer relevant.
- **Details**: User selects task by ID to remove it permanently from memory.

### Feature 5: Mark Task Complete / Incomplete
- **User Story**: As a user, I want to toggle a task's status so I can track my progress.
- **Details**: User selects task by ID and changes status to Complete (or back to Incomplete).

## 2. Data Model
- **Task**:
    - `id`: Integer (Auto-incrementing, starting from 1)
    - `description`: String (Non-empty)
    - `status`: Enum/String ("Incomplete", "Complete") - Default: "Incomplete"
- **Storage**:
    - List or Dictionary in memory.
    - No database or file persistence.

## 3. CLI Interaction Flow
1.  **Start Application**: Display "Evolution of Todo (Phase I)" banner.
2.  **Main Menu**: Loop showing options:
    1.  Add Task
    2.  List Tasks
    3.  Update Task
    4.  Delete Task
    5.  Mark Task Complete/Incomplete
    6.  Exit
3.  **Action Execution**:
    - Prompt for necessary input (e.g., Description, ID).
    - Perform action.
    - Show success/error message.
    - Return to Main Menu.

## 4. Acceptance Criteria
1.  Application starts and shows menu.
2.  Can add a task and see it in the list.
3.  Can update a task's description.
4.  Can delete a task and it disappears from the list.
5.  Can mark a task complete and see the status change.
6.  Application exits cleanly when "Exit" is selected.
7.  All data is lost when application restarts (In-memory verification).

## 5. Error Handling / Edge Cases
- **Invalid Menu Option**: Show error "Invalid option, please try again."
- **Empty Description**: "Description cannot be empty."
- **Invalid ID (Non-numeric)**: "Invalid ID format."
- **ID Not Found**: "Task with ID [X] not found."
- **Empty Task List**: "No tasks found." (When viewing or trying to operate on tasks).
