import streamlit as st
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_groq import ChatGroq

template = """
    You are an expert "product owner". Below is a draft text with a list of requeriments.
    Your goal is to:
    - Properly redact a user story following the pattern: 'As [user role], I want [action], for [benefit].' 
    - create a set of user stories instead of a single one if needed.
    - Your response should be translated into spanish
    - try to create the minimal number of user stories
    
    Here are some examples :
    - Example 1:

        Como: usuario registrado
        Quiero: restablecer mi password
        Para: recuperar el acceso a mi cuenta si la olvido o la pierdo.
        Criterios de entrega:
        -El usuario debe ingresar su dirección de correo electrónico en un formulario de "Recuperar contraseña".
        -El sistema debe enviar un correo electrónico con un enlace de restablecimiento de contraseña.
        -El enlace de restablecimiento debe ser válido por 24 horas.
        -Al hacer clic en el enlace, el usuario debe ser redirigido a una página donde pueda ingresar una nueva contraseña.
        -La nueva contraseña debe tener al menos 8 caracteres, con al menos una letra mayúscula, un número y un carácter especial.
        -El sistema debe confirmar el cambio de contraseña y permitir al usuario iniciar sesión con la nueva contraseña.
    
    - Ejemplo 2:

        Como: un administrador del sistema
        Quiero: ver un reporte diario del uso de recursos del servidor
        Para: asegurarme de que el sistema funciona de manera eficiente y prevenir problemas.
        Criterios de entrega:
        -El reporte debe incluir el uso de CPU, memoria, y espacio en disco de los últimos 24 horas.
        -El reporte debe generarse automáticamente cada día a las 8:00 AM y ser enviado por correo al administrador.
        -El correo debe incluir un archivo adjunto en formato PDF con el reporte detallado.
        -El reporte debe incluir un resumen visual (gráfica) del uso promedio en las últimas 24 horas.
        -Si el uso de recursos supera el 80%, debe generarse una alerta en el reporte y en el sistema de notificaciones.
    
    Please start the redaction with a warm introduction. Add the introduction \
        if you need to.
    
    Below is the draft text, tone, and dialect:
    DRAFT: {draft}
    YOUR RESPONSE:
"""

# prompttemplate
prompt = ChatPromptTemplate(
    messages=[
        HumanMessagePromptTemplate.from_template(template)
    ],
    input_variables={"draft"},

)

#LLM and key loading function
def load_LLM(groq_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = ChatGroq(
    groq_api_key=groq_api_key, 
    model_name="llama3-70b-8192", 
    temperature=0.7)
    return llm


#Page title and header
st.set_page_config(page_title="User Stories Creator")
st.header("Crea Historias de Usuario a partir de una lista de requisitos proporcionada")


#Intro: instructions
col1, col2 = st.columns(2)

with col1:
    st.markdown("Hola soy un experto Product Owner y estoy aqui para ayudarte")

with col2:
    st.write("Contacte con Softtek para construir sus proyectos de IA")


#Input Groq API Key
st.markdown("## Introduzca su clave API de ChatGroq")

def get_groq_api_key():
    input_text = st.text_input(label="ChatGroq API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input", type="password")
    return input_text

groq_api_key = get_groq_api_key()


# Input
st.markdown("## Introduzca los requisitos")

def get_draft():
    draft_text = st.text_area(label="Text", label_visibility='collapsed', placeholder="Your Text...", key="draft_input")
    return draft_text

draft_input = get_draft()

if len(draft_input.split(" ")) > 700:
    st.write("Por favor, introduzca un texto más corto. La longitud máxima es de 700 palabras.")
    st.stop()

    
# Output
st.markdown("### La propuesta de user stories es:")

if draft_input:
    if not groq_api_key:
        st.warning('Please insert groq API Key. \
            Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', 
            icon="⚠️")
        st.stop()

    llm = load_LLM(groq_api_key = groq_api_key)

    prompt_with_draft = prompt.format_prompt(
        draft=draft_input
    )

    improved_redaction = llm.invoke(prompt_with_draft)
    improved_redaction_content = improved_redaction.content
    st.write(improved_redaction_content)
