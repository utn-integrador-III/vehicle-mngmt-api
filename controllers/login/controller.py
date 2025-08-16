from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from models.login.model import UserModel
from utils.server_response import ServerResponse, StatusCode
from utils.message_codes import SUCCESS_MSG, UNAUTHORIZED, CONFLICT_MSG
from controllers.login.parser import LoginSchema, RegisterSchema, UpdateUserSchema

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
    existing_user = UserModel.get_by_cedula(data.cedula)
    if existing_user:
        return ServerResponse.build(
            message="La cédula ya está registrada",
            message_code=CONFLICT_MSG,
            status=StatusCode.CONFLICT,
            code="CONFLICT"
        )

    user_data = {
        "cedula": data.cedula,
        "nombre": data.nombre,
        "apellidos": data.apellidos,
        "correo": data.correo,
        "contraseña": data.contraseña,
        "rol": data.rol
    }
    inserted_id = UserModel.create(user_data)

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


@router.get("/get/{user_id}")
async def get_user_by_id(user_id: str):
    user = UserModel.get_by_id(user_id)
    if not user:
        return ServerResponse.build(
            message="Usuario no encontrado",
            message_code=UNAUTHORIZED,
            status=StatusCode.NOT_FOUND,
            code="NOT_FOUND"
        )

    user["_id"] = str(user["_id"])
    return ServerResponse.build(
        data=user,
        message="Usuario encontrado",
        message_code=SUCCESS_MSG,
        status=StatusCode.OK,
        code="SUCCESS"
    )


@router.get("/all")
async def get_all_users():
    users = UserModel.get_all()
    if not users:
        return ServerResponse.build(
            message="No hay usuarios registrados",
            message_code=UNAUTHORIZED,
            status=StatusCode.NOT_FOUND,
            code="NOT_FOUND"
        )

    for user in users:
        user["_id"] = str(user["_id"])

    return ServerResponse.build(
        data=users,
        message="Lista de usuarios obtenida exitosamente",
        message_code=SUCCESS_MSG,
        status=StatusCode.OK,
        code="SUCCESS"
    )


@router.put("/update/{user_id}")
async def update_user(user_id: str, data: UpdateUserSchema):
    existing_user = UserModel.get_by_id(user_id)
    if not existing_user:
        return ServerResponse.build(
            message="Usuario no encontrado",
            message_code=UNAUTHORIZED,
            status=StatusCode.NOT_FOUND,
            code="NOT_FOUND"
        )

    # Combinar datos enviados con los existentes
    update_data = {}
    for field, value in data.dict().items():
        if value is not None:
            update_data[field] = value
        else:
            update_data[field] = existing_user.get(field)

    updated = UserModel.update_by_id(user_id, update_data)
    if not updated:
        return ServerResponse.build(
            message="No se pudo actualizar el usuario",
            message_code=UNAUTHORIZED,
            status=StatusCode.INTERNAL_SERVER_ERROR,
            code="ERROR"
        )

    updated_user = UserModel.get_by_id(user_id)
    updated_user["_id"] = str(updated_user["_id"])

    return ServerResponse.build(
        data=updated_user,
        message="Usuario actualizado exitosamente",
        message_code=SUCCESS_MSG,
        status=StatusCode.OK,
        code="SUCCESS"
    )


@router.delete("/delete/{user_id}")
async def delete_user(user_id: str):
    existing_user = UserModel.get_by_id(user_id)
    if not existing_user:
        return ServerResponse.build(
            message="Usuario no encontrado",
            message_code=UNAUTHORIZED,
            status=StatusCode.NOT_FOUND,
            code="NOT_FOUND"
        )

    deleted = UserModel.delete_by_id(user_id)
    if not deleted:
        return ServerResponse.build(
            message="No se pudo eliminar el usuario",
            message_code=UNAUTHORIZED,
            status=StatusCode.INTERNAL_SERVER_ERROR,
            code="ERROR"
        )

    return ServerResponse.build(
        message="Usuario eliminado exitosamente",
        message_code=SUCCESS_MSG,
        status=StatusCode.OK,
        code="SUCCESS"
    )
