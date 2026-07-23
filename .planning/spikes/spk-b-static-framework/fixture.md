# SPK-B Static-First Comparison Fixture

This fixture is a non-production, text-only contract. It instructs no framework initialization and contains no application tree.

| Criterion | Required observation | Failure or blocker |
| --- | --- | --- |
| prerendering | Build an inspectable static page from the same fixture | Static output cannot be reproduced |
| Markdown / structured content | Render fixture Markdown plus a structured record without duplicating essential facts | Content needs a framework-only opaque source |
| interactive labs | Mount a bounded local interactive island/lab fixture with transcript/static equivalent noted | Lab requires undisclosed trusted authority or lacks static equivalent |
| multiple entries | Produce separately named public and guest/lab entry candidates | Entries are coupled into one authority bundle |
| test support | Run a deterministic local assertion against built fixture output | No replayable assertion is available |
| bundle / authority isolation | Identify public versus guest/lab output boundaries | Guest code gains host authority or bundle boundary is opaque |
| accessibility | Record keyboard, reduced-motion, transcript/state-inspection, reset/replay support path | Essential interaction has no accessible/static equivalent |
| static deployment | Identify generated static assets suitable for independent hosting | Deployment needs a live required service |

The fixture may be materialized only under the approved candidate's SPK-B `.experiment/` path. Results are observed implementation behavior; any recommendation is proposed ADR-0002 evidence, never accepted architecture.
