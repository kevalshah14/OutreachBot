from fastapi import FastAPI, File, UploadFile, HTTPException
from app.services.file_processor import process_file
from app.services.map_generator import generate_mind_map
from fastapi.responses import JSONResponse
import os
import json
from uuid import uuid4

app = FastAPI()

JSON_FILES_DIR = "app/data/json_files/"

# Ensure the JSON_FILES_DIR exists
os.makedirs(JSON_FILES_DIR, exist_ok=True)


@app.post("/process-and-generate/")
async def process_and_generate(file: UploadFile = File(...)):
    """
    Unified endpoint to process a file, generate a mind map, and save it as JSON.

    Args:
        file (UploadFile): The uploaded file from the client.

    Returns:
        dict: File name of the saved mind map JSON.
    """
    try:
        # Step 1: Read and process the uploaded file
        content = await file.read()
        processed_data = process_file(content, file.filename)

        # Step 2: Generate a mind map from the processed content
        mind_map = generate_mind_map(processed_data)
        if mind_map is None:
            raise HTTPException(status_code=500, detail="Error generating mind map.")

        # Step 3: Save the mind map to a JSON file
        json_file_name = f"{uuid4().hex}.json"
        json_file_path = os.path.join(JSON_FILES_DIR, json_file_name)
        with open(json_file_path, "w") as json_file:
            json.dump(mind_map, json_file)

        # Step 4: Return the saved file name
        return {"status": "success", "file_name": json_file_name}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@app.get("/get-json/{file_name}")
async def get_json_file(file_name: str):
    """
    API endpoint to retrieve a JSON file by name (from the URL path).

    Args:
        file_name (str): Name of the JSON file to retrieve.

    Returns:
        JSONResponse: The contents of the JSON file.
    """
    try:
        # Construct the full path to the JSON file
        file_path = os.path.join(JSON_FILES_DIR, file_name)

        # Check if the file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="JSON file not found.")

        # Read and parse the JSON file
        with open(file_path, "r") as file:
            data = json.load(file)

        # Return the JSON data
        return JSONResponse(content=data)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="JSON file not found.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Error decoding JSON file.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


# Optional: Keep the original `/upload/` endpoint for independent testing
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    API endpoint to upload and process a file.

    Args:
        file (UploadFile): The uploaded file from the client.

    Returns:
        dict: Processed data from the file.
    """
    try:
        content = await file.read()
        processed_data = process_file(content, file.filename)
        return {"status": "success", "data": processed_data}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
