from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from models.login.model import UserModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import SUCCESS_MSG, UNAUTHORIZED, CONFLICT_MSG
from controllers.login.parser import LoginSchema, RegisterSchema

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(data: LoginSchema):
    user = UserModel.login(data.cedula, data.contraseña)
    if not user:
        return ServerResponse.build(
            message="Credenciales inválidas",
            message_code=UNAUTHORIZED,
            status=StatusCode.UNPROCESSABLE_ENTITY,
            code="UNAUTHORIZED"
        )
    rol = user.get("rol")

    user_response = {
        "cedula": user.get("cedula"),
        "nombre": user.get("nombre"),
        "apellidos": user.get("apellidos"),
        "correo": user.get("correo"),
        "rol": rol,
    }
    return ServerResponse.build(
        data=user_response,
        message="Login exitoso",
        message_code=SUCCESS_MSG,
        status=StatusCode.OK,
        code="SUCCESS"
    )


@router.post("/register")
async def register(data: RegisterSchema):
    # Verificar si la cédula ya existe
    existing_user = UserModel.get_by_cedula(data.cedula)
    if existing_user:
        return ServerResponse.build(
            message="La cédula ya está registrada",
            message_code=CONFLICT_MSG,
            status=StatusCode.CONFLICT,
            code="CONFLICT"
        )

    # Crear usuario
    user_data = {
        "cedula": data.cedula,
        "nombre": data.nombre,
        "apellidos": data.apellidos,
        "correo": data.correo,
        "contraseña": data.contraseña,  # idealmente encriptar aquí
        "rol": data.rol
    }
    inserted_id = UserModel.create(user_data)

    # Preparar respuesta
    user_data["id"] = str(inserted_id)
    if "_id" in user_data:
        del user_data["_id"]

    return ServerResponse.build(
        data=user_data,
        message="Usuario registrado exitosamente",
        message_code=SUCCESS_MSG,
        status=StatusCode.CREATED,
        code="SUCCESS"
    )
