from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Body, Request, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Annotated
from bson import ObjectId
from bson.json_util import dumps
import uvicorn
import json
from datetime import datetime
from pymongo import MongoClient
import logging
from secondTryToChange import changing_Everything
from createPDF import convert_and_save, convert_docx_to_pdf
from file_zip_handler import save_to_zip
from zipfile import ZipFile
from io import BytesIO
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logfile.log"),
        logging.StreamHandler()
    ]
)

app = FastAPI()
# How do i h8 this sh&t
# You cant even imagine!
origins = ["*"]
# New params for CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def add_timestamp_to_data(data):
    timestamp = datetime.utcnow().isoformat()
    data['timestamp'] = timestamp
    return data


def insert_data_to_mongodb(mongodb_address, database_name, collection_name, data):
    client = MongoClient(mongodb_address)
    database = client[database_name]

    # Add timestamp to the data
    data_with_timestamp = add_timestamp_to_data(data)

    collection = database[collection_name]
    result = collection.insert_one(data_with_timestamp)

    client.close()  # Close the MongoDB connection

    return result.inserted_id


def get_data_by_id_from_mongodb(mongodb_address, database_name, collection_name, document_id):
    client = MongoClient(mongodb_address)
    database = client[database_name]
    collection = database[collection_name]

    # Perform a query to retrieve data by _id
    query = {"_id": document_id}
    result = collection.find_one(query)

    client.close()  # Close the MongoDB connection

    return result


def compare_json(json1: Dict, json2: Dict) -> Dict:
    """
    Compare two JSON objects and return the fields that are different.
    """
    differences = {}
    for key in json1.keys():
        if key in json2:
            if json1[key] != json2[key]:
                differences[key] = {"new": json1[key], "old": json2[key]}
        else:
            differences[key] = {"new": json1[key], "old": None}

    for key in json2.keys():
        if key not in json1:
            differences[key] = {"new": None, "old": json2[key]}

    return differences


def get_database():
    client = MongoClient("mongodb://bulbaman.me:16017")  # Update with your MongoDB connection string
    db = client["newest_db_to_Hack"]  # Update with your database name
    yield db
    client.close()


async def process_form_data(background_tasks: BackgroundTasks, files: List[UploadFile], key: str):
    """
    Event handler to process form data with a key and files.
    """
    # You can perform any processing logic here
    # For example, save the files or do something with the key

    # In this example, we'll just print the key and file details
    print(f"Received key: {key}")

    # Prepare file information for saving to a zip archive
    files_info = [{'filename': file.filename, 'content': await file.read()} for file in files]

    # Enqueue the task to save files to a zip archive
    background_tasks.add_task(save_to_zip, files_info, zip_filename='output.zip')


# Global variable to store the filename
uploaded_filename = None

@app.post("/back/upload_file")
async def upload_file(file: UploadFile = File(...)):
    global uploaded_filename
    # Save the uploaded file with the name "dropped_file"
    uploaded_filename = file.filename  # Keep the file extension
    with open(uploaded_filename, "wb") as f:
        f.write(file.file.read())

    # Store the filename in the global variable
    uploaded_filename = uploaded_filename

    return {"filename": uploaded_filename}

# Raw method
@app.get("/back/download_zip")
async def download_file():
    global uploaded_filename
    # Check if a filename is stored in the global variable
    if not uploaded_filename:
        raise HTTPException(status_code=404, detail="File not found")

    # Create a zip archive
    zip_filename = "output.zip"
    with ZipFile(zip_filename, 'w') as zip_file:
        # Add the dropped file to the zip archive
        zip_file.write(uploaded_filename)

    # Return the zip archive as a response
    return FileResponse(zip_filename, media_type='application/zip', filename=zip_filename)

@app.post("/back/compare-json")
async def compare_json_files(json_body: Dict):
    """
    Compare the JSON in the request body with the JSON from a file in the API directory.
    """
    # Load the JSON from the file in the API directory
    with open("blocks.json", "r", encoding='utf-8') as file:
        json_file = json.load(file)

    # Compare the JSON objects
    differences = compare_json(json_body, json_file)

    # JSON data to be saved
    your_json_data = json_body
    your_mongodb_uri = "mongodb://bulbaman.me:16017"
    database_name = "newest_db_to_Hack"
    collection_name = "my_collection"
    inserted_id = insert_data_to_mongodb(your_mongodb_uri, database_name, collection_name, your_json_data)
    data_by_id = get_data_by_id_from_mongodb(your_mongodb_uri, database_name, collection_name, inserted_id)
    print(data_by_id)
    return {"differences": differences}


@app.post("/back/show_specific_version", response_model=dict)
async def show_specific_version(
        request_body: dict = Body(...),
        db=Depends(get_database)
):
    _id = request_body.get("_id")

    if not _id or not isinstance(_id, str):
        raise HTTPException(status_code=400, detail="_id should be a valid string in the request body")

    collection = db["my_collection"]

    # Convert _id string to ObjectId
    object_id = ObjectId(_id)

    # Query MongoDB to get the document by _id
    result = collection.find_one({"_id": object_id})

    # If the document is not found, raise an HTTP exception
    if not result:
        raise HTTPException(status_code=404, detail="File not found by _id")

    # Convert ObjectId to str within the response content
    result["_id"] = str(result["_id"])

    # Return a custom JSONResponse with the modified data
    return JSONResponse(content=result)


@app.get("/back/")
def read_root():
    logging.info("Root route accessed")
    return {"Hello": "World"}


@app.get("/back/get_all_versions", response_model=List[dict])
async def get_all_versions(request: Request, db=Depends(get_database)):
    # Get the query parameters
    providerID = request.query_params.get("ProviderID")
    customerID = request.query_params.get("CustomerID")

    # Construct the filter
    filtering = {}
    if providerID:
        filtering["ProviderID"] = providerID
    if customerID:
        filtering["CustomerID"] = customerID

    # Apply the filter and convert the results
    results = [
        {
            "_id": str(result["_id"]),
            "Author": result.get("Author", ""),
            "ProviderID": result.get("ProviderID", ""),
            "CustomerID": result.get("CustomerID", ""),
            "Comment": result.get("Comment", ""),
            "timestamp": result.get("timestamp", "")
        }
        for result in db["my_collection"].find(filtering,
                                               {"_id": 1, "Author": 1, "ProviderID": 1, "CustomerID": 1, "Comment": 1,
                                                "timestamp": 1})
    ]

    # Return the results directly
    return results


@app.get("/back/get_difference", response_model=Dict)
async def get_all_versions(request: Request, db=Depends(get_database)):
    # Get the query parameters
    fileid = request.query_params.get("_id")
    collection = db["my_collection"]

    # Convert _id string to ObjectId
    object_id = ObjectId(fileid)

    # Find the MongoDB file by _id
    current_file = collection.find_one({"_id": object_id})

    # If the file is not found, raise an HTTP exception
    if not current_file:
        raise HTTPException(status_code=404, detail="File not found by _id")

    # Get the timestamp value from the current file
    current_timestamp = current_file.get("timestamp")

    # Find the previous file by timestamp
    previous_file = collection.find_one({"timestamp": {"$lt": current_timestamp}}, sort=[("timestamp", -1)])

    # If there is no previous file, return an empty dictionary
    if not previous_file:
        return {}

    # Compare both files using the compare_json method
    differences = compare_json(current_file, previous_file)

    # Convert ObjectId to str using the custom JSON encoder
    differences_serialized = json.loads(json.dumps(differences, default=str))

    return differences_serialized


@app.get("/back/pdf-file")
async def get_pdf_file(request: Request):
    """
    Return a PDF file stored in the API directory. Via some magic ofc
    """
    etalonid = '6574ddd25d85588d3f5fd5d2'
    fileid = request.query_params.get("_id")
    # Change for better performance if you use windows server X(
    pdf_path = convert_docx_to_pdf(changing_Everything(etalonid, fileid), 'modified_A.pdf')
    return FileResponse(pdf_path, media_type="application/pdf")


@app.get("/back/get_current_version", response_model=Dict)
def get_current_version(db: MongoClient = Depends(get_database)):
    try:
        # Specify the collection name
        collection_name = "my_collection"

        # Query MongoDB to find the document with the newest timestamp and "Podpisant" and "Postavshik" as "True"
        result = db[collection_name].find_one(
            {"Podpisant": "True", "Postavshik": "True"},
            sort=[("timestamp", -1)]
        )

        # Check if any matching documents were found
        if result is None:
            raise HTTPException(status_code=404, detail="No matching documents found")

        # Convert ObjectId to string
        result["_id"] = str(result["_id"])

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # client = MongoClient("mongodb://bulbaman.me:16017")
    #
    # databases_list = client.list_database_names()
    #
    # for db in databases_list:
    #     print(db)
    #
    # client.close()

    uvicorn.run(app, host="127.0.0.1", port=8000)
