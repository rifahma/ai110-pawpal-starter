from pawpal_system import Pet, Task


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