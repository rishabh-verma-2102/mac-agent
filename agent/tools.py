import psutil


def get_battery():
    """
    Retrieves the current battery charge percentage.

    Returns:
        dict: A dictionary containing the integer percentage of remaining battery life.
        Example: {"battery_percent": 85}
    """
    try:
        battery = psutil.sensors_battery()
        if battery:
            return {"battery_percent": int(battery.percent)}
        else:
            return "get_battery tool failure"
    except Exception:
        return "get_battery tool failure"


def get_disk():
    """
    Retrieves the current disk storage status of the primary drive.

    Returns:
        dict: A dictionary containing 'disk_details' with 'total', 'free', and 'used' space in Gigabytes (GB).
        Example: {"disk_details": {"total": 500.0, "free": 250.5, "used": 249.5}}
    """
    try:
        usage = psutil.disk_usage('/')
        gb_divisor = 1024 ** 3

        return {
            "disk_details": {
                "total": round(usage.total / gb_divisor, 2),
                "free": round(usage.free / gb_divisor, 2),
                "used": round(usage.used / gb_divisor, 2)
            }
        }
    except Exception:
        return "get_disk tool failure"


def get_cpu():
    """
    Retrieves the current instantaneous CPU utilization percentage.

    Returns:
        dict: A dictionary containing 'cpu_usage_percent' as a float representing the total system load.
        Example: {"cpu_usage_percent": 12.5}
    """
    try:
        percent = psutil.cpu_percent(interval=1)
        return {"cpu_usage_percent": round(percent, 1)}
    except Exception:
        return "get_cpu tool failure"


def get_memory():
    """
    Retrieves the system's RAM usage statistics.

    Returns:
        dict: A dictionary containing 'memory_details' with 'total', 'free', and 'used' memory in Gigabytes (GB).
        Example: {"memory_details": {"total": 17179869184, "free": 8589934592, "used": 8589934592}}
    """
    try:
        mem = psutil.virtual_memory()
        gb_divisor = 1024 ** 3

        return {
            "memory_details": {
                "total": round(mem.total / gb_divisor, 2),
                "free": round(mem.available / gb_divisor, 2),
                "used": round((mem.total - mem.available) / gb_divisor, 2)
            }
        }
    except Exception:
        return "get_memory tool failure"
