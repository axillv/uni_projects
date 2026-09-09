import os
import subprocess

import tomlkit


def resolve_dependencies(group, dependency_groups, resolved=None, seen=None):
    """Recursively resolve dependencies for a group."""
    if resolved is None:
        resolved = set()
    if seen is None:
        seen = set()

    # Prevent infinite recursion by tracking seen groups
    if group in seen:
        return resolved
    seen.add(group)

    dependencies = dependency_groups.get(group, [])
    for dep in dependencies:
        if isinstance(dep, dict) and "include-group" in dep:
            # Resolve included groups recursively
            included_group = dep["include-group"]
            resolve_dependencies(included_group, dependency_groups, resolved, seen)
        else:
            # Add direct dependencies
            resolved.add(dep)

    return resolved


# Load the pyproject.toml file using tomlkit
pyproject_path = "pyproject.toml"
with open(pyproject_path, "r") as file:
    pyproject_data = tomlkit.parse(file.read())

# Extract dependency groups from pyproject.toml
dependency_groups = pyproject_data.get("dependency-groups", {})

# Manual mapping of dependency groups to their respective module paths
group_to_path = {
    "config": "config",
    "generic-prod": "producers/base",
    "weather-prod": "producers/weather",
    "gbfs-prod": "producers/gbfs",
    "spark": "spark",
}

# Iterate over each dependency group and generate requirements.txt
for group, path in group_to_path.items():
    # Resolve dependencies for the group
    resolved_dependencies = resolve_dependencies(group, dependency_groups)

    # Define the output folder based on the manual mapping
    output_folder = path
    os.makedirs(output_folder, exist_ok=True)  # Ensure the folder exists

    output_file = os.path.join(output_folder, "requirements.txt")

    try:
        print(f"Generating requirements for {group}...")

        # Write the resolved dependencies to the requirements file
        with open(output_file, "w") as f:
            for dep in resolved_dependencies:
                f.write(f"{dep}\n")

        print(f"Requirements for {group} saved to {output_file}")
    except Exception as e:
        print(f"Failed to generate requirements for {group}: {e}")

print("All requirements files generated.")
