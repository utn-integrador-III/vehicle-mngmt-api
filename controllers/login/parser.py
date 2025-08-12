from pydantic import BaseModel, EmailStr, Field

class RegisterSchema(BaseModel):
    cedula: str = Field(..., description="Cédula del usuario")
    nombre: str = Field(..., description="Nombre")
    apellidos: str = Field(..., description="Apellidos")
    correo: EmailStr = Field(..., description="Correo electrónico válido")
    contraseña: str = Field(..., description="Contraseña")
    rol: str = Field(..., description="Rol del usuario, admin o usuario")

class LoginSchema(BaseModel):
    cedula: str = Field(..., description="Cédula del usuario")
    contraseña: str = Field(..., description="Contraseña")
