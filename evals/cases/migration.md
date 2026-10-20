# Task

Use the installed project-workflow skill. Add migration.py exposing migrate(conn)
and rollback(conn) for the existing SQLite schema. Migration must preserve IDs and
names, add a status constrained to pending or done (initially pending), reject null
or blank names without partial changes, and advance user_version from 1 to 2.
Repeated migration of version 2 is a no-op. Reject other versions. Rollback before
application writes must restore version 1 and data; if any status is not pending,
refuse rollback without changing data. Include failure and recovery verification.
After verification and affected knowledge sync, stop in Closeout before marking
completion or moving the record; another session will finish disposition.
