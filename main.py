from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io

app = FastAPI()

@app.post("/upload-excel/")
async def upload_excel(file: UploadFile = File(...)):
    # Read the uploaded Excel file into a Pandas DataFrame
    contents = await file.read()
    df = pd.read_excel(io.BytesIO(contents))

    # Extract necessary columns
    required_columns = ["Application ID", "Name", "Mobile", "Status"]
    if not all(col in df.columns for col in required_columns):
        return {"error": "Invalid file format. Required columns missing."}

    # Convert DataFrame to list of dictionaries (JSON)
    data = df[required_columns].to_dict(orient="records")

    return {"data": data}