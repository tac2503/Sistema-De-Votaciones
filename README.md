#  Sistema de Votaciones

Sistema de información que permite gestionar un sistema de votaciones mediante el uso de API RESTful con FastAPI.

##  Características

-  Gestión de votantes
-  Gestión de candidatos
-  Registro de votos
-  Estadísticas de votación
-  Gráficas en tiempo real
-  Base de datos PostgreSQL en la nube (Neon)
-  API RESTful interactiva con Swagger

---

##  Instalación y Ejecución en Local EN WINDOWS

### **Requisitos Previos**
- Python 3.13 o superior
- Git/GitHub
- Conexión a Internet

### **Paso 1: Clonar el Repositorio**
```bash
git clone https://github.com/tac2503/Sistema-De-Votaciones.git
cd Sistema-De-Votaciones
```
### **Abrir en VScode el folder con el proyecto**

### **Paso 2: Crear Entorno Virtual en una nueva terminal dentro del proyecto**
```powershell
python -m venv venv
```

### **Paso 3: Activar Entorno Virtual**

**En terminal de VScode:**
```powershell
.\venv\Scripts\Activate.ps1
```

*Se debe ver `(venv)` al inicio de la línea de comandos*

### **Paso 4: Instalar Dependencias**
```powershell
pip install -r requirements.txt
```

### **Paso 5: Crear archivo `.env`**

En la raíz del proyecto crea un archivo llamado `.env`:
Donde va lo siguiente, que hace referencia a la base de datos utilizada.

```
DATABASE_URL=postgresql://usuario:contraseña@ep-xxxxx.neon.tech/nombre_base_datos 
```

#### **Cómo obtener las credenciales en Neon:**

1. Ve a https://neon.tech
2. Inicia sesión o crea cuenta
3. Crea un nuevo proyecto
4. Selecciona la opcion `Connect`
5. En la seccion "Connection String" selecciona Sqlalchemy
![alt text](image-1.png)
6. Selecciona el metodo .env y copia lo que aparece.
5. Pégala en el `.env` como `DATABASE_URL`  

# **IMPORTANTE**

Para el correcto funcionamiento, es importante borrar la comilla inicial y final con la que se pega la DATABASE_URL en el .env

**Ejemplo:**
```
DATABASE_URL=postgresql://neon_user:abc123@ep-morning-moon-12345.us-east-1.neon.tech/voting_db
```

### **Paso 6: Ejecutar la Aplicación**
```powershell
python -m app.main
```

### **Paso 7: Acceder a la API**

Cuando inicie, verás:
```
============================================================
 SISTEMA DE VOTACIONES API
============================================================
 API:           http://127.0.0.1:8000
Documentación: http://127.0.0.1:8000/docs
============================================================
```

- **Swagger UI:** http://127.0.0.1:8000/docs 
- **API Base:** http://127.0.0.1:8000/

---

##  Endpoints Disponibles

### **Votantes**
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/voters/` | Crear votante |
| DELETE | `/voters/{voter_id}` | Eliminar votante |

### **Candidatos**
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/candidates/` | Crear candidato |
| GET | `/candidates/` | Listar candidatos |

### **Votos**
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/votes/` | Registrar voto |
| GET | `/votes/` | Listar votos con nombres |
| GET | `/votes/statistics` | Ver estadísticas y gráficas |

---

## Ejemplos de vista base de datos en NEON

![alt text](image.png)

![alt text](image-2.png)

## Ejemplo de la gráfica generada

![alt text](image-3.png)

##  Estructura del Proyecto

```
Sistema-De-Votaciones/
├── app/
│   ├── models.py          # Modelos de BD (Voter, Candidate, Vote)
│   ├── schemas.py         # Esquemas Pydantic de validación
│   ├── crud.py            # Operaciones de BD
│   ├── database.py        # Conexión a PostgreSQL
│   ├── main.py            # Aplicación FastAPI
│   └── routers/
│       ├── voters.py      # Endpoints de votantes
│       ├── candidates.py  # Endpoints de candidatos
│       └── votes.py       # Endpoints de votos
├── requirements.txt       # Dependencias
├── .env                   # Variables de entorno (no incluida en git)
├── .gitignore            # Archivos ignorados por git
└── README.md             # Este archivo
```

---



##  Ejemplo de Uso

### **1. Crear Votante**
```json
POST http://127.0.0.1:8000/voters/
{
  "name": "Juan Pérez",
  "email": "juan@example.com"
}
```

### **2. Crear Candidato**
```json
POST http://127.0.0.1:8000/candidates/
{
  "name": "Carlos López",
  "party": "Partido A"
}
```

### **3. Registrar Voto**
```json
POST http://127.0.0.1:8000/votes/
{
  "voter_id": 1,
  "candidate_id": 1
}
```

### **4. Ver Estadísticas**
```
GET http://127.0.0.1:8000/votes/statistics
```

Respuesta:
```json
{
  "total_voters_voted": 5,
  "total_votes": 5,
  "candidates_statistics": [
    {
      "candidate_id": 1,
      "candidate_name": "Carlos López",
      "total_votes": 3,
      "percentage": 60.0
    },
    {
      "candidate_id": 2,
      "candidate_name": "Maria García",
      "total_votes": 2,
      "percentage": 40.0
    }
  ]
}
```

---

##  Dependencias Principales

- **FastAPI** - Framework web
- **SQLAlchemy** - ORM para BD
- **Pydantic** - Validación de datos
- **psycopg2** - Driver PostgreSQL
- **Pandas** - Análisis de datos
- **Matplotlib** - Gráficas
- **Uvicorn** - Servidor ASGI

---



---

##  Autor

Tomas Álvarez Castillo - 2026
