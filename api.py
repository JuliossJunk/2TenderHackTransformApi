from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from typing import Dict
import json
import uvicorn

app = FastAPI()


def compare_json(json1: Dict, json2: Dict) -> Dict:
    """
    Compare two JSON objects and return the fields that are different.
    """
    differences = {}
    for key in json1.keys():
        if key in json2:
            if json1[key] != json2[key]:
                differences[key] = {"old": json1[key], "new": json2[key]}
        else:
            differences[key] = {"old": json1[key], "new": None}

    for key in json2.keys():
        if key not in json1:
            differences[key] = {"old": None, "new": json2[key]}

    return differences


@app.post("/compare-json")
async def compare_json_files(json_body: Dict):
    """
    Compare the JSON in the request body with the JSON from a file in the API directory.
    """
    # Load the JSON from the file in the API directory
    with open("blocks.json", "r", encoding='utf-8') as file:
        json_file = json.load(file)

    # Compare the JSON objects
    differences = compare_json(json_body, json_file)

    return {"differences": differences}


@app.get("/pdf-file")
async def get_pdf_file():
    """
    Return a PDF file stored in the API directory.
    """
    pdf_path = "Договор на поставку товара № 129-23.pdf"
    return FileResponse(pdf_path, media_type="application/pdf")


if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000)
