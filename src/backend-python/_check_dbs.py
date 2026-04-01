import sqlite3

for label, path in [("backend-python/app.db", "app.db"), ("root/app.db", "../../app.db")]:
    print(f"=== {label} ===")
    try:
        conn = sqlite3.connect(path)
        tables = [t[0] for t in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        if "User" in tables:
            rows = conn.execute("SELECT id, email, display_name, length(password_hash) FROM User WHERE email='test@example.com'").fetchall()
            if rows:
                for r in rows:
                    print(f"  id={r[0]}, email={r[1]}, name={r[2]}, pw_len={r[3]}")
            else:
                print("  test@example.com NOT FOUND")
                total = conn.execute("SELECT COUNT(*) FROM User").fetchone()[0]
                all_emails = conn.execute("SELECT email FROM User").fetchall()
                print(f"  (total users: {total}, emails: {[e[0] for e in all_emails]})")
        else:
            print(f"  tables: {tables}")
        conn.close()
    except Exception as e:
        print(f"  Error: {e}")
