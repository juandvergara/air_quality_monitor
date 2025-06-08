# Air Quality Monitor for Kiwibot

Proyecto desarrollado como parte de la prueba técnica para el rol de **Service Desk Engineer** en Kiwibot.

El objetivo es crear un sistema automatizado para consultar datos de calidad del aire mediante la API de PurpleAir, almacenarlos en BigQuery y visualizarlos en un dashboard.

---

## 📋 Funcionalidades

- Cliente en Python para interactuar con la API de PurpleAir.
- CLI tool para realizar fetch, upload y export de datos.
- Contenedor Docker para ejecución portable.
- Almacenamiento en BigQuery.
- Dashboard en Looker Studio para visualización.

---

## 🚀 Instalación

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/juandvergara/air_quality_monitor.git
cd air_quality_monitor

---

###  2️⃣ Variables de entorno

Crea un archivo .env con el siguiente contenido:

PURPLEAIR_API_KEY=your_api_key_here
GCP_PROJECT_ID=your_gcp_project_id_here
BQ_DATASET_ID=your_bigquery_dataset_id_here
BQ_TABLE_ID=your_bigquery_table_id_here

---

### 3️⃣ Build y ejecución del contenedor
```bash
./setup.sh

🖥️ CLI Tool
El CLI está implementado en cli.py.
Se puede ejecutar desde el contenedor o localmente:

Comandos disponibles:
fetch
Obtiene datos de uno o varios sensores de PurpleAir.

bash

python3 cli.py fetch --sensor_id 12345
# o
python3 cli.py fetch --bounds '{"nw_lat":4.8,"nw_lng":-74.2,"se_lat":4.5,"se_lng":-74.0}'
upload
Sube datos previamente obtenidos a BigQuery.

bash

python3 cli.py upload --input_file data/sensor_data.json
export
Exporta datos desde BigQuery a CSV.

bash

python3 cli.py export --output_file export.csv --pm25_threshold 35
