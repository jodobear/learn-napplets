# SPK-I — Accessible deterministic diagram/motion comparison

This is a disposable, non-production local experiment. It creates no application route,
framework scaffold, visual-system dependency, guest runtime, or learner-code execution
surface. All labels in `fixture.svg` are synthetic or point only to project-policy IDs.
They do not assert private protocol behavior.

## Candidate matrix

| Candidate | Representation | State/motion model | Essential-equivalence status | Cost decision |
| --- | --- | --- | --- | --- |
| A | `fixture.svg`: semantic, data-driven SVG | Native SVG anchor navigation between named static steps; no auto-looping motion and no script | Measured against title/description, visible focus, keyboard links, transcript, table, reduced motion, reset/replay, screenshots, and hostile input | Measure fixture bytes and browser load/screenshot values |
| B | Minimal local state/motion controller | Would require executable state code | Not introduced: the SPK-I fixture must not create a dynamic learner-code or script-injection surface | Unselected; no cost is claimed or inferred |
| C | External visual dependency | Library-owned rendering/motion | Not introduced: no approved measured need and no visual dependency installation | Blocked; no dependency is installed or substituted |

Candidate A can only be a proposed ADR-0006 input when every essential representation
check passes in an available direct-installed browser. Candidate B is not a fallback:
adding it after a failure would hide the failure by changing the trust boundary.
Candidate C remains blocked rather than being approximated by an unreviewed package.

## Fixture contract

`fixture.svg` contains three named synthetic states: `step-compose`, `step-host`, and
`step-result`. Each state appears in all of these co-located representations:

1. the visible SVG flow;
2. the keyboard-reachable step-link labels;
3. the text transcript region; and
4. an ARIA table with state, owner, and outcome cells.

The fixture includes a `<title>` and `<desc>`, focus styling for the native SVG links,
and an explicit no-auto-motion policy. Its reduced-motion equivalent is the identical
static named-step view: motion never carries authority or protocol meaning. Replaying
always starts at `step-compose`; reset is the fixture's immutable initial URI/content,
not a script action.

The hostile-input label is literal escaped text:

```text
<script>window.__learnerInjection = true</script>
```

It must stay text. The runner injects a **trusted-host test sentinel** before navigation
and verifies that the fixture cannot create a script element, cannot expose executable
inline event handlers, cannot set `window.__learnerInjection`, and cannot alter the
sentinel. That harness-only sentinel does not give learner content any authority.

## Procedure

1. Validate the pre-execution envelope.

   ```text
   tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-i-diagram-motion --contract
   ```

2. Clear only the isolated output directory and run five samples in each approved
   direct-installed browser.

   ```text
   rm -rf /tmp/spk-i-diagram-motion
   tools/phase1-python .planning/spikes/spk-i-diagram-motion/runner.py \
     --fixture .planning/spikes/spk-i-diagram-motion/fixture.svg \
     --out /tmp/spk-i-diagram-motion
   ```

   The runner calls Playwright 1.61.0 only through `tools/phase1-python` and launches
   `/opt/google/chrome/google-chrome` and `/usr/bin/firefox` by their recorded paths.
   It never runs `playwright install`, downloads a managed browser, changes Firefox
   profiles/preferences, or adds browser flags.

3. Inspect `/tmp/spk-i-diagram-motion/manifest.json` and `browser-results.json`.
   For a browser that launches, require all five samples to pass and share one
   screenshot digest. A launch failure is an explicit blocked outcome, not a pass.

4. Verify Candidate A against its declared criteria: semantic title/description,
   keyboard-reachable focusable links, visible focus style, transcript/table parity,
   static reduced-motion equivalence, immutable reset/replay, screenshot determinism,
   fixture-byte cost, hostile-input containment, and trusted-host-sentinel integrity.

5. Copy only summarized environment, measurement, and report evidence into the spike.
   Generated screenshots and raw browser output stay in `/tmp`.

6. Validate the completed spike, its report, and the common research root. The common
   validation report must remain under `/tmp`; do not discard or stage the pre-existing
   dirty `.planning/research/reports/validation.md`.

   ```text
   tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-i-diagram-motion --complete
   tools/phase1-python tools/validate-research.py validate-report .planning/spikes/spk-i-diagram-motion/report.md
   tools/phase1-python tools/validate-research.py validate --root .planning/research --report /tmp/spk-i-research-validation.md
   ```

## Outcome handling

- **Passed:** Candidate A passes every essential local check in all available browsers;
  retain it only as a proposed, non-production ADR-0006 evidence fixture.
- **Failed:** an available browser runs but fails an essential check. Preserve the
  digest/result, report a failed comparison, and do not introduce B or C to mask it.
- **Blocked:** the approved toolchain or a direct-installed browser cannot complete a
  declared check. Record the exact scope and impacts. Preserve the existing Firefox
  launch blocker if it recurs; do not introduce a configuration workaround.

No result accepts ADR-0006 or authorizes a production component, framework, visual
library, dynamic execution surface, or motion-first teaching path.
