import getpass
import hashlib
import json
import os
from pathlib import Path
import secrets


TEACHER_CREDENTIALS_PATH = Path(__file__).with_name("teachers.json")
PASSWORD_HASH_ITERATIONS = 310000


def main():
    username = input("Teacher username: ").strip()
    if not username:
        raise SystemExit("Username cannot be empty.")

    password = getpass.getpass("Teacher password: ")
    confirmation = getpass.getpass("Confirm password: ")
    if not password:
        raise SystemExit("Password cannot be empty.")
    if password != confirmation:
        raise SystemExit("Passwords do not match.")

    if TEACHER_CREDENTIALS_PATH.exists():
        try:
            credentials = json.loads(TEACHER_CREDENTIALS_PATH.read_text(encoding="utf-8"))
            teachers = credentials["teachers"]
        except (OSError, KeyError, TypeError, json.JSONDecodeError):
            raise SystemExit("Teacher credentials file is invalid.")
    else:
        teachers = []

    if any(teacher.get("username") == username for teacher in teachers):
        raise SystemExit("That username already exists.")

    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), PASSWORD_HASH_ITERATIONS
    ).hex()
    teachers.append({
        "username": username,
        "password_hash": f"pbkdf2_sha256${PASSWORD_HASH_ITERATIONS}${salt}${digest}",
    })

    TEACHER_CREDENTIALS_PATH.write_text(
        json.dumps({"teachers": teachers}, indent=2) + "\n", encoding="utf-8"
    )
    os.chmod(TEACHER_CREDENTIALS_PATH, 0o600)
    print(f"Teacher account {username!r} added.")


if __name__ == "__main__":
    main()