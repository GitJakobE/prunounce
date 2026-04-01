import sqlite3
con = sqlite3.connect(r'c:\code\prunounce\src\backend-python\app.db')
for table in ['User', 'Category', 'Word', 'WordCategory', 'UserProgress']:
    count = con.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
    print(f'{table}: {count}')
con.close()
