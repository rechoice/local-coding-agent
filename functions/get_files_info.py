import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    # Check directory is accessible
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if valid_target_dir == False:
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    
    if os.path.isdir(target_dir) == False:
        return (f'Error: "{directory}" is not a directory')

    try:
        contents_list = os.listdir(target_dir)
        contents_info = []

        for name in contents_list:
            file_path = os.path.join(target_dir, name)
            file_size = os.path.getsize(file_path)
            file_is_dir = os.path.isdir(file_path)
            file_info = f"- {name}: file_size={file_size} bytes, is_dir={file_is_dir}"
            contents_info.append(file_info)
        return "\n".join(contents_info)
    except Exception as e:
        return f"Error: {e}"

                       