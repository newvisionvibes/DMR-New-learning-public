from db import fetch_all

rows = fetch_all(
    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
)
print(rows)
