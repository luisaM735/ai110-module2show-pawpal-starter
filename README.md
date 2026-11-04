# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Running `python main.py` produces the following output:

```
🐾 PawPal+ System Demo 🐾
==================================================

👤 Created owner: Jordan
🐕 Added pet: Mochi (Golden Retriever, 3 years old)
🐈 Added pet: Whiskers (Tabby, 5 years old)

📋 Added 4 tasks for Mochi
📋 Added 3 tasks for Whiskers

==================================================
  Today's Schedule for Jordan
==================================================
  ○ 08:00 — Morning walk (30 min)
      🔴 HIGH | Pet: Mochi [daily]
  ○ 09:00 — Feeding (10 min)
      🔴 HIGH | Pet: Mochi [daily]
  ○ 09:00 — Feeding (5 min)
      🔴 HIGH | Pet: Whiskers [daily]
  ○ 10:00 — Litter box cleaning (10 min)
      🟡 MEDIUM | Pet: Whiskers [daily]
  ○ 14:00 — Play time (20 min)
      🟡 MEDIUM | Pet: Mochi [daily]
  ○ 15:00 — Grooming (15 min)
      🟢 LOW | Pet: Whiskers [weekly]
  ○ 18:00 — Evening walk (30 min)
      🔴 HIGH | Pet: Mochi [daily]
==================================================

⚠️  SCHEDULING CONFLICTS DETECTED:
   Conflict at 09:00 on 2026-11-04: 'Feeding' (Mochi), 'Feeding' (Whiskers)

🐕 Tasks for Mochi only:
   08:00 — Morning walk
   09:00 — Feeding
   14:00 — Play time
   18:00 — Evening walk

📝 Pending tasks (not complete):
   7 tasks remaining

✅ Marking 'Morning walk' as complete...

==================================================
  Remaining Tasks for Today
==================================================
  ○ 09:00 — Feeding (10 min)
      🔴 HIGH | Pet: Mochi [daily]
  ○ 09:00 — Feeding (5 min)
      🔴 HIGH | Pet: Whiskers [daily]
  ○ 10:00 — Litter box cleaning (10 min)
      🟡 MEDIUM | Pet: Whiskers [daily]
  ○ 14:00 — Play time (20 min)
      🟡 MEDIUM | Pet: Mochi [daily]
  ○ 15:00 — Grooming (15 min)
      🟢 LOW | Pet: Whiskers [weekly]
  ○ 18:00 — Evening walk (30 min)
      🔴 HIGH | Pet: Mochi [daily]
==================================================

📅 Recurring tasks auto-created for 2026-11-05:
   08:00 — Morning walk (Mochi)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest tests/test_pawpal.py -v

# Run with coverage (requires pytest-cov):
python -m pytest --cov=pawpal_system tests/
```

### Test Coverage

The test suite covers 22 test cases across 5 categories:

- **Task tests**: mark_complete, daily/weekly recurrence, one-time tasks
- **Pet tests**: add/remove tasks, pet name assignment
- **Owner tests**: add pets, get pet by name, aggregate all tasks
- **Scheduler tests**: sort by time, filter by status/pet, conflict detection, recurring task handling
- **Edge cases**: empty pet/owner, non-existent pet lookup, marking tasks for missing pets

### Sample test output:

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0
collecting ... collected 22 items

tests/test_pawpal.py::TestTask::test_mark_complete_changes_status PASSED [  4%]
tests/test_pawpal.py::TestTask::test_get_next_occurrence_daily PASSED    [  9%]
tests/test_pawpal.py::TestTask::test_get_next_occurrence_weekly PASSED   [ 13%]
tests/test_pawpal.py::TestTask::test_get_next_occurrence_once_returns_none PASSED [ 18%]
tests/test_pawpal.py::TestPet::test_add_task_increases_count PASSED      [ 22%]
tests/test_pawpal.py::TestPet::test_add_task_sets_pet_name PASSED        [ 27%]
tests/test_pawpal.py::TestPet::test_remove_task PASSED                   [ 31%]
tests/test_pawpal.py::TestPet::test_remove_nonexistent_task_returns_false PASSED [ 36%]
tests/test_pawpal.py::TestOwner::test_add_pet PASSED                     [ 40%]
tests/test_pawpal.py::TestOwner::test_get_pet_by_name PASSED             [ 45%]
tests/test_pawpal.py::TestOwner::test_get_all_tasks_aggregates_from_all_pets PASSED [ 50%]
tests/test_pawpal.py::TestScheduler::test_sort_by_time PASSED            [ 54%]
tests/test_pawpal.py::TestScheduler::test_filter_by_status_incomplete PASSED [ 59%]
tests/test_pawpal.py::TestScheduler::test_detect_conflicts_same_time PASSED [ 63%]
tests/test_pawpal.py::TestScheduler::test_mark_task_complete_handles_recurrence PASSED [ 68%]
tests/test_pawpal.py::TestScheduler::test_get_todays_tasks_filters_by_date PASSED [ 72%]
tests/test_pawpal.py::TestScheduler::test_filter_by_pet PASSED           [ 77%]
tests/test_pawpal.py::TestScheduler::test_no_conflicts_different_times PASSED [ 81%]
tests/test_pawpal.py::TestScheduler::test_pet_with_no_tasks PASSED       [ 86%]
tests/test_pawpal.py::TestScheduler::test_owner_with_no_pets PASSED      [ 90%]
tests/test_pawpal.py::TestScheduler::test_get_pet_not_found PASSED       [ 95%]
tests/test_pawpal.py::TestScheduler::test_mark_task_complete_nonexistent_pet PASSED [100%]

============================== 22 passed in 0.03s ==============================
```

### Confidence Level: ⭐⭐⭐⭐ (4/5)

The test suite provides strong coverage of core functionality and edge cases. Additional tests that would improve confidence:
- Concurrent task modifications
- Very large numbers of tasks (performance testing)
- Overlapping time duration conflicts (currently only exact time matches)

## 📐 Smarter Scheduling

The PawPal+ scheduler implements intelligent task management through the following features:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks chronologically by scheduled_time (HH:MM format) using Python's sorted() with a lambda key |
| Filter by status | `Scheduler.filter_by_status()` | Returns only completed or pending tasks based on is_complete flag |
| Filter by pet | `Scheduler.filter_by_pet()` | Returns tasks for a specific pet, useful for multi-pet households |
| Conflict detection | `Scheduler.detect_conflicts()` | Detects tasks scheduled at the exact same time using a hash map (O(n) complexity) |
| Recurring tasks | `Task.get_next_occurrence()`, `Scheduler.handle_recurring_task()` | Automatically creates the next occurrence when a daily/weekly task is marked complete using timedelta calculations |
| Today's tasks | `Scheduler.get_todays_tasks()` | Filters all tasks to show only those scheduled for the current date |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
