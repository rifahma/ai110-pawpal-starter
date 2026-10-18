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

# Run with coverage:
pytest --cov
```

Sample test output:

```
================================================== test session starts ===================================================
platform linux -- Python 3.14.2, pytest-9.1.1, pluggy-1.7.0
rootdir: /workspaces/ai110-pawpal-starter
plugins: anyio-4.15.1
collected 11 items                                                                                                       

tests/test_pawpal.py ...........                                                                                   [100%]

=================================================== 11 passed in 0.03s ===================================================
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_tasks()`, `Scheduler.sort_by_time()` | `sort_tasks()` orders by priority, then shorter duration, and is used to build the plan. `sort_by_time()` orders by start time (HH:MM), with untimed tasks last. |
| Filtering | `Scheduler.filter_tasks()`, `Scheduler.generate_plan()` | `filter_tasks()` returns tasks by pet name and/or completion status. `generate_plan()` skips completed tasks, tasks not yet due, and tasks that no longer fit in the available minutes. |
| Conflict handling | `Scheduler.detect_conflicts()`, `_tasks_overlap()` | Tasks with overlapping start times and durations are flagged and left out of the plan. Back-to-back tasks are allowed. Overlaps across different pets count, since one owner does all the tasks. |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.mark_task_complete()` | Completing a daily or weekly task creates a new copy with `due_date` set using `timedelta` (+1 or +7 days) and adds it to the same pet. Tasks not yet due are ignored by the plan and by conflict checks. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->