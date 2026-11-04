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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
