from pydantic import BaseModel
from typing import Optional


class PartnerFinancialEstimationUpdate(BaseModel):
    """
    آپدیت اطلاعات مالی تخمینی (غیردقیق)
    """

    first_transaction_date: Optional[str] = None
    first_transaction_amount_estimated: Optional[float] = None

    last_transaction_date: Optional[str] = None
    last_transaction_amount_estimated: Optional[float] = None

    total_transaction_amount_estimated: Optional[float] = None
    transaction_count_estimated: Optional[int] = None

    avg_transaction_value_estimated: Optional[float] = None
    estimation_note: Optional[str] = None
