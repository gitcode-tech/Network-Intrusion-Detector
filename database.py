import sqlite3

DATABASE = "alerts.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_ip TEXT NOT NULL,
            destination_port INTEGER,
            attempts INTEGER NOT NULL,
            alert_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def add_alert(source_ip, destination_port, attempts, alert_type):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO alerts
        (source_ip, destination_port, attempts, alert_type)
        VALUES (?, ?, ?, ?)
        """,
        (source_ip, destination_port, attempts, alert_type)
    )

    connection.commit()
    connection.close()


def get_alerts():
    connection = get_connection()

    alerts = connection.execute("""
        SELECT *
        FROM alerts
        ORDER BY created_at DESC
    """).fetchall()

    connection.close()

    return alerts
