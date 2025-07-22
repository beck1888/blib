import os
import datetime
from pathlib import Path

def get_user_setup():
    """Gets project details from the user."""
    project_name = input("Enter the project name (e.g., my-next-app): ")
    project_root = input("Enter the absolute path to the project's root directory: ")
    output_path = input("Enter the directory where you want to save the export: ")
    output_filename = input("Enter the name for the exported markdown file (e.g., export.md): ")
    return project_name, project_root, output_path, output_filename

def generate_tree(dir_path, prefix="", ignored_dirs=None):
    """Generates a visual tree structure of the directory."""
    if ignored_dirs is None:
        ignored_dirs = {'node_modules', '.git'}
    lines = []
    items = sorted(os.listdir(dir_path))
    for i, item in enumerate(items):
        path = os.path.join(dir_path, item)
        is_last = i == len(items) - 1
        if os.path.isdir(path) and item in ignored_dirs:
            continue
        lines.append(f"{prefix}{'└── ' if is_last else '├── '}{item}{'/' if os.path.isdir(path) else ''}")
        if os.path.isdir(path):
            new_prefix = prefix + ("    " if is_last else "│   ")
            lines.extend(generate_tree(path, prefix=new_prefix, ignored_dirs=ignored_dirs))
    return lines

def is_binary_file(filepath):
    """Checks if a file is likely binary."""
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
            return b'\0' in chunk
    except IOError:
        return False

def get_files_to_export(project_root, ignored_files):
    """Gathers files to be exported, skipping ignored and binary files."""
    exported_files = []
    skipped_files = []
    ignore_set = set(ignored_files)

    for root, dirs, files in os.walk(project_root):
        # Remove ignored directories from traversal
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git']]

        for name in files:
            file_path = Path(root) / name
            relative_path = file_path.relative_to(project_root)
            if str(relative_path) in ignore_set:
                skipped_files.append(('File', str(relative_path), 'Ignored'))
                continue
            if is_binary_file(file_path):
                skipped_files.append(('File', str(relative_path), 'Binary'))
                continue
            exported_files.append(file_path)

    # Add ignored top-level directories to skipped list
    for item in os.listdir(project_root):
        if os.path.isdir(os.path.join(project_root, item)) and item in ['node_modules', '.git']:
            skipped_files.append(('Directory', item, 'Ignored'))

    return exported_files, skipped_files

def main():
    """Main function to run the CLI tool."""
    # --- User Setup ---
    project_name, project_root, output_path, output_filename = get_user_setup()

    # --- Date and Time ---
    now = datetime.datetime.now()
    date_str = now.strftime("%B %d, %Y")
    time_str = now.strftime("%I:%M %p (UTC%z)")

    # --- Generate Project Structure ---
    tree_lines = generate_tree(project_root)
    project_structure = f"{Path(project_root).name}/\n" + "\n".join(tree_lines)

    # --- Identify Skipped and Exported Files ---
    gitignore_path = os.path.join(project_root, '.gitignore')
    ignored_patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            ignored_patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            ignored_patterns.append('.env.local') # Manually add common ignored files

    exported_files, skipped_files_list = get_files_to_export(project_root, ignored_patterns)

    # --- Build Markdown Content ---
    markdown_content = f"# Export of {project_name}\n\n"
    markdown_content += f"## Info\nDate: {date_str}\n\nTime: {time_str}\n\nRoot file path: `{project_root}`\n\n"
    markdown_content += f"## Project structure\n```text\n{project_structure}\n```\n\n"
    markdown_content += "## Files Skipped In Export\n\n|Type|Path|Reason|\n|-|-|-|\n"
    for file_type, path, reason in sorted(skipped_files_list):
        markdown_content += f"|{file_type}|`{path}`|{reason}|\n"
    markdown_content += "\n"

    markdown_content += "## Exported Contents\n\n"
    for i, file_path in enumerate(exported_files):
        relative_path = file_path.relative_to(project_root)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            lang = file_path.suffix.lstrip('.')
            if lang in ['js', 'jsx', 'ts', 'tsx']:
                lang = 'tsx' # Default to tsx for syntax highlighting
            markdown_content += f"### File {i+1} of {len(exported_files)}: `{relative_path}`\n"
            markdown_content += f"```{lang}\n{content}\n```\n\n"
        except Exception as e:
            markdown_content += f"### File {i+1} of {len(exported_files)}: `{relative_path}`\n"
            markdown_content += f"Could not read file: {e}\n\n"

    # --- Write to File ---
    output_file = Path(output_path) / output_filename
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"\n✅ Project export has been successfully saved to:\n{output_file}")

if __name__ == "__main__":
    main()
else:
    raise RuntimeError("This script is meant to be run directly as a CLI tool, not imported.")