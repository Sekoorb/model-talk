from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from starlette.responses import JSONResponse
from ..crud import save_model_schema, get_model_schemas_for_user
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/model-upload/")
async def upload_model_schema(file: UploadFile = File(...), user_id: str = Depends(get_current_user)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    # Assuming the content is a CSV string, you might want to validate its structure here
    
    success = await save_model_schema(user_id, file.filename, content)
    if not success:
        raise HTTPException(status_code=500, detail="Could not save the model schema")

    return JSONResponse(status_code=200, content={"message": "Model schema uploaded successfully"})

@router.get("/model-schemas/")
async def list_model_schemas(user_id: str = Depends(get_current_user)):
    schemas = await get_model_schemas_for_user(user_id)
    if schemas is None:
        raise HTTPException(status_code=404, detail="No model schemas found")
    return schemas

# You might need to implement save_model_schema and get_model_schemas_for_user in your crud.py
