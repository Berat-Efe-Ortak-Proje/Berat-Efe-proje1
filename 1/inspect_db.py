import sqlite3
import os

# Path to the database
db_path = os.path.join('instance', 'club_management.db')

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def print_table(table_name, columns_to_show=None):
    print(f"\n--- {table_name.upper()} ---")
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        all_columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        if not rows:
            print("No data found.")
            return

        # Filter columns if specified
        if columns_to_show:
            indices = [all_columns.index(c) for c in columns_to_show if c in all_columns]
            display_columns = [all_columns[i] for i in indices]
        else:
            indices = range(len(all_columns))
            display_columns = all_columns

        # Calculate column widths
        widths = [len(c) for c in display_columns]
        formatted_rows = []
        for row in rows:
            formatted_row = []
            for i, idx in enumerate(indices):
                val = str(row[idx])
                # Truncate long text
                if len(val) > 30:
                    val = val[:27] + "..."
                formatted_row.append(val)
                widths[i] = max(widths[i], len(val))
            formatted_rows.append(formatted_row)
        
        # Print header
        header = " | ".join(f"{col:<{widths[i]}}" for i, col in enumerate(display_columns))
        print(header)
        print("-" * len(header))
        
        # Print rows
        for row in formatted_rows:
            print(" | ".join(f"{val:<{widths[i]}}" for i, val in enumerate(row)))
            
    except sqlite3.OperationalError as e:
        print(f"Error reading table {table_name}: {e}")

print("Reading database content...")

# Users: Show id, username, email, role
print_table('user', ['id', 'username', 'email', 'role'])

# Clubs: Show id, name, description
print_table('club', ['id', 'name', 'description'])

# Events: Show id, name, date, location
print_table('event', ['id', 'name', 'date', 'location'])

conn.close()
