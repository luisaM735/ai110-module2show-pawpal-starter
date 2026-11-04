"""PawPal+ Demo Script

This script demonstrates the core functionality of the PawPal+ system
by creating owners, pets, tasks, and generating a daily schedule.
"""

from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler


def print_schedule(tasks: list[Task], title: str = "Today's Schedule") -> None:
    """Print a formatted schedule of tasks."""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")
    
    if not tasks:
        print("  No tasks scheduled.")
        return
    
    for task in tasks:
        status = "✓" if task.is_complete else "○"
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.priority, "⚪")
        freq = f" [{task.frequency}]" if task.frequency != "once" else ""
        
        print(f"  {status} {task.scheduled_time} — {task.description} ({task.duration_minutes} min)")
        print(f"      {priority_emoji} {task.priority.upper()} | Pet: {task.pet_name}{freq}")
    
    print(f"{'='*50}\n")


def main():
    print("\n🐾 PawPal+ System Demo 🐾")
    print("=" * 50)
    
    # Create an owner
    owner = Owner("Jordan")
    print(f"\n👤 Created owner: {owner.name}")
    
    # Create pets
    mochi = Pet(name="Mochi", species="dog", breed="Golden Retriever", age=3)
    whiskers = Pet(name="Whiskers", species="cat", breed="Tabby", age=5)
    
    owner.add_pet(mochi)
    owner.add_pet(whiskers)
    print(f"🐕 Added pet: {mochi.name} ({mochi.breed}, {mochi.age} years old)")
    print(f"🐈 Added pet: {whiskers.name} ({whiskers.breed}, {whiskers.age} years old)")
    
    # Add tasks for Mochi (out of order to test sorting)
    today = date.today()
    
    mochi.add_task(Task(
        description="Evening walk",
        scheduled_time="18:00",
        duration_minutes=30,
        priority="high",
        frequency="daily",
        scheduled_date=today,
    ))
    
    mochi.add_task(Task(
        description="Morning walk",
        scheduled_time="08:00",
        duration_minutes=30,
        priority="high",
        frequency="daily",
        scheduled_date=today,
    ))
    
    mochi.add_task(Task(
        description="Feeding",
        scheduled_time="09:00",
        duration_minutes=10,
        priority="high",
        frequency="daily",
        scheduled_date=today,
    ))
    
    mochi.add_task(Task(
        description="Play time",
        scheduled_time="14:00",
        duration_minutes=20,
        priority="medium",
        frequency="daily",
        scheduled_date=today,
    ))
    
    # Add tasks for Whiskers
    whiskers.add_task(Task(
        description="Feeding",
        scheduled_time="09:00",
        duration_minutes=5,
        priority="high",
        frequency="daily",
        scheduled_date=today,
    ))
    
    whiskers.add_task(Task(
        description="Litter box cleaning",
        scheduled_time="10:00",
        duration_minutes=10,
        priority="medium",
        frequency="daily",
        scheduled_date=today,
    ))
    
    whiskers.add_task(Task(
        description="Grooming",
        scheduled_time="15:00",
        duration_minutes=15,
        priority="low",
        frequency="weekly",
        scheduled_date=today,
    ))
    
    print(f"\n📋 Added {len(mochi.tasks)} tasks for {mochi.name}")
    print(f"📋 Added {len(whiskers.tasks)} tasks for {whiskers.name}")
    
    # Create scheduler and get today's schedule
    scheduler = Scheduler(owner)
    
    # Get and sort today's tasks
    todays_tasks = scheduler.get_todays_tasks()
    sorted_tasks = scheduler.sort_by_time(todays_tasks)
    
    print_schedule(sorted_tasks, f"Today's Schedule for {owner.name}")
    
    # Check for conflicts
    conflicts = scheduler.detect_conflicts(todays_tasks)
    if conflicts:
        print("⚠️  SCHEDULING CONFLICTS DETECTED:")
        for conflict in conflicts:
            print(f"   {conflict}")
        print()
    
    # Filter by pet
    print("\n🐕 Tasks for Mochi only:")
    mochi_tasks = scheduler.filter_by_pet(sorted_tasks, "Mochi")
    for task in mochi_tasks:
        print(f"   {task.scheduled_time} — {task.description}")
    
    # Filter incomplete tasks
    print("\n📝 Pending tasks (not complete):")
    pending = scheduler.filter_by_status(sorted_tasks, complete=False)
    print(f"   {len(pending)} tasks remaining")
    
    # Mark a task complete and show recurring task handling
    print("\n✅ Marking 'Morning walk' as complete...")
    scheduler.mark_task_complete("Mochi", "Morning walk")
    
    # Show updated schedule
    todays_tasks = scheduler.get_todays_tasks()
    incomplete_today = scheduler.filter_by_status(todays_tasks, complete=False)
    sorted_incomplete = scheduler.sort_by_time(incomplete_today)
    
    print_schedule(sorted_incomplete, "Remaining Tasks for Today")
    
    # Show that a new task was created for tomorrow
    tomorrow = today + __import__('datetime').timedelta(days=1)
    all_tasks = owner.get_all_tasks()
    tomorrow_tasks = [t for t in all_tasks if t.scheduled_date == tomorrow]
    
    if tomorrow_tasks:
        print(f"📅 Recurring tasks auto-created for {tomorrow}:")
        for task in tomorrow_tasks:
            print(f"   {task.scheduled_time} — {task.description} ({task.pet_name})")


if __name__ == "__main__":
    main()
