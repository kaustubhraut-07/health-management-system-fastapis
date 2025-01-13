

from fastapi import APIRouter, Depends, HTTPException

from models.user import User

router = APIRouter()


@router.get("/")
async def get_all_patients():
    try:
        users_collection = MongoDB.database["users"]
        users = await users_collection.find().to_list(100)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

