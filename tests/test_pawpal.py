"""Tests for the PawPal+ system."""

from datetime import date, timedelta
import pytest
from pawpal_system import Task, Pet, Owner, Scheduler


class TestTask:
    """Tests for the Task class."""
    
    def test_mark_complete_changes_status(self):
        """Verify that calling mark_complete() changes the task's status."""
        task = Task(
            description="Morning walk",
            scheduled_time="08:00",
            duration_minutes=30,
        )
        assert task.is_complete is False
        
        task.mark_complete()
        
        assert task.is_complete is True
    
    def test_get_next_occurrence_daily(self):
        """Verify daily tasks create next occurrence for tomorrow."""
        today = date.today()
        task = Task(
            description="Feeding",
            scheduled_time="09:00",
            duration_minutes=10,
            frequency="daily",
            scheduled_date=today,
        )
        
        next_task = task.get_next_occurrence()
        
        assert next_task is not None
        assert next_task.scheduled_date == today + timedelta(days=1)
        assert next_task.is_complete is False
        assert next_task.description == task.description
    
    def test_get_next_occurrence_weekly(self):
        """Verify weekly tasks create next occurrence for next week."""
        today = date.today()
        task = Task(
            description="Grooming",
            scheduled_time="15:00",
            duration_minutes=30,
            frequency="weekly",
            scheduled_date=today,
        )
        
        next_task = task.get_next_occurrence()
        
        assert next_task is not None
        assert next_task.scheduled_date == today + timedelta(weeks=1)
    
    def test_get_next_occurrence_once_returns_none(self):
        """Verify one-time tasks return None for next occurrence."""
        task = Task(
            description="Vet appointment",
            scheduled_time="10:00",
            duration_minutes=60,
            frequency="once",
        )
        
        assert task.get_next_occurrence() is None


class TestPet:
    """Tests for the Pet class."""
    
    def test_add_task_increases_count(self):
        """Verify that adding a task increases the pet's task count."""
        pet = Pet(name="Mochi", species="dog")
        assert len(pet.tasks) == 0
        
        task = Task(
            description="Morning walk",
            scheduled_time="08:00",
            duration_minutes=30,
        )
        pet.add_task(task)
        
        assert len(pet.tasks) == 1
    
    def test_add_task_sets_pet_name(self):
        """Verify that adding a task sets the pet_name attribute."""
        pet = Pet(name="Whiskers", species="cat")
        task = Task(
            description="Feeding",
            scheduled_time="09:00",
            duration_minutes=5,
        )
        
        pet.add_task(task)
        
        assert task.pet_name == "Whiskers"
    
    def test_remove_task(self):
        """Verify tasks can be removed by description."""
        pet = Pet(name="Mochi", species="dog")
        task = Task(
            description="Morning walk",
            scheduled_time="08:00",
            duration_minutes=30,
        )
        pet.add_task(task)
        
        result = pet.remove_task("Morning walk")
        
        assert result is True
        assert len(pet.tasks) == 0
    
    def test_remove_nonexistent_task_returns_false(self):
        """Verify removing nonexistent task returns False."""
        pet = Pet(name="Mochi", species="dog")
        
        result = pet.remove_task("Nonexistent task")
        
        assert result is False


class TestOwner:
    """Tests for the Owner class."""
    
    def test_add_pet(self):
        """Verify pets can be added to owner."""
        owner = Owner("Jordan")
        pet = Pet(name="Mochi", species="dog")
        
        owner.add_pet(pet)
        
        assert len(owner.pets) == 1
        assert owner.pets[0].name == "Mochi"
    
    def test_get_pet_by_name(self):
        """Verify pets can be retrieved by name."""
        owner = Owner("Jordan")
        pet = Pet(name="Mochi", species="dog")
        owner.add_pet(pet)
        
        result = owner.get_pet("Mochi")
        
        assert result is not None
        assert result.name == "Mochi"
    
    def test_get_all_tasks_aggregates_from_all_pets(self):
        """Verify get_all_tasks returns tasks from all pets."""
        owner = Owner("Jordan")
        
        mochi = Pet(name="Mochi", species="dog")
        mochi.add_task(Task("Walk", "08:00", 30))
        
        whiskers = Pet(name="Whiskers", species="cat")
        whiskers.add_task(Task("Feed", "09:00", 5))
        
        owner.add_pet(mochi)
        owner.add_pet(whiskers)
        
        all_tasks = owner.get_all_tasks()
        
        assert len(all_tasks) == 2


class TestScheduler:
    """Tests for the Scheduler class."""
    
    def test_sort_by_time(self):
        """Verify tasks are returned in chronological order."""
        owner = Owner("Jordan")
        pet = Pet(name="Mochi", species="dog")
        
        pet.add_task(Task("Evening walk", "18:00", 30))
        pet.add_task(Task("Morning walk", "08:00", 30))
        pet.add_task(Task("Lunch", "12:00", 10))
        
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        
        sorted_tasks = scheduler.sort_by_time(pet.get_tasks())
        
        assert sorted_tasks[0].scheduled_time == "08:00"
        assert sorted_tasks[1].scheduled_time == "12:00"
        assert sorted_tasks[2].scheduled_time == "18:00"
    
    def test_filter_by_status_incomplete(self):
        """Verify filtering returns only incomplete tasks."""
        owner = Owner("Jordan")
        pet = Pet(name="Mochi", species="dog")
        
        task1 = Task("Walk", "08:00", 30)
        task2 = Task("Feed", "09:00", 10)
        task2.mark_complete()
        
        pet.add_task(task1)
        pet.add_task(task2)
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        incomplete = scheduler.filter_by_status(pet.get_tasks(), complete=False)
        
        assert len(incomplete) == 1
        assert incomplete[0].description == "Walk"
    
    def test_detect_conflicts_same_time(self):
        """Verify scheduler detects tasks scheduled at the same time."""
        owner = Owner("Jordan")
        today = date.today()
        
        mochi = Pet(name="Mochi", species="dog")
        mochi.add_task(Task("Feeding", "09:00", 10, scheduled_date=today))
        
        whiskers = Pet(name="Whiskers", species="cat")
        whiskers.add_task(Task("Feeding", "09:00", 5, scheduled_date=today))
        
        owner.add_pet(mochi)
        owner.add_pet(whiskers)
        
        scheduler = Scheduler(owner)
        conflicts = scheduler.detect_conflicts(owner.get_all_tasks())
        
        assert len(conflicts) == 1
        assert "09:00" in conflicts[0]
    
    def test_mark_task_complete_handles_recurrence(self):
        """Verify marking a daily task complete creates next occurrence."""
        owner = Owner("Jordan")
        today = date.today()
        
        pet = Pet(name="Mochi", species="dog")
        pet.add_task(Task(
            "Morning walk", "08:00", 30,
            frequency="daily",
            scheduled_date=today,
        ))
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        scheduler.mark_task_complete("Mochi", "Morning walk")
        
        tomorrow_tasks = [t for t in pet.get_tasks() 
                         if t.scheduled_date == today + timedelta(days=1)]
        
        assert len(tomorrow_tasks) == 1
        assert tomorrow_tasks[0].description == "Morning walk"
        assert tomorrow_tasks[0].is_complete is False
