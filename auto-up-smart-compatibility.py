import re
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import tempfile
import os


def run_pip_install_test(requirements_content):
    """Test if requirements can be installed by actually trying pip install"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(requirements_content)
        temp_path = temp_file.name

    try:
        # Test actual pip install with --dry-run
        result = subprocess.run(
            ["pip", "install", "--dry-run", "-r", temp_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode == 0, result.stderr, result.stdout
    except Exception as e:
        return False, str(e), ""
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def fix_dependency_conflicts(requirements_content):
    """Apply known fixes for common dependency conflicts"""
    lines = requirements_content.strip().split('\n')
    fixed_lines = []

    # Known conflict fixes
    conflict_fixes = {
        'numpy==2.3.1': 'numpy>=2.0.0,<2.3.0',  # OpenCV compatibility
        'numpy==2.3.0': 'numpy>=2.0.0,<2.3.0',
        'pillow>=11.3.0': 'pillow>=10.0.0',  # Broader compatibility
        'scipy>=1.16.0': 'scipy>=1.11.0',  # More compatible
    }

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            fixed_lines.append(line)
            continue

        # Check for exact matches first
        if line in conflict_fixes:
            fixed_lines.append(conflict_fixes[line])
            continue

        # Check for pattern matches
        fixed = False
        for pattern, replacement in conflict_fixes.items():
            if line.startswith(pattern.split('=')[0] + '==') or line.startswith(pattern.split('>')[0]):
                fixed_lines.append(replacement)
                fixed = True
                break

        if not fixed:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def make_requirements_flexible(requirements_content):
    """Convert pinned versions to flexible ranges"""
    lines = requirements_content.strip().split('\n')
    flexible_lines = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            flexible_lines.append(line)
            continue

        # Convert exact pins to flexible ranges
        if '==' in line:
            package_name = line.split('==')[0]
            version = line.split('==')[1]

            # Extract major.minor version
            version_parts = version.split('.')
            if len(version_parts) >= 2:
                major = version_parts[0]
                minor = version_parts[1]
                # Allow patch updates
                flexible_line = f"{package_name}>={major}.{minor}.0"
            else:
                flexible_line = f"{package_name}>={version}"

            flexible_lines.append(flexible_line)
        else:
            flexible_lines.append(line)

    return '\n'.join(flexible_lines)


def progressive_fix_requirements(original_content):
    """Try progressively more flexible approaches until one works"""
    strategies = [
        ("Original", original_content),
        ("Fixed conflicts", fix_dependency_conflicts(original_content)),
        ("Flexible versions", make_requirements_flexible(original_content)),
        ("Flexible + Fixed", make_requirements_flexible(fix_dependency_conflicts(original_content)))
    ]

    print("🔍 Testing different compatibility strategies...\n")

    for strategy_name, content in strategies:
        print(f"Testing: {strategy_name}")
        success, error, output = run_pip_install_test(content)

        if success:
            print(f"✅ {strategy_name} - SUCCESS!")
            return content, strategy_name
        else:
            print(f"❌ {strategy_name} - Failed")
            if "conflict" in error.lower() or "incompatible" in error.lower():
                # Extract the conflicting packages for debugging
                conflict_lines = [line for line in error.split('\n') if
                                  'depends on' in line or 'conflict' in line.lower()]
                if conflict_lines:
                    print(f"   Conflict details: {conflict_lines[0]}")
            print()

    return None, "All strategies failed"


def upgrade_requirements_smart_v2(input_path):
    """Smart upgrade using pip's actual dependency resolution"""
    output_file = input_path.replace(".txt", "-compatible.txt")

    print("📖 Reading original requirements...")
    with open(input_path, 'r') as f:
        original_content = f.read()

    # Test original first
    print("🧪 Testing original requirements...")
    success, error, output = run_pip_install_test(original_content)

    if success:
        print("✅ Original requirements are already compatible!")
        messagebox.showinfo("Already Compatible", "Your requirements.txt is already compatible!")
        return

    print("❌ Original requirements have conflicts")
    print("🔧 Attempting to fix...\n")

    # Try progressive fixes
    fixed_content, strategy = progressive_fix_requirements(original_content)

    if fixed_content:
        # Save the fixed version
        with open(output_file, 'w') as f:
            f.write(fixed_content)

        print(f"\n✅ SUCCESS! Fixed using strategy: {strategy}")
        print(f"💾 Compatible requirements saved to: {output_file}")

        # Show what changed
        original_lines = set(original_content.strip().split('\n'))
        fixed_lines = set(fixed_content.strip().split('\n'))

        changes = []
        for line in original_lines:
            if line not in fixed_lines:
                # Find what it changed to
                package_name = line.split('==')[0] if '==' in line else line.split('>=')[0] if '>=' in line else line
                for fixed_line in fixed_lines:
                    if fixed_line.startswith(package_name):
                        changes.append(f"{line} → {fixed_line}")
                        break

        if changes:
            print("\n📝 Changes made:")
            for change in changes[:10]:  # Show first 10 changes
                print(f"  {change}")
            if len(changes) > 10:
                print(f"  ... and {len(changes) - 10} more changes")

        messagebox.showinfo("Success!",
                            f"Requirements fixed using: {strategy}\n\n"
                            f"File saved as: {os.path.basename(output_file)}\n"
                            f"Made {len(changes)} changes to resolve conflicts.")
    else:
        print("❌ Could not automatically fix the dependency conflicts")
        print("💡 Try manually adjusting versions of conflicting packages")
        messagebox.showerror("Failed",
                             "Could not automatically resolve all conflicts.\n\n"
                             "Try manually adjusting the versions of packages that are conflicting.")


def create_basic_ml_requirements(output_path):
    """Create a basic ML requirements file with known-good versions"""
    basic_requirements = """# Basic Flask web framework
flask>=3.0.0
flask-cors>=6.0.0
werkzeug>=3.0.0

# AWS SDK
boto3>=1.35.0
botocore>=1.35.0

# Computer Vision & ML
opencv-python>=4.8.0
numpy>=1.24.0,<2.3.0
pillow>=10.0.0
scipy>=1.11.0
pandas>=2.0.0

# PyTorch (CPU version for faster install)
torch>=2.0.0
torchvision>=0.15.0

# YOLO
ultralytics>=8.0.0

# Utilities
python-dotenv>=1.0.0
gunicorn>=21.0.0
psutil>=5.9.0

# Testing
pytest>=7.0.0
pytest-flask>=1.2.0
"""

    with open(output_path, 'w') as f:
        f.write(basic_requirements.strip())

    print(f"✅ Basic ML requirements template created: {output_path}")


def main():
    root = tk.Tk()
    root.withdraw()

    # Ask user what they want to do
    choice = messagebox.askyesnocancel(
        "Requirements Fixer",
        "What would you like to do?\n\n"
        "YES = Fix existing requirements.txt file\n"
        "NO = Create basic ML template (recommended)\n"
        "CANCEL = Exit"
    )

    if choice is None:  # Cancel
        return

    if choice:  # YES - Fix existing file
        file_path = filedialog.askopenfilename(
            title="Select requirements.txt file to fix",
            filetypes=[("Text Files", "*.txt")]
        )

        if not file_path:
            messagebox.showwarning("Cancelled", "No file selected.")
            return

        upgrade_requirements_smart_v2(file_path)

    else:  # NO - Create template
        save_path = filedialog.asksaveasfilename(
            title="Save basic requirements template",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            initialvalue="requirements-basic.txt"
        )

        if save_path:
            create_basic_ml_requirements(save_path)
            messagebox.showinfo("Template Created", f"Basic ML requirements template saved to:\n{save_path}")


if __name__ == "__main__":
    main()