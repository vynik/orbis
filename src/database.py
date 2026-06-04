import sqlite3

# Creating the database

def create_warn_database(orbis_database):
    conn = sqlite3.connect(database=orbis_database)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS active_warns (
            id           INTEGER PRIMARY KEY AUTOINCREMENT, 
            member       TEXT NOT NULL,
            member_id    INTEGER NOT NULL,
            warned_by    TEXT NOT NULL,
            reason       TEXT NOT NULL,
            duration     TEXT NOT NULL,
            evidence     TEXT NOT NULL,
            appealable   BOOL NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS archived_warns (
            id           INTEGER PRIMARY KEY AUTOINCREMENT, 
            member       TEXT NOT NULL,
            member_id    INTEGER NOT NULL,
            warned_by    TEXT NOT NULL,
            reason       TEXT NOT NULL,
            duration     TEXT NOT NULL,
            evidence     TEXT NOT NULL,
            appealable   BOOL NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# Adding a warn to the database

def log_warn(orbis_database, member, member_id, warned_by, reason, duration, evidence, appealable):
    conn = sqlite3.connect(database=orbis_database)

    try:
        conn.execute(
            "INSERT INTO active_warns (member, member_id, warned_by, reason, duration, evidence, appealable) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (member, member_id, warned_by, reason, duration, evidence, appealable),
        )
        conn.execute(
            "INSERT INTO archived_warns (member, member_id, warned_by, reason, duration, evidence, appealable) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (member, member_id, warned_by, reason, duration, evidence, appealable),
        )
        conn.commit()

    except sqlite3.IntegrityError:
        print(f"Error {sqlite3.IntegrityError}")

    conn.close()

# Removing a warn from the database

def delete_warn(orbis_database, warn_id):
    conn = sqlite3.connect(database=orbis_database)

    try:
        conn.execute(
            f"DELETE FROM active_warns WHERE id = ?",
            (warn_id,),
        )
        conn.commit()

    except sqlite3.IntegrityError:
        print(f"Error: {sqlite3.IntegrityError}")

    conn.close()

# Reading the database

def read_database(orbis_database, get_user_id):
    conn = sqlite3.connect(database=orbis_database)
    rows = conn.execute(
        f"SELECT id, member, member_id, warned_by, reason, duration, evidence, appealable FROM active_warns WHERE member_id = ?",
        (get_user_id,),
    ).fetchall()
    conn.close()
    return rows

def read_deleted_warn(orbis_database, warn_id):
    conn = sqlite3.connect(database=orbis_database)
    rows = conn.execute(
        f"SELECT id, member, member_id, warned_by, reason, duration, evidence, appealable FROM active_warns WHERE id = ?",
        (warn_id,),
    ).fetchall()
    conn.close()
    return rows

def read_archive_database(orbis_database):
    conn = sqlite3.connect(database=orbis_database)
    rows = conn.execute(
        "SELECT id, member, member_id, warned_by, reason, duration, evidence, appealable FROM archived_warns ORDER BY id"
    ).fetchall()
    conn.close()
    return rows