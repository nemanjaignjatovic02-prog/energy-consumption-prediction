from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Measurement(BaseModel):
    meter_id: str
    timestamp: datetime
    consumption_kwh: float
    temperature: Optional[float] = None
    humidity: Optional[float] = None