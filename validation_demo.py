import re

EMAIL = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_UA = re.compile(r"^\+380\d{9}$")
FILENAME = re.compile(r"^[A-Za-z0-9_-]+\.(txt|log|csv)$", re.IGNORECASE)


def check(pattern: re.Pattern, values: list[str]) -> None:
    for value in values:
        result = "OK" if pattern.fullmatch(value) else "INVALID"
        print(f"{value:<30} {result}")


def main() -> None:
    print("EMAIL")
    check(EMAIL, [
        "student@example.com",
        "name.surname@university.edu.ua",
        "wrong@",
        "a b@example.com",
    ])

    print("\nPHONE")
    check(PHONE_UA, [
        "+380501234567",
        "+380671112233",
        "0501234567",
        "+38050123",
    ])

    print("\nFILENAME")
    check(FILENAME, [
        "server.log",
        "report_2026.csv",
        "notes.txt",
        "photo.jpg",
    ])

    line = "user=anna ip=192.168.1.10 path=/api/profile"
    line = re.sub(r"user=[\w.-]+", "user=***", line)
    line = re.sub(
        r"(\d{1,3}\.\d{1,3}\.)\d{1,3}\.\d{1,3}",
        r"\1x.x",
        line,
    )
    print("\nANONYMIZED")
    print(line)


if __name__ == "__main__":
    main()