from pydantic import BaseModel
from typing import Optional, List

from app.models.partner import BusinessType, ContactNumber, GeoLocation


class PartnerQuickEntry(BaseModel):
    """
    ورودی فرم ورود سریع
    فقط brand_name اجباری است
    """

    brand_name: str  # ✅ تنها فیلد اجباری

    manager_full_name: Optional[str] = None
    business_type: Optional[BusinessType] = None

    contact_numbers: Optional[List[ContactNumber]] = None

    province: Optional[str] = None
    city: Optional[str] = None
    location: Optional[GeoLocation] = None

    notes: Optional[str] = None
