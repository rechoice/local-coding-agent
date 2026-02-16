import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    """List information about files in a directory under a constrained working directory.

    Args:
        working_directory (str): Base directory that the agent is allowed to access.
        directory (str, optional): Relative path from the working directory to inspect. Defaults to ".".

    Returns:
       str: A newline-separated description of each entry in the target directory, or an error message starting with "Error:" if the path is invalid or an exception occurs.
    """

    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    # Check directory is accessible
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    
    if not os.path.isdir(target_dir):
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
    

# schema
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from",
            ),
        },
    ),
)

                       