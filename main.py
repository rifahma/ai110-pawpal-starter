"""Demo script: builds an owner, pets, and tasks, then prints today's schedule."""

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Barnes", available_minutes=120)

    cookie = Pet(name="Cookie", species="Dog", age=4)
    luna = Pet(name="Luna", species="Cat", age=2)
    owner.add_pet(cookie)
    owner.add_pet(luna)

    # Tasks added deliberately OUT of time order
    cookie.add_task(Task("Evening play", 15, "low", start_time="18:00"))
    luna.add_task(Task("Grooming", 20, "medium", start_time="16:00"))
    cookie.add_task(Task("Morning walk", 30, "high", start_time="08:00", frequency="daily"))
    luna.add_task(Task("Medication", 5, "high", start_time="12:00", frequency="weekly"))
    luna.add_task(Task("Breakfast", 10, "high", start_time="08:30", frequency="daily"))
    cookie.add_task(Task("Brush fur", 10, "low"))  # no start time

    # Mark one task complete so the status filters have something to show
    luna.tasks[2].mark_complete()  # Breakfast

    scheduler = Scheduler(owner)

    print("All tasks sorted by time:")
    for task in scheduler.sort_by_time():
        print(f"  {task.start_time or 'Flexible'} - {task.title}")

    print("\nCookie's tasks:")
    for task in scheduler.filter_tasks(pet_name="Cookie"):
        print(f"  {task.title}")

    print("\nPending tasks:")
    for task in scheduler.filter_tasks(completed=False):
        print(f"  {task.title}")

    print("\nCompleted tasks:")
    for task in scheduler.filter_tasks(completed=True):
        print(f"  {task.title}")

    print("\nLuna's pending tasks:")
    for task in scheduler.filter_tasks(completed=False, pet_name="Luna"):
        print(f"  {task.title}")

    # Demonstrate the mark_task_complete method
    walk = Task("Morning walk", 30, "high", start_time="08:00", frequency="daily")
    cookie.add_task(walk)

    scheduler = Scheduler(owner)
    new_task = scheduler.mark_task_complete(walk)
    print(f"Completed: {walk.title}. Next due: {new_task.due_date}")
    print("Cookie now has", len(cookie.tasks), "tasks")


if __name__ == "__main__":
    main()