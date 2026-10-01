import re
from collections import defaultdict

from database import add_alert


EVENT_PATTERN = re.compile(
    r"source=(\d+\.\d+\.\d+\.\d+)\s+"
    r"destination_port=(\d+)"
)


def analyze_events(filename, threshold=5):
    connections = defaultdict(int)

    with open(
        filename,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as log_file:

        for line in log_file:
            match = EVENT_PATTERN.search(line)

            if not match:
                continue

            source_ip = match.group(1)
            destination_port = int(match.group(2))

            key = (source_ip, destination_port)

            connections[key] += 1

    alerts = []

    for (source_ip, port), attempts in connections.items():

        if attempts >= threshold:

            alert_type = "Repeated connection attempts"

            add_alert(
                source_ip,
                port,
                attempts,
                alert_type
            )

            alerts.append({
                "source_ip": source_ip,
                "port": port,
                "attempts": attempts,
                "type": alert_type
            })

    return alerts
