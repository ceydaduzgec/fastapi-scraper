from fastapi import APIRouter

router = APIRouter()


@router.post('/download')
async def start_downloading_images():
    pass


@router.get('/download/{download_id}/status')
async def get_download_status():
    pass


@router.get('/download/{download_id}')
async def download_images():
    pass
