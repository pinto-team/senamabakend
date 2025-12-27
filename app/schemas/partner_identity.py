from pydantic import BaseModel
from typing import Optional, List

from app.models.partner import (
    BusinessType,
    ContactNumber,
    SocialLink,
    GeoLocation,
)


class PartnerIdentityUpdate(BaseModel):
    """
    آپدیت اطلاعات هویتی پایه
    فقط brand_name اجباری است
    """

    brand_name: str  # ✅ تنها فیلد اجباری

    manager_full_name: Optional[str] = None
    business_type: Optional[BusinessType] = None

    contact_numbers: Optional[List[ContactNumber]] = None
    social_links: Optional[List[SocialLink]] = None

    province: Optional[str] = None
    city: Optional[str] = None
    map_link: Optional[str] = None
    full_address: Optional[str] = None

    location: Optional[GeoLocation] = None
