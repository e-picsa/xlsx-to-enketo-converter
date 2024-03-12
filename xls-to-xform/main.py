from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.responses import JSONResponse
from pathlib import Path
from typing import List
import subprocess
import tempfile
import shutil
import os

app = FastAPI()


@app.get("/")
def read_health():
    return {"message": "Welcome to the python xlsx to xml convertor server ", "status": "OK"}


@app.get("/api/health")
def read_health():
    return {"status": "OK"}


def convert_xls_to_xml_bg(file: UploadFile, temp_dir: str):
    try:
        temp_file_path = Path(temp_dir) / file.filename

        # Save the uploaded file to the temporary directory
        with temp_file_path.open("wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)

        # Call xls2xform module from the command line process
        # NOTE - form validation requires java 8+
        output_path = Path(temp_dir) / "output.xml"
        process = subprocess.Popen(
            ["xls2xform", "--skip_validate", str(temp_file_path), str(output_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = process.communicate()

        # Check if the conversion was successful
        if process.returncode != 0:
            raise HTTPException(
                status_code=500, detail=f"Conversion failed for file {file.filename}: {stderr}")

        # Read the content of the created XML file
        with output_path.open("r", encoding="utf-8") as xml_file:
            xml_content = xml_file.read()

        # Return the content of the XML file
        return xml_content

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/convert_xls_to_xml")
async def convert_xls_to_xml(files: List[UploadFile] = File(...)):
    try:
        xml_contents = ""

        for file in files:

            temp_dir = tempfile.mkdtemp()

            xml_content = convert_xls_to_xml_bg(file, temp_dir)

            xml_contents += xml_content

            # Clean up the temporary directory
            shutil.rmtree(temp_dir)

        # Return the paths to the created XML files
        return JSONResponse(content={
            "message": "Conversion completed for all files",
            "xml_file": xml_contents
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def run_app():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 5262)))


if __name__ == "__main__":
    run_app()
