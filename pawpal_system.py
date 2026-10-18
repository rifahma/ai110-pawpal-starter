"""Core class skeletons for the PawPal+ pet care planner."""

from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    start_time: str | None = None
    frequency: str | None = None
    completed: bool = False

    def mark_complete(self) -> None:
        raise NotImplementedError

    def edit(self, **changes) -> None:
        raise NotImplementedError


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        raise NotImplementedError

    def remove_task(self, task: Task) -> None:
        raise NotImplementedError


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)
    preferences: dict[str, str] = field(default_factory=dict)

    def add_pet(self, pet: Pet) -> None:
        raise NotImplementedError

    def get_all_tasks(self) -> list[Task]:
        raise NotImplementedError


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def generate_plan(self) -> list[Task]:
        raise NotImplementedError

    def sort_tasks(self) -> list[Task]:
        raise NotImplementedError

    def detect_conflicts(self) -> list[Task]:
        raise NotImplementedError

    def explain_plan(self) -> str:
        raise NotImplementedError