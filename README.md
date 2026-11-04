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
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

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
