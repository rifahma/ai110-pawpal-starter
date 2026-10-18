# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features
- **Multi-pet management:** an owner can have several pets, and the Scheduler works across all of them through `Owner.get_all_tasks()`.
- **Priority-based planning:** tasks are ordered high, medium, low (shorter first on ties) and fitted into the owner's available minutes.
- **Sorting by time:** tasks are shown in clock order using minutes after midnight, with untimed tasks last.
- **Filtering:** view tasks by pet name, completion status, or both.
- **Conflict warnings:** overlapping tasks, within one pet or across pets, produce a readable warning. Back-to-back tasks are allowed, and invalid times return a warning instead of crashing.
- **Recurring tasks:** completing a daily or weekly task creates the next occurrence (+1 or +7 days with `timedelta`). Future-dated tasks stay out of today's plan.
- **Plan explanation:** `explain_plan()` summarizes what was chosen and how many minutes it uses.

## Implementation Summary
PawPal+ is a pet care planner. An owner can add pets, give each pet care tasks (walks, feeding, medication, grooming), and generate a daily schedule that fits the owner's available time.

The logic or skeleton lives in `pawpal_system.py` and uses four classes:

- **Task** 
one care activity with a title, duration, priority, optional start time, frequency, and completion status.
- **Pet**: stores a pet's name, species, plus its list of tasks.
- **Owner**: stores the owner's available minutes and list of pets.
  `get_all_tasks()` returns every pet's tasks together.
- **Scheduler**: reads all tasks through `Owner.get_all_tasks()`, sorts them by priority, skips completed or conflicting tasks, and fits the rest into the owner's available time. `explain_plan()` summarizes what was chosen.

**How they work together:** 
an Owner has many Pets, each Pet has many Tasks, and the Scheduler uses the Owner to reach all tasks across all pets.

`main.py` is a terminal demo that prints today's schedule, and
`tests/test_pawpal.py` contains tests for task completion and task addition.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output
Today's Schedule for Barnes
========================================
08:00 - Morning walk for Cookie (30 min) [priority: high]
08:30 - Breakfast for Luna (10 min) [priority: high]
12:00 - Medication for Luna (5 min) [priority: high]
16:00 - Grooming for Luna (20 min) [priority: medium]
18:00 - Evening play for Cookie (15 min) [priority: low]

Selected 5 task(s), using 80 of 120 available minutes:
- Medication (5 min, high priority)
- Breakfast (10 min, high priority)
- Morning walk (30 min, high priority)
- Grooming (20 min, medium priority)
- Evening play (15 min, low priority)


## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

```

Sample test output:

```
rootdir: /workspaces/ai110-pawpal-starter
plugins: anyio-4.15.1
collected 21 items                                                                                                       

tests/test_pawpal.py::test_completing_daily_task_creates_task_for_tomorrow PASSED                                  [  4%]
tests/test_pawpal.py::test_weekly_task_recurs_in_seven_days PASSED                                                 [  9%]
tests/test_pawpal.py::test_non_recurring_task_creates_no_new_task PASSED                                           [ 14%]
tests/test_pawpal.py::test_task_mark_complete_changes_status PASSED                                                [ 19%]
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED                                             [ 23%]
tests/test_pawpal.py::test_sort_tasks_orders_by_priority PASSED                                                    [ 28%]
tests/test_pawpal.py::test_sort_by_time_orders_start_times_and_places_unscheduled_last PASSED                      [ 33%]
tests/test_pawpal.py::test_filter_tasks_by_completion_status_and_pet_name PASSED                                   [ 38%]
tests/test_pawpal.py::test_plan_skips_completed_and_respects_time_limit PASSED                                     [ 42%]
tests/test_pawpal.py::test_overlapping_tasks_are_conflicts_and_excluded PASSED                                     [ 47%]
tests/test_pawpal.py::test_back_to_back_tasks_do_not_conflict PASSED                                               [ 52%]
tests/test_pawpal.py::test_conflict_warnings_report_overlapping_tasks PASSED                                       [ 57%]
tests/test_pawpal.py::test_conflict_warnings_do_not_crash_on_bad_time PASSED                                       [ 61%]
tests/test_pawpal.py::test_conflict_warnings_report_overlaps_between_pets PASSED                                   [ 66%]
tests/test_pawpal.py::test_conflict_warnings_handle_non_string_start_time PASSED                                   [ 71%]
tests/test_pawpal.py::test_sort_by_time_handles_non_zero_padded_times PASSED                                       [ 76%]
tests/test_pawpal.py::test_sort_by_time_rejects_invalid_time PASSED                                                [ 80%]
tests/test_pawpal.py::test_tasks_at_identical_time_are_flagged_as_conflicts PASSED                                 [ 85%]
tests/test_pawpal.py::test_future_recurring_task_is_not_in_todays_plan PASSED                                      [ 90%]
tests/test_pawpal.py::test_completing_a_task_twice_does_not_duplicate_it PASSED                                    [ 95%]
tests/test_pawpal.py::test_completing_unowned_task_raises_error PASSED                                             [100%]

=================================================== 21 passed in 0.11s ===================================================
```
**What the tests cover**

- **Task and Pet basics:** marking a task complete, and adding a task to a pet.
- **Sorting:** priority order, time order (including non-zero-padded times like `9:00`), and untimed tasks placed last.
- **Filtering:** by completion status, by pet name (case-insensitive), and by both.
- **Plan generation:** skips completed tasks and respects the owner's available minutes.
- **Conflict detection:** overlapping tasks, identical start times, back-to-back tasks (not a conflict), warnings within one pet and across pets, and invalid start times returning a warning instead of crashing.
- **Recurring tasks:** a daily task creates a copy due tomorrow, a weekly task one due in 7 days, non-recurring tasks create nothing, completing twice does not duplicate, tomorrow's copy stays out of today's plan, and completing a task that belongs to no pet raises an error.

**Confidence Level: ⭐⭐⭐⭐ (4/5)**

All 21 tests pass and they cover edge cases as well as happy paths, so I'm confident in the core scheduling logic. I held back one star because some cases are untested: unknown priority values, zero available minutes, a task fully inside another task's time slot, and the Streamlit UI itself.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting | `Scheduler.sort_tasks()`, `Scheduler.sort_by_time()` | `sort_tasks()` orders by priority, then shorter duration, and is used to build the plan. `sort_by_time()` orders by start time (HH:MM), with untimed tasks last. |
| Filtering | `Scheduler.filter_tasks()`, `Scheduler.generate_plan()` | `filter_tasks()` returns tasks by pet name and/or completion status. `generate_plan()` skips completed tasks, tasks not yet due, and tasks that don't fit in the available minutes. |
| Conflict detection | `Scheduler.detect_conflicts()`, `Scheduler.get_conflict_warnings()` | Overlapping start times and durations are flagged, across the same pet or different pets. Warnings name both tasks and pets, and invalid times return a warning instead of crashing. Back-to-back tasks are allowed. |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.mark_task_complete()` | Completing a daily or weekly task creates a new copy with `due_date` set using `timedelta` (+1 or +7 days) and adds it to the same pet. |

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_tasks()`, `Scheduler.sort_by_time()` | `sort_tasks()` orders by priority, then shorter duration, and is used to build the plan. `sort_by_time()` orders by start time (HH:MM), with untimed tasks last. |
| Filtering | `Scheduler.filter_tasks()`, `Scheduler.generate_plan()` | `filter_tasks()` returns tasks by pet name and/or completion status. `generate_plan()` skips completed tasks, tasks not yet due, and tasks that no longer fit in the available minutes. |
| Conflict handling | `Scheduler.detect_conflicts()`, `_tasks_overlap()` | Tasks with overlapping start times and durations are flagged and left out of the plan. Back-to-back tasks are allowed. Overlaps across different pets count, since one owner does all the tasks. |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.mark_task_complete()` | Completing a daily or weekly task creates a new copy with `due_date` set using `timedelta` (+1 or +7 days) and adds it to the same pet. Tasks not yet due are ignored by the plan and by conflict checks. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

**Example workflow:**

1. Enter the owner name and available minutes.
2. Add a pet, for example Cookie the dog.
3. Add tasks, such as a walk at 08:00 (30 min, high, daily) and feeding at 08:15 (10 min, high).
4. Check the task table, which is sorted by time. A yellow warning shows that the walk and feeding overlap.
5. Change the feeding to 08:30, and the warning turns into a green "No time conflicts found."
6. Click **Generate schedule** to see the plan and its explanation.
7. Mark the walk complete, and a new walk is created for tomorrow.

**Scheduler behaviors shown:** sorting by time, filtering by pet and status, conflict warnings, daily recurrence, and a plan that respects available time.

**Sample CLI output (`python main.py`):**

```
All tasks sorted by time:
  08:00 - Morning walk
  08:30 - Breakfast
  12:00 - Training session
  12:00 - Medication
  12:10 - Bath
  16:00 - Grooming
  18:00 - Evening play
  Flexible - Brush fur

Cookie's tasks:
  Evening play
  Morning walk
  Brush fur
  Training session
  Bath

Pending tasks:
  Evening play
  Morning walk
  Brush fur
  Training session
  Bath
  Grooming
  Medication

Completed tasks:
  Breakfast

Luna's pending tasks:
  Grooming

Conflict check:
  Medication

Conflict check:
  Warning: 'Training session' (Cookie, 12:00, 20 min) overlaps 'Bath' (Cookie, 12:10, 15 min) for pet Cookie.
  Warning: 'Training session' (Cookie, 12:00, 20 min) overlaps 'Medication' (Luna, 12:00, 5 min) between pets Cookie and Luna.
Completed: Morning walk. Next due: 2026-10-19
Cookie now has 7 tasks
```

**Screenshot or video** *(optional)*: /workspaces/ai110-pawpal-starter/docs