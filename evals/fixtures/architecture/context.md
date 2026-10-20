# Report processing context

The application is a single service backed by SQLite. Users currently run reports
synchronously. The team can operate one application service and one database.
Some reports might outgrow synchronous requests, but arrival rate, report duration,
latency goals and retention requirements have not been measured or agreed.

The request is an architecture proposal only. Do not add application code,
install dependencies, run experiments or accept a delivery baseline.
