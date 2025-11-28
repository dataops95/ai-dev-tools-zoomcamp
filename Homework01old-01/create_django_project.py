import subprocess
import sys
import os
from typing import Optional, Tuple

def run_command(command: list[str], cwd: Optional[str] = None) -> Tuple[bool, str]:
    """
    Runs a shell command and returns success status and output.

    Args:
        command (list[str]): Command to run as a list of strings.
        cwd (Optional[str]): Working directory. Defaults to None (current directory).

    Returns:
        Tuple[bool, str]: (success, output)
    """
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def create_django_project_and_app(
    project_name: str,
    app_name: str,
    venv_name: str = "myenv",
) -> bool:
    """
    Creates a Django project and app using `uv` and Django's management commands.

    Args:
        project_name (str): Name of the Django project.
        app_name (str): Name of the Django app.
        venv_name (str): Name of the virtual environment. Defaults to "myenv".

    Returns:
        bool: True if successful, False otherwise.
    """
    # Step 1: Construct the path to the virtual environment's Python executable
    if sys.platform == "win32":
        venv_python = os.path.join(venv_name, "Scripts", "python.exe")
    else:
        venv_python = os.path.join(venv_name, "bin", "python")

    # Step 2: Create Django project
    print(f"Creating Django project: {project_name}")
    success, output = run_command([venv_python, "-m", "django", "admin", "startproject", project_name])
    if not success:
        print(f"Failed to create project: {output}")
        return False

    # Step 3: Create Django app
    print(f"Creating Django app: {app_name}")
    success, output = run_command(
        [venv_python, "-m", "django", "admin", "startapp", app_name],
        cwd=project_name,
    )
    if not success:
        print(f"Failed to create app: {output}")
        return False

    # Step 4: Register the app in the project's INSTALLED_APPS
    installed_apps_file = os.path.join(project_name, project_name, "settings.py")
    try:
        with open(installed_apps_file, "r") as f:
            settings_content = f.read()

        # Add the app to INSTALLED_APPS
        if f'"{app_name}",' not in settings_content:
            settings_content = settings_content.replace(
                "INSTALLED_APPS = [",
                f"INSTALLED_APPS = [\n        '{app_name}',",
            )
            with open(installed_apps_file, "w") as f:
                f.write(settings_content)
            print(f"App '{app_name}' registered in INSTALLED_APPS.")
        else:
            print(f"App '{app_name}' is already in INSTALLED_APPS.")
    except Exception as e:
        print(f"Failed to update settings.py: {e}")
        return False

    print("Django project and app created successfully!")
    return True

# Example usage
if __name__ == "__main__":
    project_name = "myproject"
    app_name = "myapp"
    success = create_django_project_and_app(project_name, app_name)
    if success:
        print(f"Project '{project_name}' and app '{app_name}' are ready!")
    else:
        print("Failed to create project or app.")
