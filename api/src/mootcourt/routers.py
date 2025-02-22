from fastapi import APIRouter, HTTPException, status
from decouple import config
from getstream import Stream
from getstream.models import UserRequest
from src.mootcourt.schemas import StreamUserRequest, StreamUserResponse

router = APIRouter(prefix="/stream", tags=["Stream Token"])


@router.post(
    "/token", status_code=status.HTTP_201_CREATED, response_model=StreamUserResponse
)
async def stream_token(request: StreamUserRequest):
    try:
        # validate request
        if not request:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Request"
            )

        # get stream  api credentials
        STREAM_API_KEY = config("STREAM_API_KEY", cast=str)
        STREAM_API_SECRET = config("STREAM_API_SECRET", cast=str)

        if not STREAM_API_KEY or not STREAM_API_SECRET:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Stream API configuration is missing",
            )

        # initilize stream client
        client = Stream(
            api_key=STREAM_API_KEY, api_secret=STREAM_API_SECRET, timeout=3.0
        )

        # prepare custom data
        custom_data = {"email": request.email}

        # create or update user in stream
        client.upsert_users(
            UserRequest(
                id=request.userId,
                name=request.name,
                image=request.image,
                role="user",
                custom=custom_data,
            ),
        )

        token = client.create_token(user_id=request.userId, expiration=3600)

        return {"token": token}
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate token {e}",
        )
