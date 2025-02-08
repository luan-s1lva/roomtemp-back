from pydantic import BaseModel,Field

class Sensor(BaseModel):
    idSala: str = Field(...)
    temperaturaCelsius: str = Field(...)