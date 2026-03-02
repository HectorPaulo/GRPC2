# gRPC + PostgreSQL + FastAPI + React + Tkinter + Swing

Proyecto con backend en Python (FastAPI + gRPC) y clientes React (Web), Tkinter (Python) y Swing (Java) conectados a una base de datos PostgreSQL local.

## Estructura
- `backend/`: FastAPI + gRPC + PostgreSQL
- `clients/react-frontend/`: Cliente React (Web) - Interfaz web moderna con diseño limpio
- `clients/tkinter/`: Cliente Python Tkinter (gRPC)
- `clients/java_swing/`: Cliente Java Swing (gRPC)
- `backend/proto/vehicle.proto`: contrato gRPC

## Paso a paso (orden recomendado)
1. Inicia PostgreSQL local.
2. Crea la base y confirma credenciales.
3. Instala dependencias del backend.
4. Genera stubs gRPC.
5. Ejecuta el backend (gRPC + FastAPI).
6. Abre el cliente que prefieras:
   - **React**: Interfaz web moderna (http://localhost:5173)
   - **Tkinter**: Cliente Python de escritorio (gRPC)
   - **Swing**: Cliente Java de escritorio (gRPC)

## 1) Configurar PostgreSQL (local)
Base y credenciales usadas por defecto:
- DB: `SistemasDistribuidos`
- User: `postgres`
- Password: `1253`

Si necesitas cambiar algo, usa variables de entorno:
- `DB_HOST` (default: `localhost`)
- `DB_PORT` (default: `5432`)
- `DB_NAME` (default: `SistemasDistribuidos`)
- `DB_USER` (default: `postgres`)
- `DB_PASSWORD` (default: `1253`)

Ejemplo de creación rápida:
```bash
createdb SistemasDistribuidos
```
Si no tienes `createdb`, también puedes usar:
```bash
psql -U postgres -c "CREATE DATABASE \"SistemasDistribuidos\";"
```

Para crear la tabla manualmente (si el backend no la crea):
```bash
psql -U postgres -d "SistemasDistribuidos" -c "
CREATE TABLE IF NOT EXISTS vehicles (
    matricula VARCHAR(20) PRIMARY KEY, 
    vin VARCHAR(40) UNIQUE NOT NULL, 
    modelo VARCHAR(60) NOT NULL, 
    marca VARCHAR(60) NOT NULL, 
    tipo VARCHAR(60) NOT NULL
);
"
```

## 2) Backend (FastAPI + gRPC)
```bash
cd gRPC/1_coneccion_BD/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3) Compilar stubs gRPC
```
cd gRPC/1_coneccion_BD/backend/proto

python -m grpc_tools.protoc \
    -I . \
    --python_out ../app \
    --grpc_python_out ../app \
    vehicle.proto

cd gRPC/1_coneccion_BD/clients/java_swing/src/main/proto

python -m grpc_tools.protoc \
    -I . \
    --python_out ../../../../tkinter \
    --grpc_python_out ../../../../tkinter \
    vehicle.proto

```

## 4) Ejecutar backend (gRPC + FastAPI)
Esto levanta:
- gRPC en `localhost:50051`
- FastAPI en `http://localhost:8000`
```bash
cd gRPC/1_coneccion_BD/backend
source .venv/bin/activate
python -m app.main
```

## 5) Cliente React (Frontend Web)
El cliente React consume los endpoints REST de FastAPI.
```bash
cd clients/react-frontend
npm install   # Solo la primera vez
npm run dev
```
Abre el navegador en: **http://localhost:5173**

**Características:**
- ✅ Diseño limpio y profesional (sin gradientes complejos ni colores morado/rosa)
- ✅ Paleta de colores: Azul (#1976d2) y Gris (#546e7a)
- ✅ CRUD completo de vehículos
- ✅ Responsive design (móvil y escritorio)
- ✅ Manejo de errores con alertas visuales
- ✅ Estados de carga y feedback al usuario

Ver más detalles en: `clients/react-frontend/INSTRUCCIONES.md`

## 6) Cliente Tkinter (Desktop Python)
Nota: Activar entorno desde backend
```bash
cd gRPC/1_coneccion_BD/clients/tkinter
python3 tkinter_client.py
```

## 7) Cliente Swing (Desktop Java)
```bash
cd gRPC/1_coneccion_BD/clients/java_swing
mvn -q -DskipTests compile
mvn -q -DskipTests exec:java -Dexec.mainClass=com.example.vehicles.VehicleSwingApp
```

## Endpoints FastAPI (opcional)
- `POST /vehicles`
- `GET /vehicles/{matricula}`
- `GET /vehicles`
- `DELETE /vehicles/{matricula}`

## gRPC
Servicio: `VehicleService` con `CreateVehicle`, `GetVehicle`, `ListVehicles`, `DeleteVehicle`.
