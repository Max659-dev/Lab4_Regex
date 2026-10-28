from collections import Counter
from pathlib import Path
import re

LOG_PATTERN = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2}) "
    r"(?P<time>\d{2}:\d{2}:\d{2}) "
    r"(?P<level>INFO|WARN|ERROR) "
    r"user=(?P<user>[\w.-]+|-) "
    r"ip=(?P<ip>(?:\d{1,3}\.){3}\d{1,3}) "
    r"method=(?P<method>GET|POST|PUT|DELETE) "
    r"path=(?P<path>\S+) "
    r"status=(?P<status>\d{3}) "
    r"duration=(?P<duration>\d+)ms$"
)

# Регулярний вираз для пошуку path з числовим ID (Самостійна модифікація 13.1 #3)
PATH_ID_PATTERN = re.compile(r"^/api/[A-Za-z_-]+/\d+$")


def parse_line(line: str) -> dict | None:
    match = LOG_PATTERN.fullmatch(line.strip())
    if not match:
        return None
    item = match.groupdict()
    item["status"] = int(item["status"])
    item["duration"] = int(item["duration"])
    return item


def main() -> None:
    log_path = Path("data/app.log")
    lines = log_path.read_text(encoding="utf-8").splitlines()

    records = []
    invalid_lines = []

    for number, line in enumerate(lines, start=1):
        record = parse_line(line)
        if record is None:
            invalid_lines.append((number, line))
        else:
            records.append(record)

    levels = Counter(item["level"] for item in records)
    methods = Counter(item["method"] for item in records)
    users = Counter(item["user"] for item in records if item["user"] != "-")
    
    # Модифікація: Підрахунок HTTP status-кодів через Counter (Крок 13.1 #1)
    statuses = Counter(item["status"] for item in records)

    errors = [item for item in records if item["level"] == "ERROR"]
    slow = [item for item in records if item["duration"] >= 300]
    
    # Модифікація: Список записів зі status >= 400 (Крок 13.1 #2)
    http_errors = [item for item in records if item["status"] >= 400]

    # Модифікація: Унікальні path з числовим ID (Крок 13.1 #3)
    id_paths = sorted(list({item["path"] for item in records if PATH_ID_PATTERN.fullmatch(item["path"])}))

    print(f"Parsed records: {len(records)}")
    print(f"Invalid lines: {len(invalid_lines)}")
    if invalid_lines:
        for num, line in invalid_lines:
            print(f"  Line {num}: {line}")
            
    print(f"Levels: {dict(levels)}")
    print(f"Methods: {dict(methods)}")
    print(f"Users: {dict(users)}")
    print(f"Statuses: {dict(statuses)}")

    print("\nERROR records:")
    for item in errors:
        print(f"  {item['time']} user={item['user']} status={item['status']} path={item['path']}")

    print("\nSlow requests (>= 300 ms):")
    for item in slow:
        print(f"  {item['duration']} ms | {item['method']} {item['path']} | user={item['user']}")

    print("\nHTTP Error Statuses (status >= 400):")
    for item in http_errors:
        print(f"  status={item['status']} | {item['method']} {item['path']} | user={item['user']}")

    print("\nUnique Paths with Numeric ID:")
    for path in id_paths:
        print(f"  {path}")


if __name__ == "__main__":
    main()