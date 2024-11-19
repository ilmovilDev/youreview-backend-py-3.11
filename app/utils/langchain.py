import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

class LangchainError(Exception):
    pass

class Langchain:
    def __init__(self):
        self.api_key = self._load_api_key()
        self.model = self._initialize_model()

    @staticmethod
    def _load_api_key() -> str:
        """Load the GROQ API key from environment variables."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise LangchainError("GROQ API key is not configured.")
        return api_key

    def _initialize_model(self) -> ChatGroq:
        """Initialize the ChatGroq model with the loaded API key."""
        try:
            return ChatGroq(model='llama-3.1-70b-versatile', api_key=self.api_key)
        except Exception as e:
            raise LangchainError(f"Error initializing ChatGroq model: {str(e)}") from e

    def generate_summary(self, prompt_template: ChatPromptTemplate) -> str:
        """
        Generate a summary based on the input prompt template.
        """
        try:
            chain = prompt_template | self.model
            response = chain.invoke({})
            summary = response.content if response else None
            if not summary:
                raise LangchainError("Failed to generate a summary for the transcription.")
            return summary
        except Exception as e:
            raise LangchainError(f"Error generating summary: {str(e)}") from e

    @staticmethod
    def generate_prompt_template_video_analysis(text_to_be_analyzed: str) -> ChatPromptTemplate:
        """
        Generate a prompt template to analyze a video and return a summary in formatted HTML with Tailwind CSS styles.
        The prompt dynamically adapts to different types of video content such as music, news, tutorials, and more.
        """
        prompt_text = (
            "Eres un asistente experto en análisis, resumen y diseño de contenido. "
            "Tu tarea es analizar el texto transcrito de un video de YouTube, identificar el tipo de contenido, y "
            "proporcionar un resumen breve y claro en español. El resultado debe estar formateado en HTML estilizado con "
            "Tailwind CSS para garantizar una presentación visual atractiva y responsiva.\n\n"
            "Tipos de contenido y directrices específicas:\n"
            "1. **Musicales**: Describe brevemente el tema o género del video, menciona el artista y destaca las emociones o mensajes principales.\n"
            "2. **Noticias**: Enfócate en los titulares, eventos clave y su impacto. Utiliza listas si hay múltiples eventos relevantes.\n"
            "3. **Tutoriales**: Resume los pasos principales, los objetivos del tutorial, y cualquier consejo clave.\n"
            "4. **Tecnología**: Destaca los productos, innovaciones o conceptos explicados. Asegúrate de incluir ideas clave y tendencias.\n"
            "5. **Educativos**: Resalta los conceptos principales, aprendizajes y su utilidad práctica.\n"
            "6. **Entretenimiento**: Enfócate en el tema central, personajes o eventos destacados.\n"
            "7. **Salud/Ciencia**: Proporciona un resumen estructurado con puntos clave, hallazgos o consejos prácticos.\n\n"
            "Formato del HTML:\n"
            "- Usa `<div>` como contenedor principal con clases como `p-4`.\n"
            "- Títulos principales en `<h2>` con clases como `text-xl font-bold mb-2 text-gray-800`.\n"
            "- Los párrafos deben usar `<p>` con clases como `text-gray-700 leading-relaxed`.\n"
            "- Usa listas `<ul>` y `<li>` para enumerar puntos clave.\n"
            "- El diseño debe ser responsivo y semántico.\n\n"
            "Ejemplo de salida formateada:\n"
            "<div class='p-4'>\n"
            "  <h2 class='text-xl font-bold mb-2 text-gray-800'>Título del Resumen</h2>\n"
            "  <p class='text-gray-700 leading-relaxed'>Resumen adaptado al tipo de contenido.</p>\n"
            "  <ul class='list-disc pl-5 text-gray-700'>\n"
            "    <li>Punto clave 1</li>\n"
            "    <li>Punto clave 2</li>\n"
            "  </ul>\n"
            "</div>\n\n"
            "Responde únicamente con un bloque de código HTML bien formateado y estilizado con Tailwind CSS. "
            "Adapta el contenido según el tipo de video analizado.\n\n"
            "Texto a analizar:\n"
            f"{text_to_be_analyzed}"
        )
        return ChatPromptTemplate.from_messages([
            ('system', prompt_text),
            ('user', text_to_be_analyzed)
        ])

