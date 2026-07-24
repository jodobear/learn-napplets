# SPK-J — Least-authority code-editing comparison

SPK-J is a disposable, **non-production** local experiment. It supplies a
synthetic editing task, not a product editor or a runtime for learner code. It
creates no route, framework scaffold, guest napplet, package manifest, package
install, code evaluation, network request, credential, telemetry event, or
persistent learner record.

## Research question

Which least-authority editing approach lets a learner distinguish one declared
safe text variant from another while retaining keyboard operation, a
screen-reader-readable result, static fallback, deterministic reset/replay, and
no execution of arbitrary learner content?

The comparison follows the required ordering: fixed tested variants, controlled
small edits, lightweight editor, then a full editor only when evidence justifies
it. `ADR-0009` may receive proposed evidence only; SPK-J cannot accept an ADR
or choose a production editor.

## Declared learning task

Given the synthetic starter text `const greeting = "Hello";`, identify the
predeclared safe change that selects `"Hi"`. The intended fact is limited to:
**this fixture recognizes two exact strings**. It does not parse, run, lint,
format, compile, validate, sandbox, transmit, or claim anything about arbitrary
JavaScript, a napplet, or a host API.

## Candidate matrix

| Candidate | Learner interaction | Execution authority | Accessibility/static/replay contract | Cost and eligibility |
| --- | --- | --- | --- | --- |
| A — fixed tested variants | Choose the starter or alternate button; the fixture renders the matching fixed text | None; text is a fixture constant | Native buttons, visible focus, status announcement, readable `<pre>`, and reset to the starter button | Baseline; measure fixture bytes and local load only |
| B — controlled textarea | Type or paste into a labelled native textarea; the fixture accepts only either exact declared string | Exact string comparison only; arbitrary text becomes `unrecognized` and is rendered with `textContent` | Native textarea keyboard behavior, focus, `aria-live` status, reset button, and no-JS-readable starter/alternate text | Baseline; measure fixture bytes and local load only |
| C — lightweight native shell | Use a second labelled textarea with line/character inspection and a read-only safe-variant guide | No package and no evaluator; inspection is character count and exact-match classification | Native label, visible focus, text status, safe guide, deterministic reset, and static guide | Measure only as a local native-control shell; it is not an external editor claim |
| D — CodeJar 4.3.0 | Proposed lightweight package candidate | Not run | Could only be measured after complete version/API/license/source evidence and human review | **Blocked pending Task 2**: registry `4.3.0` gitHead has a `4.2.0` immutable source package.json |
| E — CodeMirror 6 direct set | Proposed package editor: state, view, commands, and JavaScript language support | Not run | Could only be measured after public API, keyboard/static/replay, bundle, and isolation tests | **Blocked pending Task 2**: direct package records are complete, but the resolved dependency closure and dated human decision are absent |

No candidate accepts arbitrary code execution. Candidate E is not a fallback for a
failure of A–C. A failed or blocked lower-authority result remains evidence; it
must not be hidden by adding a heavier editor.

## Exact editor package dossier and human gate

All registry data below was retrieved read-only at `2026-07-24T09:23:23Z`.
The commands are **future operation shapes only**. Do not run them until Task 2
records a dated per-package human decision. Any dependency not in the reviewed
resolved lock remains blocked; no alternative package or version may be
substituted.

| Package / version | Root public export/API locator | Official provenance and immutable source revision | License / integrity | Bundle and maintenance evidence | Isolated install command | Eligibility / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| `codejar@4.3.0` | Registry `exports`: `.` → `./dist/codejar.js`; `./cursor` → `./dist/cursor.js` | Registry: `https://registry.npmjs.org/codejar/4.3.0`; repo: `https://github.com/antonmedv/codejar`; registry gitHead `4d19174c5a2759a5bf90be26353f7c85715392fa` (`https://github.com/antonmedv/codejar/commit/4d19174c5a2759a5bf90be26353f7c85715392fa`) | Registry declares MIT and `sha512-A7BlrtD2oHR4xsABs/lLvDNxiPxkx71SuyHhcilBHbPMASpQs4d1AG2XjDSAm7y40RmfXbSGbMBhllGy//CDOA==`; shasum `16901574fa2114def629ff20bd0408acb1891a12` | Published `2025-10-14T09:05:30.639Z`; 26,112 unpacked bytes, 7 files, no registry dependencies | `npm --prefix .planning/spikes/spk-j-code-editing/.experiment/codejar-4.3.0 install --ignore-scripts --package-lock=false codejar@4.3.0` | **Blocked**: source `package.json` at gitHead reports `4.2.0`, so that revision cannot prove the 4.3.0 API/license source. No install. |
| `@codemirror/state@6.5.2` | `exports.import` `./dist/index.js`, `exports.require` `./dist/index.cjs`; immutable `src/index.ts` exports `EditorState`, `StateField`, `Compartment`, `Transaction`, `StateEffect` | Registry: `https://registry.npmjs.org/@codemirror%2Fstate/6.5.2`; repo `https://github.com/codemirror/state`; gitHead `64cba4b48555891636bc9afba74952c4224f53b1`, source `https://github.com/codemirror/state/blob/64cba4b48555891636bc9afba74952c4224f53b1/src/index.ts` | MIT in immutable `package.json`; integrity `sha512-FVqsPqtPWKVVL3dPSxy8wEF/ymIEuVzF1PK3VbUgrxXpJUSHQWWZz4JMToquRxnkw+36LTamCZG2iua2Ptq0fA==`; shasum `8eca3a64212a83367dc85475b7d78d5c9b7076c6` | Published `2025-02-03T12:12:54.353Z`; 431,834 unpacked bytes, 9 files | `npm --prefix .planning/spikes/spk-j-code-editing/.experiment/codemirror-6-core install --ignore-scripts --package-lock=false @codemirror/state@6.5.2 @codemirror/view@6.38.6 @codemirror/commands@6.8.1 @codemirror/lang-javascript@6.2.3` | **Blocked pending Task 2**: direct record complete, but dependency closure must be locked, inspected, and approved. |
| `@codemirror/view@6.38.6` | `exports.import` `./dist/index.js`, `exports.require` `./dist/index.cjs`; immutable `src/index.ts` exports `EditorView`, `keymap`, `KeyBinding`, `lineNumbers`, `placeholder` | Registry: `https://registry.npmjs.org/@codemirror%2Fview/6.38.6`; repo `https://github.com/codemirror/view`; gitHead `05e9b6633b03f857178b1dd7f97739cea7cffd2e`, source `https://github.com/codemirror/view/blob/05e9b6633b03f857178b1dd7f97739cea7cffd2e/src/index.ts` | MIT in immutable `package.json`; integrity `sha512-qiS0z1bKs5WOvHIAC0Cybmv4AJSkAXgX5aD6Mqd2epSLlVJsQl8NG23jCVouIgkh4All/mrbdsf2UOLFnJw0tw==`; shasum `25d9df071393801196c311025d2caa7a5523c26c` | Published `2025-10-13T07:32:25.479Z`; 1,195,929 unpacked bytes, 9 files | Same CodeMirror command above | **Blocked pending Task 2**: direct record complete, but dependency closure must be locked, inspected, and approved. |
| `@codemirror/commands@6.8.1` | `exports.import` `./dist/index.js`, `exports.require` `./dist/index.cjs`; immutable `src/commands.ts` exports `history`, `historyKeymap`, `undo`, `redo`, and `defaultKeymap` | Registry: `https://registry.npmjs.org/@codemirror%2Fcommands/6.8.1`; repo `https://github.com/codemirror/commands`; gitHead `1fe425f7424887b96feadf8d9b0dc7f3afb80b44`, source `https://github.com/codemirror/commands/blob/1fe425f7424887b96feadf8d9b0dc7f3afb80b44/src/commands.ts` | MIT in immutable `package.json`; integrity `sha512-KlGVYufHMQzxbdQONiLyGQDUW0itrLZwq3CcY7xpv9ZLRHqzkBSoteocBHtMCoY7/Ci4xhzSrToIeLg7FxHuaw==`; shasum `639f5559d2f33f2582a2429c58cb0c1b925c7a30` | Published `2025-03-31T06:09:04.731Z`; 235,720 unpacked bytes, 9 files | Same CodeMirror command above | **Blocked pending Task 2**: direct record complete, but dependency closure must be locked, inspected, and approved. |
| `@codemirror/lang-javascript@6.2.3` | `exports.import` `./dist/index.js`, `exports.require` `./dist/index.cjs`; immutable `src/index.ts` exports `javascript`, `javascriptLanguage`, `typescriptLanguage`, `jsxLanguage` | Registry: `https://registry.npmjs.org/@codemirror%2Flang-javascript/6.2.3`; repo `https://github.com/codemirror/lang-javascript`; gitHead `9f86da0fcf08360c449a327b131866d9b4ca8d95`, source `https://github.com/codemirror/lang-javascript/blob/9f86da0fcf08360c449a327b131866d9b4ca8d95/src/index.ts` | MIT in immutable `package.json`; integrity `sha512-8PR3vIWg7pSu7ur8A07pGiYHgy3hHj+mRYRCSG8q+mPIrl0F02rgpGv+DsQTHRTc30rydOsf5PZ7yjKFg2Ackw==`; shasum `d705c359dc816afcd3bcdf120a559f83d31d4cda` | Published `2025-02-12T10:12:43.061Z`; 61,953 unpacked bytes, 9 files | Same CodeMirror command above | **Blocked pending Task 2**: direct record complete, but dependency closure must be locked, inspected, and approved. |

The CodeMirror source commits were checked as release-marking commits:
`64cba4b...` “Mark version 6.5.2”, `05e9b66...` “Mark version 6.38.6”,
`1fe425f...` “Mark version 6.8.1”, and `9f86da0...` “Mark version 6.2.3”.
This is provenance evidence, not an approval to install or a claim of complete
resolved-package eligibility.

## Fixture safety contract

`fixture.html` uses only local constants and native controls. Its script may:

1. compare textarea values to the two declared exact strings;
2. update visible text and ARIA status via `textContent`;
3. reset native controls to deterministic fixture constants; and
4. expose a test-only inspection summary.

It must never use `eval`, `Function`, dynamic `<script>` creation, `innerHTML`,
inline event attributes derived from learner input, module loading, worker
creation, `srcdoc`, `postMessage`, `fetch`, storage, or a network target.
Learner text is never interpreted as markup or code. The fixture places a
trusted-context sentinel on `window`; hostile text such as
`<script>window.__spkJTrustedHostSentinel = "changed"</script>` must remain
literal text and leave the sentinel unchanged.

The fixture is intentionally **not** a sandbox that executes learner code. If a
later lesson needs execution, it requires a separately reviewed isolated
bundling-worker or sandbox design; SPK-J cannot grant that authority.

## Predeclared accessibility, performance, and replay checks

| Check | Fixed / controlled / lightweight requirement | Package-editor requirement |
| --- | --- | --- |
| Keyboard | Buttons, textareas, and reset controls are reachable in tab order and usable without a pointer | Record actual keyboard behavior only after approval |
| Screen reader | Every textarea has a visible `<label>` and short description; an `aria-live` status reports accepted or unrecognized exact text | Record actual role/name/value and announcement behavior only after approval |
| Focus | Visible `:focus-visible` outline is present | Record actual visible focus only after approval |
| Static equivalent | The starter/alternate text and safety explanation remain readable before JavaScript runs | Supply an equivalent readable fallback before any package measurement |
| Reduced motion | No animation is present | Any package motion must be disabled or have an equivalent static state |
| Reset/replay | Reset restores the starter text, accepted state, length, and sentinel check deterministically | Five clean local replays must preserve initial state and report all values |
| Isolation | Hostile input remains text; no arbitrary learner code can execute in the trusted top-level context | Prove no dynamic execution or script injection reaches trusted context |
| Bundle/startup | Record fixture bytes and local load values; no package is loaded | Record package/lock bundle and startup measurements only after approval |

## Outcome handling

- **Passed candidate:** only a measured local candidate that meets every declared
  essential check in all available browser samples. A pass is observed browser
  behavior, not protocol authority or an ADR acceptance.
- **Failed candidate:** retain actual output and failure details; do not add a
  heavier editor as compensation.
- **Blocked candidate:** missing provenance/API/license/integrity/source/lock/
  human decision, or a browser launch block. Preserve the exact blocker and use
  fixed variants or controlled textarea only.

Before Task 2, the sole permitted command is:

```text
tools/phase1-python tools/validate-research.py validate-spike .planning/spikes/spk-j-code-editing --contract
```

It validates the record only. It does not install, import, bundle, or execute an
editor package.
