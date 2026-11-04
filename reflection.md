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

AI tools were used throughout this project in several key ways:

1. **Design Brainstorming**: Started by describing the pet care app scenario and asking for a Mermaid.js UML class diagram. This helped visualize relationships between Owner, Pet, Task, and Scheduler before writing code.

2. **Code Generation**: Used AI to generate class skeletons based on the UML design, then incrementally filled in method implementations. The prompt "Based on my skeletons, how should the Scheduler retrieve all tasks from the Owner's pets?" helped design the data flow.

3. **Test Generation**: Asked AI to draft pytest test cases covering "happy paths" and edge cases. The prompt "What are the most important edge cases to test for a pet scheduler with sorting and recurring tasks?" identified scenarios I hadn't considered.

4. **Documentation**: AI helped generate docstrings and format README sections consistently.

The most helpful prompts were specific and contextual, like attaching the current `pawpal_system.py` file and asking for targeted improvements rather than open-ended questions.

**b. Judgment and verification**

One moment where I modified an AI suggestion: The initial UML diagram suggested a complex `TaskManager` class separate from the `Scheduler`. I rejected this and kept a simpler design where `Scheduler` handles all task operations directly through the `Owner`. 

I evaluated this by considering:
1. The project scope (a single-user pet care app, not a multi-tenant system)
2. The principle of keeping designs as simple as possible while meeting requirements
3. The fact that adding another layer would complicate the code without providing clear benefits for this use case

I verified my decision by implementing the simpler design and confirming that all required features (sorting, filtering, conflicts, recurrence) could be achieved without the extra abstraction.

---

## 4. Testing and Verification

**a. What you tested**

The test suite covers 22 test cases organized by class:

1. **Task behaviors**: Marking tasks complete, generating next occurrences for daily/weekly recurrence, verifying one-time tasks don't recur
2. **Pet behaviors**: Adding/removing tasks, automatic pet_name assignment when tasks are added
3. **Owner behaviors**: Adding pets, retrieving pets by name, aggregating tasks across all pets
4. **Scheduler behaviors**: Sorting by time, filtering by status/pet, conflict detection, recurring task handling, getting today's tasks
5. **Edge cases**: Empty pets (no tasks), empty owners (no pets), non-existent pet lookups, marking tasks for missing pets

These tests are important because they verify:
- Core CRUD operations work correctly
- The "smart" scheduling features (sorting, filtering, conflicts) behave as expected
- Edge cases don't cause crashes or unexpected behavior
- Recurring task logic correctly creates future tasks

**b. Confidence**

**Confidence Level: 4/5 stars**

The test suite provides strong coverage of the core functionality and common edge cases. The 22 tests all pass consistently, and the CLI demo script (`main.py`) demonstrates the system working end-to-end.

Edge cases I would test next if given more time:
- **Performance**: How does the scheduler handle 1000+ tasks?
- **Duration overlap**: Tasks that start within another task's duration
- **Concurrent modifications**: Adding/removing tasks while iterating
- **Date edge cases**: Tasks scheduled at midnight, spanning multiple days
- **Input validation**: Invalid time formats, negative durations, empty descriptions

---

## 5. Reflection

**a. What went well**

I'm most satisfied with the **modular system design**. By separating concerns clearly (Task holds data, Pet owns tasks, Owner aggregates pets, Scheduler operates on the data), the code remained clean and testable. The UML-first approach paid off - the final implementation closely matches the original design, with only minor additions (like `scheduled_date`).

The **CLI-first workflow** was also effective. By verifying logic in `main.py` before connecting to Streamlit, I caught issues early and had a reliable demo script to show the system working without UI dependencies.

**b. What you would improve**

If I had another iteration, I would:

1. **Add duration-based conflict detection**: Currently only exact time matches are flagged. Overlapping durations (e.g., a 30-min task at 09:00 vs. a task at 09:15) aren't detected.

2. **Implement priority-based scheduling**: The scheduler sorts by time but could also consider priority for suggesting optimal task ordering.

3. **Add data persistence**: Currently all data lives in `st.session_state` and disappears on page refresh. Adding SQLite or JSON file storage would make the app practical.

4. **Improve input validation**: The system trusts all inputs. Adding validation for time formats, reasonable durations, and duplicate task detection would make it more robust.

**c. Key takeaway**

The most important thing I learned is that **AI works best as a collaborator, not a replacement for design thinking**. The AI could generate code quickly, but I needed to:
- Define clear requirements and constraints first
- Evaluate suggestions against the project's actual needs
- Verify generated code with tests and manual review
- Make judgment calls about complexity vs. simplicity

Being the "lead architect" means using AI to accelerate implementation while maintaining ownership of design decisions and quality standards.
