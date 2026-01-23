import os
import shutil
import datetime
from typing import List, Dict, Union, Optional

class FileUtils:
    """
    A utility class for performing common file system operations.
    Designed to be compatible with MCP tools, providing descriptive methods and detailed documentation.
    """

    @staticmethod
    def read_file_content(file_path: str) -> str:
        """
        Reads the content of a file and returns it as a string.

        Args:
            file_path (str): The absolute or relative path to the file to be read.

        Returns:
            str: The content of the file.

        Raises:
            FileNotFoundError: If the file does not exist.
            IOError: If there is an error reading the file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise IOError(f"Error reading file '{file_path}': {str(e)}")

    @staticmethod
    def write_content_to_file(file_path: str, content: str, mode: str = 'w') -> str:
        """
        Writes content to a file. Creates the file and parent directories if they do not exist.

        Args:
            file_path (str): The absolute or relative path to the file.
            content (str): The content to write to the file.
            mode (str): The file opening mode ('w' for write/overwrite, 'a' for append). Defaults to 'w'.

        Returns:
            str: A success message indicating the file was written.

        Raises:
            IOError: If there is an error writing to the file.
        """
        try:
            # Ensure directory exists
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote to file '{file_path}'."
        except Exception as e:
            raise IOError(f"Error writing to file '{file_path}': {str(e)}")

    @staticmethod
    def list_directory_contents(directory_path: str = ".") -> List[Dict[str, Union[str, bool, int]]]:
        """
        Lists the files and directories within a specified directory.

        Args:
            directory_path (str): The path to the directory to list. Defaults to current directory.

        Returns:
            List[Dict[str, Union[str, bool, int]]]: A list of dictionaries, where each dictionary contains
            information about a file or directory (name, path, is_directory, size).

        Raises:
            FileNotFoundError: If the directory does not exist.
            NotADirectoryError: If the path is not a directory.
        """
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory '{directory_path}' not found.")
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Path '{directory_path}' is not a directory.")

        items = []
        for entry in os.scandir(directory_path):
            info = {
                "name": entry.name,
                "path": entry.path,
                "is_directory": entry.is_dir(),
                "size": entry.stat().st_size if entry.is_file() else 0
            }
            items.append(info)
        return items

    @staticmethod
    def check_file_exists(file_path: str) -> bool:
        """
        Checks if a file or directory exists at the specified path.

        Args:
            file_path (str): The path to check.

        Returns:
            bool: True if the file or directory exists, False otherwise.
        """
        return os.path.exists(file_path)

    @staticmethod
    def delete_file(file_path: str) -> str:
        """
        Deletes a file at the specified path.

        Args:
            file_path (str): The path to the file to delete.

        Returns:
            str: A success message.

        Raises:
            FileNotFoundError: If the file does not exist.
            IsADirectoryError: If the path points to a directory (use delete_directory instead).
            IOError: If the file could not be deleted.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found.")
        if os.path.isdir(file_path):
            raise IsADirectoryError(f"Path '{file_path}' is a directory. Use delete_directory instead.")
        
        try:
            os.remove(file_path)
            return f"Successfully deleted file '{file_path}'."
        except Exception as e:
            raise IOError(f"Error deleting file '{file_path}': {str(e)}")

    @staticmethod
    def get_file_metadata(file_path: str) -> Dict[str, Union[str, int, float]]:
        """
        Retrieves metadata for a specific file.

        Args:
            file_path (str): The path to the file.

        Returns:
            Dict[str, Union[str, int, float]]: A dictionary containing file metadata 
            (path, size_bytes, created_time, modified_time).

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found.")
        
        stat = os.stat(file_path)
        return {
            "path": file_path,
            "size_bytes": stat.st_size,
            "created_time": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_time": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
        }
