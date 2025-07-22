if input("STOP! This script is very verbose and not recommended beyond small projects. Continue (y/n)? ").lower() != 'y':
    print("Exiting...")
    exit(0)

import os
import datetime
from pathlib import Path

def get_user_setup():
    """Gets project details from the user."""
    print("--- Project Export Setup ---")
    project_name = input("Enter the project name (e.g., my-next-app): ")
    
    while True:
        project_root = input("Enter the absolute path to the project's root directory: ")
        if os.path.isdir(project_root):
            break
        print(f"❌ Error: The path '{project_root}' is not a valid directory. Please try again.")
        
    output_path = input("Enter the directory where you want to save the export: ")
    output_filename = input("Enter the name for the exported markdown file (e.g., export.md): ")
    
    os.makedirs(output_path, exist_ok=True)
    return project_name, Path(project_root), Path(output_path), output_filename

def is_binary_file(filepath):
    """Checks if a file is likely binary by checking for null bytes."""
    try:
        with open(filepath, 'rb') as f:
            return b'\0' in f.read(1024)
    except IOError:
        return False

def get_all_files_in_dir(dir_path):
    """Recursively gets all file paths in a directory."""
    files = []
    for root, _, filenames in os.walk(dir_path):
        for filename in filenames:
            files.append(Path(root) / filename)
    return files

def process_directory_interactively(current_path, project_root, files_to_export, files_to_ignore):
    """Recursively prompts the user to select files and directories for export."""
    print(f"\n--- Processing Directory: {current_path.relative_to(project_root) or '.'} ---")
    
    try:
        items = sorted(os.listdir(current_path))
        files = [f for f in items if (current_path / f).is_file()]
        dirs = [d for d in items if (current_path / d).is_dir()]
    except OSError as e:
        print(f"⚠️ Could not read directory {current_path}: {e}")
        return

    # 1. Ask about individual files in the current directory
    if files:
        print("\n[Files in this directory]")
    for filename in files:
        filepath = current_path / filename
        if is_binary_file(filepath):
            print(f"  - Ignoring binary file: {filename}")
            files_to_ignore.add(filepath)
            continue
        
        while True:
            choice = input(f"  Export '{filename}'? (y/n): ").lower()
            if choice in ['y', 'n']:
                if choice == 'y':
                    files_to_export.add(filepath)
                else:
                    files_to_ignore.add(filepath)
                break
            else:
                print("  Invalid input. Please enter 'y' or 'n'.")

    # 2. Ask about subdirectories
    if dirs:
        print("\n[Subdirectories in this directory]")
    for dirname in dirs:
        dirpath = current_path / dirname
        
        # Auto-ignore common large/system directories
        if dirname in ['.git', 'node_modules']:
            print(f"  - Automatically ignoring directory: {dirname}")
            all_nested_files = get_all_files_in_dir(dirpath)
            files_to_ignore.update(all_nested_files)
            # Also add the directory itself for the skipped list
            files_to_ignore.add(dirpath) 
            continue

        while True:
            prompt = (f"  Directory '{dirname}':\n"
                      f"    (2) Export All Files\n"
                      f"    (1) Select Files Interactively\n"
                      f"    (0) Ignore This Directory\n"
                      f"    Choose an option (2/1/0): ")
            choice = input(prompt)
            if choice in ['2', '1', '0']:
                break
            else:
                print("  Invalid input. Please enter 2, 1, or 0.")
        
        if choice == '0': # Ignore
            all_nested_files = get_all_files_in_dir(dirpath)
            files_to_ignore.update(all_nested_files)
            files_to_ignore.add(dirpath)
        elif choice == '2': # Export All
            all_nested_files = get_all_files_in_dir(dirpath)
            for f in all_nested_files:
                if is_binary_file(f):
                    files_to_ignore.add(f)
                else:
                    files_to_export.add(f)
        elif choice == '1': # Interactive
            process_directory_interactively(dirpath, project_root, files_to_export, files_to_ignore)

def generate_tree(root_path, all_paths):
    """Generates a visual tree structure from a list of paths."""
    tree = {}
    for path in all_paths:
        parts = path.relative_to(root_path).parts
        node = tree
        for part in parts:
            node = node.setdefault(part, {})

    def build_lines(node, prefix=""):
        lines = []
        items = sorted(node.keys())
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{item}")
            if node[item]:
                new_prefix = prefix + ("    " if is_last else "│   ")
                lines.extend(build_lines(node[item], new_prefix))
        return lines

    return f"{root_path.name}/\n" + "\n".join(build_lines(tree))


def main():
    """Main function to run the CLI tool."""
    project_name, project_root, output_path, output_filename = get_user_setup()
    
    files_to_export = set()
    files_to_ignore = set()

    # Start the interactive process from the root directory
    process_directory_interactively(project_root, project_root, files_to_export, files_to_ignore)

    # --- Prepare lists for Markdown ---
    exported_files_list = sorted(list(files_to_export))
    
    skipped_files_info = []
    for path in sorted(list(files_to_ignore)):
        relative_path = path.relative_to(project_root)
        if path.is_dir() or (path.name in ['.git', 'node_modules'] and path.is_dir()):
             skipped_files_info.append(('Directory', str(relative_path), 'Ignored'))
        else:
            reason = 'Binary' if is_binary_file(path) else 'Ignored'
            skipped_files_info.append(('File', str(relative_path), reason))

    # --- Date and Time ---
    now = datetime.datetime.now(datetime.timezone.utc)
    date_str = now.strftime("%B %d, %Y")
    time_str = now.strftime("%I:%M %p (UTC)")

    # --- Generate Project Structure ---
    all_included_paths = exported_files_list + [p for p in files_to_ignore if p.is_file()]
    project_structure = generate_tree(project_root, all_included_paths)

    # --- Build Markdown Content ---
    markdown_content = f"# Export of {project_name}\n\n"
    markdown_content += f"## Info\nDate: {date_str}\n\nTime: {time_str}\n\nRoot file path: `{project_root}`\n\n"
    markdown_content += f"## Project structure\n```text\n{project_structure}\n```\n\n"
    if skipped_files_info:
        markdown_content += "## Files Skipped In Export\n\n|Type|Path|Reason|\n|-|-|-|\n"
        for file_type, path_str, reason in skipped_files_info:
            markdown_content += f"|{file_type}|`{path_str}`|{reason}|\n"
        markdown_content += "\n"

    markdown_content += "## Exported Contents\n\n"
    total_files = len(exported_files_list)
    for i, file_path in enumerate(exported_files_list):
        relative_path = file_path.relative_to(project_root)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            lang = file_path.suffix.lstrip('.') if file_path.suffix else 'text'
            markdown_content += f"### File {i+1} of {total_files}: `{relative_path}`\n"
            markdown_content += f"```{lang}\n{content}\n```\n\n"
        except Exception as e:
            markdown_content += f"### File {i+1} of {total_files}: `{relative_path}`\n"
            markdown_content += f"```\nError reading file: {e}\n```\n\n"

    # --- Write to File ---
    output_file = output_path / output_filename
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"\n✅ All set! Project export has been successfully saved to:\n{output_file}")

if __name__ == "__main__":
    main()