from datetime import date, timedelta
from pawpal_system import Owner, Pet, Scheduler, Task

# Test cases for the PawPal+ system
def test_completing_daily_task_creates_task_for_tomorrow() -> None:
    owner = Owner("Test", 60)
    pet = Pet("Cookie", "dog", 4)
    owner.add_pet(pet)
    walk = Task("Walk", 30, "high", frequency="daily")
    pet.add_task(walk)

    new_task = Scheduler(owner).mark_task_complete(walk)

    assert walk.completed is True
    assert new_task.due_date == date.today() + timedelta(days=1)
    assert new_task.completed is False
    assert len(pet.tasks) == 2


def test_weekly_task_recurs_in_seven_days() -> None:
    task = Task("Grooming", 20, "medium", frequency="weekly")
    assert task.next_occurrence().due_date == date.today() + timedelta(days=7)


def test_non_recurring_task_creates_no_new_task() -> None:
    owner = Owner("Test", 60)
    pet = Pet("Cookie", "dog", 4)
    owner.add_pet(pet)
    task = Task("Vet visit", 60, "high")
    pet.add_task(task)

    assert Scheduler(owner).mark_task_complete(task) is None
    assert len(pet.tasks) == 1

# This is old test code that was already present in the file. It is kept for reference but may not be necessary to run if the new tests cover the same functionality.
def test_task_mark_complete_changes_status() -> None:
    task = Task(title="Morning walk", duration_minutes=30, priority="high")

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", species="dog", age=3)
    task = Task(title="Feeding", duration_minutes=10, priority="high")

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task

# More tests can be added here to cover additional functionality of the Task, Pet, Owner, and Scheduler classes.
def make_scheduler(minutes: int, *tasks: Task) -> Scheduler:
    owner = Owner(name="Test", available_minutes=minutes)
    pet = Pet(name="Cookie", species="dog", age=4)
    owner.add_pet(pet)
    for task in tasks:
        pet.add_task(task)
    return Scheduler(owner)


def test_sort_tasks_orders_by_priority() -> None:
    scheduler = make_scheduler(
        60,
        Task("Play", 10, "low"),
        Task("Meds", 5, "high"),
        Task("Groom", 10, "medium"),
    )
    assert [t.title for t in scheduler.sort_tasks()] == ["Meds", "Groom", "Play"]


def test_sort_by_time_orders_start_times_and_places_unscheduled_last() -> None:
    scheduler = make_scheduler(
        60,
        Task("Evening", 10, "low", start_time="18:00"),
        Task("Unscheduled", 5, "medium"),
        Task("Morning", 10, "high", start_time="08:00"),
    )

    assert [task.title for task in scheduler.sort_by_time()] == [
        "Morning",
        "Evening",
        "Unscheduled",
    ]

def test_filter_tasks_by_completion_status_and_pet_name() -> None:
    owner = Owner(name="Test", available_minutes=60)
    cookie = Pet(name="Cookie", species="dog", age=4)
    luna = Pet(name="Luna", species="cat", age=2)
    completed_walk = Task("Walk", 10, "high", completed=True)
    pending_walk = Task("Walk", 10, "medium")
    pending_feed = Task("Feed", 5, "high")
    cookie.add_task(completed_walk)
    cookie.add_task(pending_walk)
    luna.add_task(pending_feed)
    owner.add_pet(cookie)
    owner.add_pet(luna)
    scheduler = Scheduler(owner)

    assert scheduler.filter_tasks(completed=False) == [pending_walk, pending_feed]
    assert scheduler.filter_tasks(pet_name="cOoKiE") == [completed_walk, pending_walk]
    assert scheduler.filter_tasks(completed=False, pet_name="Cookie") == [pending_walk]
    assert scheduler.filter_tasks(pet_name="Unknown") == []


def test_plan_skips_completed_and_respects_time_limit() -> None:
    done = Task("Done", 5, "high")
    done.mark_complete()
    scheduler = make_scheduler(30, done, Task("Walk", 20, "high"), Task("Play", 20, "low"))
    assert [t.title for t in scheduler.generate_plan()] == ["Walk"]


def test_overlapping_tasks_are_conflicts_and_excluded() -> None:
    scheduler = make_scheduler(
        60,
        Task("Walk", 30, "high", start_time="08:00"),
        Task("Feed", 10, "high", start_time="08:15"),
    )
    assert len(scheduler.detect_conflicts()) == 2
    assert scheduler.generate_plan() == []


def test_back_to_back_tasks_do_not_conflict() -> None:
    scheduler = make_scheduler(
        60,
        Task("Walk", 30, "high", start_time="08:00"),
        Task("Feed", 10, "high", start_time="08:30"),
    )
    assert scheduler.detect_conflicts() == []

def test_back_to_back_tasks_do_not_conflict() -> None:
    scheduler = make_scheduler(
        60,
        Task("Walk", 30, "high", start_time="08:00"),
        Task("Feed", 10, "high", start_time="08:30"),
    )
    assert scheduler.detect_conflicts() == []


def test_conflict_warnings_report_overlapping_tasks() -> None:
    scheduler = make_scheduler(
        60,
        Task("Walk", 30, "high", start_time="08:00"),
        Task("Feed", 10, "high", start_time="08:15"),
    )
    warnings = scheduler.get_conflict_warnings()
    assert len(warnings) == 1
    assert "Walk" in warnings[0] and "Feed" in warnings[0]


def test_conflict_warnings_do_not_crash_on_bad_time() -> None:
    scheduler = make_scheduler(60, Task("Walk", 30, "high", start_time="8am"))
    warnings = scheduler.get_conflict_warnings()
    assert len(warnings) == 1
    assert "invalid" in warnings[0]