# Phase I Implementation Tasks

Derived from `speckit/plan.md` and `speckit/spec.md`.

## Setup & Data Model
- [ ] **TASK-01**: Initialize `main.py` with basic structure and "Evolution of Todo" banner.
- [ ] **TASK-02**: Implement in-memory data storage (global `tasks` list and `current_id`).
- [ ] **TASK-03**: Create helper function `find_task(task_id)` to retrieve tasks safely.

## Core Logic (CRUD)
- [ ] **TASK-04**: Implement `add_task_logic(description)` function.
- [ ] **TASK-05**: Implement `delete_task_logic(task_id)` function.
- [ ] **TASK-06**: Implement `update_task_logic(task_id, new_desc)` function.
- [ ] **TASK-07**: Implement `toggle_status_logic(task_id)` function.

## CLI & Interaction
- [ ] **TASK-08**: Implement `print_menu()` to display options.
- [ ] **TASK-09**: Implement `view_tasks_ui()` to format and print the task list.
- [ ] **TASK-10**: Implement `add_task_ui()` to handle user input for adding.
- [ ] **TASK-11**: Implement `update_task_ui()` to handle user input for updating.
- [ ] **TASK-12**: Implement `delete_task_ui()` to handle user input for deleting.
- [ ] **TASK-13**: Implement `toggle_status_ui()` to handle user input for toggling status.
- [ ] **TASK-14**: Implement Main Application Loop (`while True`) linking menu to UI functions.
- [ ] **TASK-15**: Implement Exit condition and graceful shutdown.

## Validation & Polish
- [ ] **TASK-16**: Add error handling for invalid integer inputs (ID selection).
- [ ] **TASK-17**: Add error handling for empty descriptions.
- [ ] **TASK-18**: Verify all acceptance criteria are met manually.
