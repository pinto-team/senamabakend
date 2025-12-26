from pydantic import BaseModel
from typing import Optional

from app.models.partner import AcquisitionSource


class PartnerAcquisitionUpdate(BaseModel):
    """
    بروزرسانی منبع آشنایی مخاطب با مجموعه
    """

    source: Optional[AcquisitionSource] = None
    source_note: Optional[str] = None
