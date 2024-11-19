# 🎥 Youreview API

Esta aplicación Flask proporciona una API para extraer contenido de videos de YouTube, incluyendo la extracción de audio, transcripción de texto y generación de un resumen de los puntos principales. La aplicación utiliza la biblioteca `yt_dlp` para descargar audio y `langchain` para procesamiento de lenguaje natural.

## ⚙️ Tecnologías Utilizadas

- **🐍 Python 3.11**: Lenguaje principal.
- **🌐 Flask**: Framework para desarrollar la API.
- **📥 yt_dlp**: Descarga de videos y audio desde YouTube.
- **🧠 Langchain**: Procesamiento de lenguaje natural.
- **🐳 Docker**: Contenedores para fácil implementación.
- **🎵 FFmpeg**: Manipulación de archivos multimedia.

## 🚀 Instalación

### 1. 🛠️ Clonar el repositorio
    ```bash
    git clone https://github.com/ilmovilDev/Youreview-backend-python-3.11.git
    ```

### 2. 📂 Acceder al directorio del proyecto
    ```bash
    cd my_app
    ```

### 3. 🔑 Configurar variables de entorno
    - Solicita tu `api_key` en [Groq](https://groq.com/).
    - Copia el archivo `.env.example` y renómbralo como `.env`.
    - Abre el archivo `.env` y actualiza la variable `GROQ_API_KEY` con tu clave obtenida.


## 🐳 Ejecución con Docker

Para ejecutar la aplicación usando Docker, sigue los pasos:

### 1. 🏗️ Construir la imagen Docker
    ```bash
    docker build -t my_app .
    ```

### 2. ▶️ Ejecutar el contenedor
    ```bash
    docker run -p 5000:5000 my_app
    ```

Una vez iniciado el contenedor, la API estará disponible en `http://127.0.0.1:5000`.

## 📡 Endpoints

### 1. 📝 Generar Resumen
- **URL**: `/generate_video_summary`
- **Método**: `GET`
- **Descripción**: Genera un resumen del contenido del video.
- **Parámetros**: 
  - `url` (string, requerido): URL del video de YouTube.
- **🌐 Ejemplo de solicitud en Postman:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```
- **✅ Respuestas:**
    - **Código 200**: JSON con el título del video, el canal y el resumen.
    ```json
    {
        "audio_download_link": "download_audio?url=https://www.youtube.com/watch?v=b5Ho2_Si6hY",
        "channel": "GitHub",
        "summary": "<div class='p-4'>Summary</div>",
        "thumbnail": "https://i.ytimg.com/vi_webp/b5Ho2_Si6hY/maxresdefault.webp",
        "title": "Octoverse 2024: The rise of Python and AI",
        "transcription": "remember when people said that ai would replace "
    }
    ```
    - **Código 402** | **Código 404** | **Código 500**: 
    ```json
    {
        "context": "Información adicional sobre el error (opcional)",
        "message": "Mensaje de error detallado",
        "success": false
    }
    ```


### 2. 🎧 Descargar Audio
- **URL**: `/download_audio?url=`
- **Método**: `GET`
- **Descripción**: Extrae el audio de un video de YouTube y lo descarga en formato MP3.
- **Parámetros**: 
  - `video_url` (string, requerido): URL del video de YouTube.
- **Ejemplo de solicitud en Postman**
```http
GET /download_audio?url=https://www.youtube.com/watch?v=VIDEO_ID
```
- **✅ Respuestas:**
    - **Código 200**: Devuelve el archivo de audio descargado
    - **Código 402** | **Código 404** | **Código 500**: 
    ```json
    {
        "context": "Información adicional sobre el error (opcional)",
        "message": "Mensaje de error detallado",
        "success": false
    }
    ```

### 🖼️ Ejemplos Visuales

![youreview - backend - postman](https://res.cloudinary.com/dihhlrchn/image/upload/v1732007852/Youreview/Backend/hpnsrwzkytqnfcsjw6ne.png)

![youreview - backend - postman](https://res.cloudinary.com/dihhlrchn/image/upload/v1732007851/Youreview/Backend/cd8yrv3hkkz3vmbam31h.png)

![youreview - backend - postman](https://res.cloudinary.com/dihhlrchn/image/upload/v1732007851/Youreview/Backend/jq1je7afqc0ppweiu9es.png)

## 👨‍💻 Datos del Autor

- **Nombre**: Luis Carrasco
- **GitHub**: [github.com/ilmovilDev](https://github.com/ilmovilDev)

## 📜 Licencia

Este proyecto está bajo la licencia MIT.
