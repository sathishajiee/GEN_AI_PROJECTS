from pydantic import BaseModel, Field


class User(BaseModel):
  id: str
  name: str = Field(description="The user's full name", examples=['Alice', 'Ali'])
  age: int

user = User(
  id='1',
  name='Alice',
  age='25'
)

print(user)