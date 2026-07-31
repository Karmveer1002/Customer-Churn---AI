import sqlite3

DATABASE = "database.db"


def create_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    # ===========================================
    # USERS
    # ===========================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # ===========================================
    # PREDICTION HISTORY
    # ===========================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS prediction_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        CreditScore INTEGER,

        Geography TEXT,

        Gender TEXT,

        Age INTEGER,

        Tenure INTEGER,

        Balance REAL,

        NumOfProducts INTEGER,

        HasCrCard INTEGER,

        IsActiveMember INTEGER,

        EstimatedSalary REAL,

        Prediction INTEGER,

        Probability REAL,

        Risk TEXT,

        CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # ===========================================
    # DATASET INFO
    # ===========================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS uploaded_dataset(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT,

        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    conn.commit()

    conn.close()

    print("=" * 60)
    print("DATABASE CREATED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":

    create_database()