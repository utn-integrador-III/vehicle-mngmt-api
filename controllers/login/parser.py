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

class UpdateUserSchema(BaseModel):
    cedula: str = Field(..., description="Cédula del usuario")
    nombre: str | None = Field(None, description="Nombre")
    apellidos: str | None = Field(None, description="Apellidos")
    correo: EmailStr | None = Field(None, description="Correo electrónico válido")
    contraseña: str | None = Field(None, description="Contraseña")
    rol: str | None = Field(None, description="Rol del usuario, admin o usuario")
