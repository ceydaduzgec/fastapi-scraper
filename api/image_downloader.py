from fastapi import APIRouter

router = APIRouter()


@router.post('/downloads')
async def start_downloading_images():
    pass


@router.get('/downloads/{download_id}/status')
async def get_download_status():
    pass


@router.get('/downloads/{download_id}')
async def download_images():
    pass
