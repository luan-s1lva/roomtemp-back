from pydantic import BaseModel,Field

class Room(BaseModel):
    idSala: int = Field(..., alias="_id")
    temperaturaCelsius: str = Field(default="30")
    isLightOn: bool = Field(default=False)
    isACOn: bool = Field(default=False)