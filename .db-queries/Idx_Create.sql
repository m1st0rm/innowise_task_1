BEGIN TRANSACTION;

CREATE INDEX IF NOT EXISTS idx_students_room ON Students (room);

COMMIT;


BEGIN TRANSACTION;

CREATE INDEX IF NOT EXISTS idx_students_birthday ON Students (birthday);

COMMIT;