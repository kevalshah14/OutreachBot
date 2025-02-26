import os
from markitdown import MarkItDown
from openai import OpenAI
import tempfile

def process_file(file_content: bytes, file_name: str) -> dict:
    """
    Process the uploaded file using MarkItDown and return JSON data.

    Args:
        file_content (bytes): The content of the uploaded file in bytes.
        file_name (str): The original name of the uploaded file.

    Returns:
        dict: Processed JSON data containing the converted content and metadata.
    """
    try:
        # Ensure environment variables are set
        API_KEY = os.getenv('OPENAI_API_KEY')
        BASE_URL = os.getenv('BASE_URL')

        if API_KEY:
            client = OpenAI(api_key=API_KEY)
        else:
            client = None  # No LLM client if API_KEY is not set

        # Initialize MarkItDown
        md = MarkItDown(llm_client=client, llm_model="gpt-4o" if client else None)

        # Save the file temporarily with the original file name
        temp_dir = tempfile.gettempdir()  # Use system temp directory
        temp_file_path = os.path.join(temp_dir, file_name)

        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(file_content)

        # Convert the file using MarkItDown
        result = md.convert(temp_file_path)

        # Extract the processed content and metadata
        processed_content = result.text_content
        metadata = result.metadata if hasattr(result, "metadata") else None

        # Clean up temporary file
        os.remove(temp_file_path)

        # Return the processed content and metadata
        return {
            "processed_content": processed_content,
            "metadata": metadata
        }

    except UnicodeDecodeError:
        raise ValueError("Failed to decode the file. Ensure it's a valid text file.")
    except FileNotFoundError:
        raise ValueError("Temporary file not found during processing.")
    except Exception as e:
        raise ValueError(f"Unexpected error while processing the file: {e}")
