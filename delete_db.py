import os

db_path = os.path.join('instance', 'event_management.db')
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Deleted {db_path}")
else:
    print(f"{db_path} does not exist")
