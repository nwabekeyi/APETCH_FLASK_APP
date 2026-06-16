# migrate.py
from database import get_db_connection

def migrate_add_columns():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Example 1: Add created_at column
        cur.execute("""
            ALTER TABLE classes 
            ADD COLUMN IF NOT EXISTS created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        """)

        # Example 2: Add status column
        cur.execute("""
            ALTER TABLE classes 
            ADD COLUMN IF NOT EXISTS status ENUM('active', 'inactive', 'archived') 
            DEFAULT 'active'
        """)

        # Example 3: Add teacher_id (if you have teachers table)
        # cur.execute("""
        #     ALTER TABLE classes 
        #     ADD COLUMN IF NOT EXISTS teacher_id INT NULL
        # """)

        print("✅ Migration completed successfully!")

    except Exception as e:
        print(f"❌ Migration Error: {e}")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    print("Running database migration...")
    migrate_add_columns()