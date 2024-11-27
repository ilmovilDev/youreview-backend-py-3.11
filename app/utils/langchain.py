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
            "Tu tarea es analizar un texto transcrito de un video de YouTube, identificar el tipo de contenido y "
            "proporcionar un resumen breve y claro en español, formateado en HTML estilizado con Tailwind CSS. "
            "El resultado debe ser visualmente atractivo y responsivo.\n\n"

            "### Tipos de contenido y directrices:\n"
            "- **Musicales**: Describe el tema o género, menciona el artista y destaca emociones o mensajes clave.\n"
            "- **Noticias**: Resume eventos clave y su impacto; usa listas para múltiples eventos relevantes.\n"
            "- **Tutoriales**: Enumera los pasos principales y consejos clave.\n"
            "- **Tecnología**: Destaca productos, innovaciones o conceptos clave y tendencias.\n"
            "- **Educativos**: Resalta conceptos principales, aprendizajes y utilidad práctica.\n"
            "- **Entretenimiento**: Identifica el tema central, personajes o eventos destacados.\n"
            "- **Salud/Ciencia**: Resume puntos clave, hallazgos o consejos prácticos.\n\n"

            "### Formato del HTML:\n"
            "- Usa `<section>` como contenedor principal con las clases `flex flex-col gap-y-4`.\n"
            "- Párrafos: Usa `<p>` con las clases `text-gray-500 text-sm md:text-md tracking-wide leading-tight font-normal`.\n"
            "- Listas: Usa `<ul>` y `<li>` con las clases `list-disc text-gray-500 text-sm md:text-md tracking-wide leading-tight font-normal`.\n\n"

            "### Ejemplo de salida:\n"
            "<section class='flex flex-col gap-y-4'>"
            "  <p class='text-gray-500 text-sm md:text-md tracking-wide leading-tight font-normal'>Resumen adaptado al tipo de contenido.</p>\n"
            "  <ul class='list-disc text-gray-500 text-sm md:text-md tracking-wide leading-tight font-normal'>\n"
            "    <li>Punto clave 1</li>\n"
            "    <li>Punto clave 2</li>\n"
            "  </ul>\n"
            "</section>"

            "Responde únicamente con el bloque de código HTML estilizado con Tailwind CSS, adaptado al tipo de video analizado.\n\n"
            f"{text_to_be_analyzed}"
        )

        return ChatPromptTemplate.from_messages([
            ('system', prompt_text),
            ('user', text_to_be_analyzed)
        ])

