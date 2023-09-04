from fastapi import APIRouter, HTTPException, status
from api.models.models import input_tag_identification,output_tag_identification
from main import tag_identification
import logging
from datetime import datetime



logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.ERROR)
logger = logging.getLogger()
router = APIRouter()

router = APIRouter()

@router.post('/tag-identification',response_model=output_tag_identification)
def tag_find(input:input_tag_identification):
    try:
        start_time = datetime.now()
        logger.info("-----------------START-------------------------------")
        logger.info(f"Start time is {start_time}")


        result = tag_identification(input.websites)

        end_time = datetime.now()
        logger.info('Response time  is: {}'.format(end_time - start_time))
        logger.info("-----------------END-------------------------------")
        return output_tag_identification(output=result)

    except Exception as e:
        end_time = datetime.now()
        logger.info('Response time  is: {}'.format(end_time - start_time))
        logger.error(str(e), exc_info=True)
        logger.info("-----------------END-------------------------------")
        raise HTTPException(detail=str(e), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

