from ninja import Schema

class ErrorSchema(Schema):
  success:bool
  status_code:int
  message:str