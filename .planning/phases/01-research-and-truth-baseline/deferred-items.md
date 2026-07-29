# Deferred Items

- Full `tests/phase1/test_evidence.py` cannot pass in this durable worktree because the pre-existing untracked `.planning/traceability/pack-v3-file-manifest.json` is absent here. The three existing source-validation tests fail with `ERROR TRC001`; this is unrelated to Plan 01-44. The four Plan 01-44 focused certification tests pass through `tools/phase1-python`.
