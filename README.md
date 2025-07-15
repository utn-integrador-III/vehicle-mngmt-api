# vehicle-mngmt-api

### Create virtual environment

python -m venv venv

#### Or

py -m venv venv

### Activate virtual environment

.\venv\Scripts\activate

### Update pip

python -m pip install --upgrade pip

#### Or

py -m pip install --upgrade pip

### Install dependencies

pip install -r requirements.txt

After that, create the .env file based on the .env.example

### Inicialize the app

uvicorn app:app --reload

### En caso de agregar una nueva libreria, ejecutar el siguiente comando para actualizar el requirements.txt

pip freeze > .\requirements.txt

###

### TESTING

## Try testing to vehicle

## Run the next command

pytest

###

### db_testing

# Ejecutar el siguiente comando desde la raíz del proyecto para comprobar la conexión con la base de datos

python -m testing.db_testing.db_connection_test
