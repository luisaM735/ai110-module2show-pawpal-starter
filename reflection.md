# PawPal+ Project Reflection

## 1. System Design

### Core User Actions

The PawPal+ system enables pet owners to perform three core actions:

1. **Add a Pet**: Register a new pet with details like name, species, breed, and age. This creates a profile that can hold multiple care tasks.

2. **Schedule a Task**: Create care activities (walks, feeding, medications, grooming, enrichment) with attributes including scheduled time, duration, priority level, and recurrence frequency (one-time, daily, weekly).

3. **View Today's Schedule**: Display an organized daily plan showing all tasks sorted by time, with visual indicators for priority levels and warnings for scheduling conflicts.

**a. Initial design**

The initial UML design includes four core classes with clear separation of concerns:

1. **Task** (Python dataclass): Represents a single pet care activity. Holds attributes for description, scheduled_time (HH:MM format), duration_minutes, priority (low/medium/high), frequency (once/daily/weekly), completion status, pet_name, and scheduled_date. Methods include `mark_complete()` and `get_next_occurrence()` for recurring task support.

2. **Pet** (Python dataclass): Stores pet details (name, species, breed, age) and maintains a list of Task objects. Methods include `add_task()`, `remove_task()`, and `get_tasks()` to manage the pet's activities.

3. **Owner**: Manages multiple Pet objects. Contains the owner's name and a list of pets. Methods include `add_pet()`, `remove_pet()`, `get_pet()`, and `get_all_tasks()` to aggregate tasks across all pets.

4. **Scheduler**: The "brain" of the system that operates on an Owner's data. It retrieves, sorts, filters, and manages tasks. Methods include `get_todays_tasks()`, `sort_by_time()`, `filter_by_status()`, `filter_by_pet()`, `detect_conflicts()`, `handle_recurring_task()`, and `mark_task_complete()`.

The relationships are: Owner owns multiple Pets (1-to-many), Pet has multiple Tasks (1-to-many), and Scheduler manages one Owner (1-to-1).

**b. Design changes**

During skeleton creation, I added the `scheduled_date` attribute to Task. This was necessary because the original design only had `scheduled_time` (HH:MM), but to properly support recurring tasks and daily scheduling, we need to know which date the task is for. This enables filtering "today's tasks" and calculating the next occurrence for daily/weekly recurring tasks.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers the following constraints:

1. **Time**: Tasks are sorted chronologically by their `scheduled_time` (HH:MM format) using Python's `sorted()` with a lambda key. This ensures the daily schedule presents tasks in the order they should be performed.

2. **Date**: Tasks are filtered by `scheduled_date` to show only today's tasks, preventing future/past tasks from cluttering the current view.

3. **Completion Status**: Tasks can be filtered to show pending or completed items, helping owners focus on what still needs to be done.

4. **Pet Association**: Tasks can be filtered by pet name, allowing owners with multiple pets to view schedules separately.

Time was prioritized as the primary sorting constraint because pet care is inherently time-sensitive (feeding times, medication schedules, walk routines).

**b. Tradeoffs**

The conflict detection algorithm only checks for **exact time matches**, not overlapping durations. For example, two tasks at "09:00" are flagged as conflicts, but a 30-minute task at "09:00" and another task at "09:15" are not detected as overlapping.

This tradeoff is reasonable because:
1. It keeps the algorithm simple and fast (O(n) with a hash map)
2. Pet owners typically schedule tasks at distinct times anyway
3. The visual schedule already shows durations, so owners can spot near-conflicts manually
4. Adding duration-based overlap detection would significantly increase complexity for minimal real-world benefit in a pet care context

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
