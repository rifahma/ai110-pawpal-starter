"""Core classes for the PawPal+ pet care planner."""

from dataclasses import dataclass, field, replace
from datetime import date, datetime, timedelta


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    start_time: str | None = None
    frequency: str | None = None
    completed: bool = False
    due_date: date | None = None

    def next_occurrence(self) -> "Task | None":
        """Return a new task for the next daily/weekly occurrence, or None."""
        days = {"daily": 1, "weekly": 7}.get((self.frequency or "").lower())
        if days is None:
            return None
        base = self.due_date or date.today()
        return replace(self, completed=False, due_date=base + timedelta(days=days))

    def mark_complete(self) -> None:
        """Mark the task as complete."""
        self.completed = True

    def edit(self, **changes: object) -> None:
        """Update allowed task fields with validation."""
        editable_fields = {
            "title",
            "duration_minutes",
            "priority",
            "start_time",
            "frequency",
            "completed",
        }
        unknown_fields = changes.keys() - editable_fields
        if unknown_fields:
            names = ", ".join(sorted(unknown_fields))
            raise ValueError(f"Cannot edit unknown task field(s): {names}")

        updated_values = {
            "title": self.title,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "start_time": self.start_time,
            "frequency": self.frequency,
            "completed": self.completed,
        }
        updated_values.update(changes)

        title = updated_values["title"]
        duration_minutes = updated_values["duration_minutes"]
        priority = updated_values["priority"]
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Task title must be a non-empty string")
        if not isinstance(duration_minutes, int) or duration_minutes <= 0:
            raise ValueError("Task duration must be a positive number of minutes")
        if not isinstance(priority, str) or not priority.strip():
            raise ValueError("Task priority must be a non-empty string")

        for field_name, value in changes.items():
            setattr(self, field_name, value)


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the pet's schedule."""
        if not isinstance(task, Task):
            raise TypeError("task must be a Task instance")
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the pet's schedule."""
        self.tasks.remove(task)


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)
    preferences: dict[str, str] = field(default_factory=dict)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's care list."""
        if not isinstance(pet, Pet):
            raise TypeError("pet must be a Pet instance")
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return every task assigned to the owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Collects and organizes care tasks belonging to every owner pet."""

    _PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def __init__(self, owner: Owner) -> None:
        """Store the owner whose tasks are being scheduled."""
        if not isinstance(owner, Owner):
            raise TypeError("owner must be an Owner instance")
        self.owner = owner

    def generate_plan(self) -> list[Task]:
        """Return incomplete, non-conflicting tasks that fit the owner's time."""
        plan: list[Task] = []
        scheduled: list[Task] = []
        remaining_minutes = self.owner.available_minutes
        conflicts = {id(task) for task in self.detect_conflicts()}

        for task in self.sort_tasks():
            if (
                task.completed
                or not self._is_due(task)
                or id(task) in conflicts
                or task.duration_minutes > remaining_minutes
            ):
                continue
            if any(self._tasks_overlap(task, planned) for planned in scheduled):
                continue
            plan.append(task)
            scheduled.append(task)
            remaining_minutes -= task.duration_minutes

        return plan

    def sort_tasks(self) -> list[Task]:
        """Sort all pets' tasks by priority, then by shorter duration."""
        tasks = self.owner.get_all_tasks()
        return sorted(
            tasks,
            key=lambda task: (
                self._PRIORITY_ORDER.get(task.priority.lower(), len(self._PRIORITY_ORDER)),
                task.duration_minutes,
            ),
        )

    def sort_by_time(self) -> list[Task]:
        """Sort all pets' tasks by start time, placing unscheduled tasks last."""
        return sorted(
            self.owner.get_all_tasks(),
            key=lambda task: (task.start_time is None, task.start_time or ""),
        )

    def filter_tasks(
        self,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Filter tasks by completion status, pet name, or both."""
        return [
            task
            for pet in self.owner.pets
            if pet_name is None or pet.name.casefold() == pet_name.casefold()
            for task in pet.tasks
            if completed is None or task.completed is completed
        ]

    def detect_conflicts(self) -> list[Task]:
        """Return incomplete tasks whose fixed start times overlap."""
        tasks = [
            task
            for task in self.owner.get_all_tasks()
            if not task.completed and task.start_time is not None and self._is_due(task)
        ]
        conflicts: set[int] = set()

        for index, task in enumerate(tasks):
            for other in tasks[index + 1 :]:
                if self._tasks_overlap(task, other):
                    conflicts.update((id(task), id(other)))

        return [task for task in tasks if id(task) in conflicts]

    def get_conflict_warnings(self) -> list[str]:
        """Return a warning message for each pair of overlapping tasks."""
        warnings: list[str] = []
        entries: list[tuple[Pet, Task]] = []

        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.completed or task.start_time is None or not self._is_due(task):
                    continue
                try:
                    self._minutes_after_midnight(task.start_time)
                except (TypeError, ValueError):
                    warnings.append(
                        f"Warning: '{task.title}' for {pet.name} has an invalid "
                        f"start time ({task.start_time!r}) and was not checked."
                    )
                    continue
                entries.append((pet, task))

        for index, (pet_a, task_a) in enumerate(entries):
            for pet_b, task_b in entries[index + 1 :]:
                if self._tasks_overlap(task_a, task_b):
                    if pet_a is pet_b:
                        who = f"for pet {pet_a.name}"
                    else:
                        who = f"between pets {pet_a.name} and {pet_b.name}"
                    warnings.append(
                        f"Warning: '{task_a.title}' ({pet_a.name}, {task_a.start_time}, "
                        f"{task_a.duration_minutes} min) overlaps '{task_b.title}' "
                        f"({pet_b.name}, {task_b.start_time}, {task_b.duration_minutes} min) "
                        f"{who}."
                    )
        return warnings

    def explain_plan(self) -> str:
        """Summarize the selected tasks and time usage."""
        plan = self.generate_plan()
        if not plan:
            return "No incomplete tasks fit the available time."

        total_minutes = sum(task.duration_minutes for task in plan)
        lines = [
            f"Selected {len(plan)} task(s), using {total_minutes} of "
            f"{self.owner.available_minutes} available minutes:"
        ]
        lines.extend(
            f"- {task.title} ({task.duration_minutes} min, {task.priority} priority)"
            for task in plan
        )
        return "\n".join(lines)
    
    def mark_task_complete(self, task: Task) -> Task | None:
        """Complete a task and add the next occurrence if it recurs."""
        for pet in self.owner.pets:
            if any(t is task for t in pet.tasks):
                if task.completed:
                    return None  # avoid creating duplicates
                task.mark_complete()
                next_task = task.next_occurrence()
                if next_task is not None:
                    pet.add_task(next_task)
                return next_task
        raise ValueError("Task does not belong to any of the owner's pets")

    @staticmethod
    def _is_due(task: Task) -> bool:
        """Return True if the task has no due date or is due today or earlier."""
        return task.due_date is None or task.due_date <= date.today()

    @staticmethod
    def _tasks_overlap(first: Task, second: Task) -> bool:
        """Check whether two tasks overlap in scheduled time."""
        if first.start_time is None or second.start_time is None:
            return False

        first_start = Scheduler._minutes_after_midnight(first.start_time)
        second_start = Scheduler._minutes_after_midnight(second.start_time)
        first_end = first_start + first.duration_minutes
        second_end = second_start + second.duration_minutes

        return first_start < second_end and second_start < first_end

    @staticmethod
    def _minutes_after_midnight(start_time: str) -> int:
        """Convert a HH:MM time to minutes after midnight."""
        try:
            parsed_time = datetime.strptime(start_time, "%H:%M")
        except ValueError as error:
            raise ValueError(
                f"Invalid start_time {start_time!r}; expected 24-hour HH:MM format"
            ) from error
        return parsed_time.hour * 60 + parsed_time.minute