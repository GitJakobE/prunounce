import sqlite3
conn = sqlite3.connect(r"c:\code\prunounce\src\backend-python\app.db")
c = conn.cursor()

print("=== CATEGORY COLUMNS ===")
c.execute('PRAGMA table_info("Category")')
for r in c.fetchall():
    print(r)

print("\n=== CATEGORY DATA ===")
c.execute('SELECT "nameEn", "nameEs", "nameDa" FROM "Category"')
for r in c.fetchall():
    en, es, da = r
    print(f'{en:30s} | es: {str(es):30s} | da: {da}')

conn.close()

con.close()
