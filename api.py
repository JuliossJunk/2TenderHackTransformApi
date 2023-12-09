from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Body
from fastapi.responses import FileResponse, JSONResponse
from typing import Dict, List
import json
from bson import ObjectId
import uvicorn
import json
from datetime import datetime
from pymongo import MongoClient



app = FastAPI()
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

@app.get("/back/get_all_versions", response_model=List[dict])
async def get_all_versions(db=Depends(get_database)):
    collection = db["my_collection"]

    # Correct field names and ObjectId conversion
    results = [
        {
            "_id": str(result["_id"]),
            "Author": result.get("Author", ""),
            "Comment": result.get("Comment", ""),
            "timestamp": result.get("timestamp", "")
        }
        for result in collection.find({}, {"_id": 1, "Author": 1, "Comment": 1, "timestamp": 1})
    ]

    # Return the results directly
    return results
@app.get("/back/pdf-file")
async def get_pdf_file():
    """
    Return a PDF file stored in the API directory.
    """
    pdf_path = "A.pdf"
    return FileResponse(pdf_path, media_type="application/pdf")


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
