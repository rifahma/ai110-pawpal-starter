from pawpal_system import Owner, Pet, Scheduler, Task
from datetime import date, datetime
import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=120)
owner = st.session_state.owner

owner.name = st.text_input("Owner name", value=owner.name)
owner.available_minutes = int(
    st.number_input("Available minutes today", min_value=1, max_value=1440, value=owner.available_minutes)
)

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Age", min_value=0, max_value=40, value=1)

if st.button("Add pet"):
    owner.add_pet(Pet(name=pet_name, species=species, age=int(age)))  # Owner.add_pet()

st.markdown("### Tasks")

if owner.pets:
    pet_choice = st.selectbox("Task for which pet?", [p.name for p in owner.pets])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        start_time = st.text_input("Start time (HH:MM, optional)", value="")
    frequency = st.selectbox("Repeats", ["none", "daily", "weekly"])

    if st.button("Add task"):
        start = start_time.strip() or None
        valid = True
        if start is not None:
            try:
                datetime.strptime(start, "%H:%M")
            except ValueError:
                st.error("Start time must be 24-hour HH:MM, like 08:30.")
                valid = False
        if valid:
            pet = next(p for p in owner.pets if p.name == pet_choice)
            pet.add_task(
                Task(
                    task_title,
                    int(duration),
                    priority,
                    start_time=start,
                    frequency=None if frequency == "none" else frequency,
                )
            )
            st.success(f"Added {task_title} for {pet.name}")
else:
    st.info("Add a pet first, then you can add tasks.")

# Build the scheduler AFTER the add buttons run, so it sees new tasks
scheduler = Scheduler(owner)
pet_for_task = {id(t): p.name for p in owner.pets for t in p.tasks}

if owner.get_all_tasks():
    st.markdown("#### Current tasks")

    f1, f2 = st.columns(2)
    with f1:
        pet_filter = st.selectbox("Filter by pet", ["All"] + [p.name for p in owner.pets])
    with f2:
        status_filter = st.selectbox("Filter by status", ["All", "Pending", "Completed"])

    completed = {"All": None, "Pending": False, "Completed": True}[status_filter]
    filtered = scheduler.filter_tasks(
        completed=completed,
        pet_name=None if pet_filter == "All" else pet_filter,
    )
    keep = {id(t) for t in filtered}
    ordered = [t for t in scheduler.sort_by_time() if id(t) in keep]  # clock order

    st.table(
        [
            {
                "Time": t.start_time or "Flexible",
                "Pet": pet_for_task[id(t)],
                "Task": t.title,
                "Minutes": t.duration_minutes,
                "Priority": t.priority,
                "Repeats": t.frequency or "-",
                "Due": t.due_date or "today",
                "Done": t.completed,
            }
            for t in ordered
        ]
    )

    # Conflict warnings, shown right away
    warnings = scheduler.get_conflict_warnings()
    if warnings:
        st.warning(
            f"{len(warnings)} scheduling issue(s) found. Overlapping tasks are left "
            "out of the plan until you change one of their start times."
        )
        for message in warnings:
            st.warning(message)
    else:
        st.success("No time conflicts found.")

    # Mark complete (triggers recurring tasks)
    pending = scheduler.filter_tasks(completed=False)
    if pending:
        st.markdown("#### Mark a task complete")
        index = st.selectbox(
            "Task",
            range(len(pending)),
            format_func=lambda i: f"{pet_for_task[id(pending[i])]}: {pending[i].title} ({pending[i].start_time or 'flexible'})",
        )
        if st.button("Mark complete"):
            next_task = scheduler.mark_task_complete(pending[index])
            st.success(f"Completed {pending[index].title}.")
            if next_task is not None:
                st.info(f"Next occurrence added for {next_task.due_date}.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    try:
        plan = scheduler.generate_plan()
    except ValueError as error:
        st.error(str(error))
    else:
        plan_ids = {id(t) for t in plan}
        if plan:
            st.success(f"Today's schedule for {owner.name}")
            st.table(
                [
                    {
                        "Time": t.start_time or "Flexible",
                        "Pet": pet_for_task[id(t)],
                        "Task": t.title,
                        "Minutes": t.duration_minutes,
                        "Priority": t.priority,
                    }
                    for t in scheduler.sort_by_time()
                    if id(t) in plan_ids
                ]
            )
            st.text(scheduler.explain_plan())
        else:
            st.warning("No tasks could be scheduled.")

        left_out = [
            t
            for t in scheduler.filter_tasks(completed=False)
            if id(t) not in plan_ids and (t.due_date is None or t.due_date <= date.today())
        ]
        if left_out:
            st.info(
                "Left out (conflict or not enough time): "
                + ", ".join(f"{t.title} ({pet_for_task[id(t)]})" for t in left_out)
            )