# SPK-F Two-Lesson Guest-only Fixture

**Fixture status:** proposed, local, non-production simulation.

**Authority boundary:** This fixture is a single guest-only document. It has no
host imports, no private child frames, no privileged browser assumption, no real
host capability, and no claim of runtime composition. A visual card representing
another actor is ordinary UI only; it is not a composed napplet.

## Architecture diagram

```text
+---------------------------------------------------------------+
| SPK-F guest-only local simulation                             |
|                                                               |
|  Lesson 1 <---- local navigation state ----> Lesson 2         |
|      |                                         |               |
|  diagram + transcript                      assessment          |
|      |                                         |               |
|  optional progress: guest-memory model (simulated)            |
|  optional source/lab open: copyable request (simulated)       |
+---------------------------------------------------------------+

No host import | No direct storage | No relay | No child frame
No external request | No real sibling-napplet composition claim
```

## Diagram transcript

1. The learner starts at Lesson 1 with local navigation state set to `boundary`.
2. The diagram labels the guest simulation as untrusted and self-contained.
3. The learner advances to Lesson 2; only the fixture's local state changes.
4. If the optional progress capability is simulated as present, the fixture
   displays `progress retained in guest memory for this session`.
5. If absent, it displays `progress is not retained; replay starts at Lesson 1`.
6. If an optional source/lab-open capability is simulated as present, the fixture
   renders a copyable request transcript; it does not open a link or lab.
7. If absent, it renders the same canonical citation as text and labels the
   unavailable capability. No private frame or actor is created in either state.

## Representative lesson 1 — Boundary map

**Learning objective:** Identify which behavior belongs to a guest simulation and
which would require a separately verified external host.

**Code example (local, illustrative only):**

```js
const guestState = { lesson: 'boundary', progress: 'not-persisted' };
function navigate(nextLesson) {
  guestState.lesson = nextLesson;
  return { kind: 'local-navigation', lesson: guestState.lesson };
}
```

**Inspectable state:** `lesson`, `progress`, and the simulated capability flag.
The function neither imports host code nor sends a message; it only changes local
fixture state.

## Representative lesson 2 — Capability degradation

**Learning objective:** Explain that optional progress and external source/lab
opening must degrade deterministically without claiming delegated authority.

**Capability-present simulation:**

```text
progress: retained in guest memory until fixture replay
external source/lab: copyable request transcript only; no opening occurs
```

**Capability-absent simulation:**

```text
progress: reset on replay; learner can inspect and repeat the lesson
external source/lab: copyable source citation only; no opening occurs
```

## Assessment

**Prompt:** A course guest renders a button that looks like a sibling lab. May it
claim that the sibling napplet was runtime-composed because the button is visible?

**Expected response:** No. Visibility is ordinary guest UI. A real sibling would
need external-host creation/focus through current verified composition behavior;
this SPK-F fixture has no such host or claim.

## Source metadata

| ID | Classification | Use in fixture | Status |
| --- | --- | --- | --- |
| `SRC-POLICY-001` | preserved project-policy/archive planning seed | scope and composition warning | not upstream proof |
| `SRC-POLICY-002` | project policy | evidence and safety handling | accepted project policy |
| `CMP-BASELINE-001` | compatibility baseline | explains blocked runtime/package facts | blocked |

**Uncertainty:** The fixture demonstrates only local, labeled behavior. It does
not prove a released package surface, a portable artifact contract, browser
conformance, host authority, or any upstream protocol behavior.

## Accessibility and replay expectations

- Keyboard: lesson navigation and assessment actions must be reachable in a
  deterministic tab order.
- Reduced motion: no required animated transition; the transcript remains the
  static equivalent.
- Inspection: rendered state and the transcript must expose every capability
  branch without requiring a visual-only interaction.
- Replay: reset returns to Lesson 1, clears guest-memory progress, and preserves
  the copyable source metadata.
