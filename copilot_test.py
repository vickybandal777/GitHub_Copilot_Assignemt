import subprocess
from pathlib import Path


def format_uptime(seconds: float) -> str:
	total_seconds = int(seconds)
	days, remainder = divmod(total_seconds, 24 * 60 * 60)
	hours, remainder = divmod(remainder, 60 * 60)
	minutes, seconds = divmod(remainder, 60)

	parts = []
	if days:
		parts.append(f"{days} day{'s' if days != 1 else ''}")
	if hours:
		parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
	if minutes:
		parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
	if not parts:
		parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

	return ", ".join(parts)


def get_system_uptime() -> str:
	try:
		result = subprocess.run(
			["uptime", "-p"],
			check=True,
			capture_output=True,
			text=True,
		)
		return result.stdout.strip().removeprefix("up ")
	except (subprocess.CalledProcessError, FileNotFoundError, OSError):
		try:
			uptime_text = Path("/proc/uptime").read_text().split()[0]
			return format_uptime(float(uptime_text))
		except (OSError, ValueError, IndexError) as exc:
			raise RuntimeError("Unable to determine system uptime") from exc


def main() -> None:
	try:
		uptime = get_system_uptime()
		print(f"System uptime: {uptime}")
	except RuntimeError as exc:
		print(f"Error: {exc}")


if __name__ == "__main__":
	main()
