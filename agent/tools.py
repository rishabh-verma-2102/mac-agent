# import psutil
#
#
# def get_battery():
#     """To retrieve battery percentage of macbook
#
#         Returns:
#             dict: A dictionary containing the current battery charge percentage under the key 'battery_percent'.
#             Example: {"battery_percent": 85}
#         """
#     return {"battery_percent": psutil.sensors_battery().percent}
#
#
# def get_disk():
#     """To retrieve total, free and used disk space in macbook
#
#         Returns:
#             dict: A dictionary containing disk usage details. The 'disk_details' key holds a nested dictionary
#             with the total, free, and used disk space values, all calculated and returned in Gigabytes (GB).
#             Example: {"disk_details": {"total": 500.0, "free": 300.5, "used:": 199.5}}
#         """
#     d = psutil.disk_usage('/')
#     return {
#         "disk_details": {"total": d.total / (1024 ** 3), "free": d.free / (1024 ** 3), "used:": d.used / (1024 ** 3)}}
#
#
# def get_cpu():
#     """To retrieve cpu usage percentage of macbook
#
#         Returns:
#             dict: A dictionary containing the instantaneous overall CPU utilization percentage under the key 'cpu_usage_percent'.
#             Example: {"cpu_usage_percent": 15.2}
#         """
#     return {"cpu_usage_percent": psutil.cpu_percent(interval=1)}
#
#
# def get_memory():
#     """To retrieve memory usage, total, available and used for macbook
#
#         Returns:
#             dict: A dictionary containing virtual memory details. The 'memory_details' key holds a nested dictionary
#             with the total, available (free), and used memory values, all returned in Bytes.
#             Example: {"memory_details": {"total": 17179869184, "free": 8589934592, "used:": 8589934592}}
#         """
#     m = psutil.virtual_memory()
#     return {"memory_details": {"total": m.total, "free": m.available, "used:": m.used}}

import subprocess
import re


def _run_command(command):
    """Helper to run a shell command and return the output as a string."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            text=True,
            capture_output=True,
            check=False
        )
        return result.stdout.strip()
    except Exception:
        return "Failed to run command in shell."


def get_battery():
    """
    Retrieves the current battery charge percentage.

    Returns:
        dict: A dictionary containing the integer percentage of remaining battery life.
        Example: {"battery_percent": 85}
    """
    try:
        output = _run_command("pmset -g batt")
        percent_match = re.search(r'(\d+)%', output)
        if percent_match:
            return {"battery_percent": int(percent_match.group(1))}
    except Exception:
        return "get_battery tool failure"


def get_disk():
    """
    Retrieves the current disk storage status of the primary drive.

    Returns:
        dict: A dictionary containing 'disk_details' with 'total', 'free', and 'used' space in Gigabytes (GB).
        Example: {"disk_details": {"total": 500.0, "free": 250.5, "used": 249.5}}
    """
    output = _run_command("df -k /")
    try:
        lines = output.splitlines()
        if len(lines) >= 2:
            parts = lines[1].split()
            # Convert byte blocks to GB
            return {
                "disk_details": {
                    "total": round(int(parts[1]) / 1048576, 2),
                    "free": round(int(parts[3]) / 1048576, 2),
                    "used": round(int(parts[2]) / 1048576, 2)
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
    output = _run_command("top -l 2 -n 0 | grep -E '^CPU'")
    try:
        lines = output.strip().splitlines()
        if lines:
            last_line = lines[-1]
            user_match = re.search(r'([\d\.]+)%\s+user', last_line)
            sys_match = re.search(r'([\d\.]+)%\s+sys', last_line)
            if user_match and sys_match:
                return {"cpu_usage_percent": round(float(user_match.group(1)) + float(sys_match.group(1)), 1)}
    except Exception:
        return "get_cpu tool failure"


def get_memory():
    """
    Retrieves the system's RAM usage statistics.

    Returns:
        dict: A dictionary containing 'memory_details' with 'total', 'free', and 'used' memory in Bytes.
        Example: {"memory_details": {"total": 17179869184, "free": 8589934592, "used": 8589934592}}
    """
    try:
        page_size_str = _run_command("sysctl -n hw.pagesize")
        page_size = int(page_size_str) if page_size_str.isdigit() else 16384

        # Get Total Memory
        mem_size_str = _run_command("sysctl -n hw.memsize")
        total_mem = int(mem_size_str) if mem_size_str.isdigit() else 0

        vm_stat_out = _run_command("vm_stat")
        vm_stats = {}
        for line in vm_stat_out.splitlines():
            if ":" in line:
                key, val = line.split(":")
                vm_stats[key.replace('.', '').strip()] = int(val.strip())

        pages_free = vm_stats.get("Pages free", 0)
        pages_inactive = vm_stats.get("Pages inactive", 0)

        available_mem = (pages_free + pages_inactive) * page_size
        used_mem = total_mem - available_mem

        return {
            "memory_details": {
                "total": total_mem,
                "free": available_mem,
                "used": used_mem
            }
        }
    except Exception:
        return "get_memory tool failure"
