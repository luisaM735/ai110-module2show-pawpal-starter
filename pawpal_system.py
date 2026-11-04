"""PawPal+ Core System - Logic Layer

This module contains the core classes for the PawPal+ pet care management system:
- Task: Represents a single pet care activity
- Pet: Stores pet details and associated tasks
- Owner: Manages multiple pets and provides access to all tasks
- Scheduler: The "brain" that organizes and manages tasks across pets
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import date, timedelta


@dataclass
class Task:
    """Represents a single pet care activity."""
    
    description: str
    scheduled_time: str
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "once"
    is_complete: bool = False
    pet_name: str = ""
    scheduled_date: date = field(default_factory=date.today)
    
    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.is_complete = True
    
    def get_next_occurrence(self) -> Optional["Task"]:
        """Create the next occurrence of this task based on frequency."""
        if self.frequency == "once":
            return None
        
        if self.frequency == "daily":
            next_date = self.scheduled_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.scheduled_date + timedelta(weeks=1)
        else:
            return None
        
        return Task(
            description=self.description,
            scheduled_time=self.scheduled_time,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            is_complete=False,
            pet_name=self.pet_name,
            scheduled_date=next_date,
        )


@dataclass
class Pet:
    """Stores pet details and a list of associated tasks."""
    
    name: str
    species: str
    breed: str = ""
    age: int = 0
    tasks: list[Task] = field(default_factory=list)
    
    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        task.pet_name = self.name
        self.tasks.append(task)
    
    def remove_task(self, description: str) -> bool:
        """Remove a task by description. Returns True if removed."""
        for i, task in enumerate(self.tasks):
            if task.description == description:
                self.tasks.pop(i)
                return True
        return False
    
    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        return self.tasks.copy()


class Owner:
    """Manages multiple pets and provides access to all their tasks."""
    
    def __init__(self, name: str):
        self.name = name
        self.pets: list[Pet] = []
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's list."""
        self.pets.append(pet)
    
    def remove_pet(self, name: str) -> bool:
        """Remove a pet by name. Returns True if removed."""
        for i, pet in enumerate(self.pets):
            if pet.name == name:
                self.pets.pop(i)
                return True
        return False
    
    def get_pet(self, name: str) -> Optional[Pet]:
        """Get a pet by name. Returns None if not found."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None
    
    def get_all_tasks(self) -> list[Task]:
        """Get all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """The 'brain' that retrieves, organizes, and manages tasks across pets."""
    
    def __init__(self, owner: Owner):
        self.owner = owner
    
    def get_todays_tasks(self) -> list[Task]:
        """Get all tasks scheduled for today."""
        today = date.today()
        return [task for task in self.owner.get_all_tasks() 
                if task.scheduled_date == today]
    
    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by their scheduled time (HH:MM format)."""
        return sorted(tasks, key=lambda t: t.scheduled_time)
    
    def filter_by_status(self, tasks: list[Task], complete: bool) -> list[Task]:
        """Filter tasks by completion status."""
        return [task for task in tasks if task.is_complete == complete]
    
    def filter_by_pet(self, tasks: list[Task], pet_name: str) -> list[Task]:
        """Filter tasks by pet name."""
        return [task for task in tasks if task.pet_name == pet_name]
    
    def detect_conflicts(self, tasks: list[Task]) -> list[str]:
        """Detect scheduling conflicts (tasks at the same time)."""
        conflicts = []
        time_map: dict[str, list[Task]] = {}
        
        for task in tasks:
            key = f"{task.scheduled_date}_{task.scheduled_time}"
            if key not in time_map:
                time_map[key] = []
            time_map[key].append(task)
        
        for key, task_list in time_map.items():
            if len(task_list) > 1:
                task_names = ", ".join(f"'{t.description}' ({t.pet_name})" 
                                       for t in task_list)
                date_str, time_str = key.split("_")
                conflicts.append(
                    f"Conflict at {time_str} on {date_str}: {task_names}"
                )
        
        return conflicts
    
    def handle_recurring_task(self, task: Task) -> Optional[Task]:
        """Handle a recurring task after completion by creating next occurrence."""
        next_task = task.get_next_occurrence()
        if next_task:
            pet = self.owner.get_pet(task.pet_name)
            if pet:
                pet.add_task(next_task)
        return next_task
    
    def mark_task_complete(self, pet_name: str, description: str) -> bool:
        """Mark a specific task as complete and handle recurrence."""
        pet = self.owner.get_pet(pet_name)
        if not pet:
            return False
        
        for task in pet.tasks:
            if task.description == description and not task.is_complete:
                task.mark_complete()
                self.handle_recurring_task(task)
                return True
        return False
