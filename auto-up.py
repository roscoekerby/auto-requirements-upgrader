import re
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def get_latest_version(package_name):
    try:
        result = subprocess.run(
            ["pip", "index", "versions", package_name],
            capture_output=True,
            text=True
        )
        lines = result.stdout.splitlines()
        for line in lines:
            if "Available versions:" in line:
                versions = line.split("Available versions:")[-1].strip().split(", ")
                return versions[0]  # Latest version is listed first
    except Exception as e:
        print(f"Error checking {package_name}: {e}")
    return None

def upgrade_requirements_file(input_path):
    output_file = input_path.replace(".txt", "-upgraded.txt")
    upgraded_lines = []

    with open(input_path, "r") as file:
        for line in file:
            original_line = line.strip()
            if not original_line or original_line.startswith("#"):
                upgraded_lines.append(original_line)
                continue

            match = re.match(r"([a-zA-Z0-9\-_]+)(==([^\s]+))?", original_line)
            if match:
                package = match.group(1)
                latest_version = get_latest_version(package)
                if latest_version:
                    upgraded_line = f"{package}=={latest_version}"
                    print(f"{package}: {match.group(3)} → {latest_version}")
                else:
                    upgraded_line = original_line
            else:
                upgraded_line = original_line

            upgraded_lines.append(upgraded_line)

    with open(output_file, "w") as file:
        file.write("\n".join(upgraded_lines))

    print(f"\n✅ Upgraded requirements saved to `{output_file}`")
    messagebox.showinfo("Done", f"Upgraded file saved as:\n{output_file}")

def main():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select requirements.txt file",
        filetypes=[("Text Files", "*.txt")]
    )
    if not file_path:
        messagebox.showwarning("Cancelled", "No file selected.")
        return

    upgrade_requirements_file(file_path)

if __name__ == "__main__":
    main()
