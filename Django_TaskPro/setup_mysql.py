"""
Setup script to initialize the MySQL database for TaskPro.
Usage:
    python setup_mysql.py
"""
import os
import sys
import getpass
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

def setup_mysql():
    print("=" * 60)
    print("TaskPro - MySQL Database Setup")
    print("=" * 60)

    host = os.environ.get("DB_HOST", "127.0.0.1")
    port = int(os.environ.get("DB_PORT", "3306"))
    user = os.environ.get("DB_USER", "root")
    dbname = os.environ.get("DB_NAME", "taskpro_db")
    password = os.environ.get("DB_PASSWORD", "")

    if not password:
        prompt_pwd = getpass.getpass(f"Enter MySQL password for user '{user}': ")
        password = prompt_pwd

    try:
        import pymysql
    except ImportError:
        print("Error: pymysql is not installed. Run: pip install pymysql")
        sys.exit(1)

    print(f"\nAttempting to connect to MySQL at {host}:{port} as '{user}'...")
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            connect_timeout=5
        )
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            print(f"✓ Database '{dbname}' created or already exists!")
        conn.close()

        # Update .env
        env_path = BASE_DIR / ".env"
        lines = []
        if env_path.exists():
            with open(env_path, "r") as f:
                lines = f.readlines()

        updated_password = False
        new_lines = []
        for line in lines:
            if line.startswith("DB_PASSWORD="):
                new_lines.append(f"DB_PASSWORD={password}\n")
                updated_password = True
            elif line.startswith("DB_FALLBACK_SQLITE="):
                new_lines.append("DB_FALLBACK_SQLITE=False\n")
            else:
                new_lines.append(line)
        if not updated_password:
            new_lines.append(f"DB_PASSWORD={password}\n")

        with open(env_path, "w") as f:
            f.writelines(new_lines)

        print("✓ Updated .env with MySQL credentials!")
        print("\nNow running Django migrations...")
        os.system(f'"{sys.executable}" manage.py makemigrations')
        os.system(f'"{sys.executable}" manage.py migrate')
        print("\n✓ Setup completed successfully! You can run: python manage.py runserver")

    except Exception as e:
        print(f"\n✗ Failed to connect to MySQL: {e}")
        print("Please verify MySQL is running and your credentials are correct.")

if __name__ == "__main__":
    setup_mysql()
