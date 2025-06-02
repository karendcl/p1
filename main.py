import streamlit as st

def main():
    # Set the page configuration
    st.set_page_config(
        page_title="P1 ",
        page_icon=":guardsman:",  # Emoji icon
        layout="wide",  # Full width layout
    )

    # Title of the app
    st.title("P1 Formularios")

    # Display a welcome message
    st.write("Bienvenido a la plataforma para la entrega del P1 a administración")
    st.write("Paso 1: Descrague el siguiente archivo excel y comlete su formylario P1")

    # Provide a link to download the Excel file
    if st.button("Descargar P1 Excel"):
        # Link to the Excel file
        excel_file_url = "https://raw.githubusercontent.com/karendcl/p1/main/P1_Generar_pru.xlsx"
        st.markdown(f"[Descargar P1 Excel]({excel_file_url})", unsafe_allow_html=True)

    # Display instructions for filling out the form
    st.write("Paso 2: Una vez completado el formulario, súbalo a continuación."
             "Copie la abreviatura del nombre de la asignatura que le generó")

    # File uploader for the completed P1 form
    uploaded_file = st.file_uploader("Sube tu formulario P1 aquí", type=["xlsx"])

    st.write("Paso 3: Complete todas las preguntas a continuación")

    carrera = st.selectbox(
        "Seleccione la carrera a la que se imparte",
        ['Bioligia',
         'Microbiologia',
         'Bioquimica y Biologia Molecular']
    )

    asign = st.text_input(
        "Ingrese la abreviatura del nombre de la asignatura que le generó automaticamente el archivo excel",
        placeholder="Ejemplo: BIO123"
    )

    semestre = st.selectbox(
        "Seleccione el semestre al que se imparte",
        ['Primer Semestre',
         'Segundo semestre']
    )

    prof = st.text_input(
        "Ingrese el nombre los nombres de los profesores que participen, separados por comas ",
        placeholder="Ejemplo: Juan Pérez, Juana Perez"
    )

    days_not_available = st.multiselect(
        "Seleccione los días en que no se puede impartir la asignatura en ningun turno de clase",
        ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    )

    turnos_not_available = st.multiselect(
        "Seleccione los turnos en los que no se puede impartir la asignatura en ningun dia de la semana",
        ['1ero', '2do', '3ero', '4to', '5to', '6to',]
    )

    prof_other_subjects = st.text_input(
        """Especifique los nombres, las asignaturas y el tipo de docencia que imparten los profesores que participan en otras asignaturas, siguiendo este patrón:
Nombre del profesor, Nombre de la otra asignatura, Tipo de docencia que imparte
El tipo de la docencia debe ser Conf, CP, Sem, LAB, según corresponda.

Por ejemplo si el profesor Fulano De Tal imparte seminarios de otra asignatura y el profesor Mengano Don Nadie imparte conferencias de otra asignatura y también clases prácticas de una tercera, usted debe ponerlos así:

Fulano De Tal, Introducción a los apagones, Sem
Mengano Don Nadie, Introducción al arte de sobrevivir, Conf
Mengano Don Nadie, Como llegar temprano, CP""")

    act_full_year = st.multiselect(
        "Seleccione el tipo de actividad que se impartirá al año completo, en lugar de ser impartida a cada subgrupo por separado.",
        ['Las Conferencias serán impartidas al año completo',
        'Los Seminarios serán impartidos al año completo',
         'Las Clases Prácticas serán impartidas al año completo',
         'Los Laboratorios serán impartidos al año completo',
         'Las Evaluaciones Parciales serán impartidas al año completo',
         'El trabajo de curso sera realizado al año completo',
         ]
    )

    need_joined = st.checkbox(
        "Necesito que se unan los grupos de la asignatura para poder impartirla",
        value=False
    )

    precendence_conf = st.multiselect(
        "Seleccione aquellas actividades que deben ser impartidas despues que las conferencias de la semana en curso",
        ['Seminarios', 'Clases Prácticas', 'Laboratorios']

    )






