import datetime
import io

import streamlit as st
from github import Github
import pandas as pd

REPO_URL = "https://raw.githubusercontent.com/karendcl/p1/main/"
GITHUB_TOKEN = st.secrets["github_token"]  # Use Streamlit secrets in production
REPO_NAME = "karendcl/p1"  # Your repo
FILE_PATH = "admin.xlsx"  # Path to your excel file
BRANCH = "main"  # Branch to update

def github_commit_file(file_name, content, commit_message, admin=False):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{timestamp}_{file_name}" if not admin else file_name

    github_file_path = f"data/{file_name}"

    repo.create_file(
        path=github_file_path,
        message=commit_message,
        content=content,
        branch=BRANCH
        ) if not admin else repo.update_file(
            path=github_file_path,
            message=commit_message,
            content=content,
            branch=BRANCH,
            sha=repo.get_contents(github_file_path, ref=BRANCH).sha
        )

    return github_file_path

def update_admin_excel_file(file_link, carrera, year, asign, semestre, prof, days_not_available,
                            turnos_not_available, prof_other_subjects, act_full_year,
                            need_joined, precendence_conf):
    """Function to update the admin Excel file with the latest data."""
    # This function would contain logic to update the Excel file
    # For example, you could read the JSON data and write it to an Excel file

    time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    file_link = f"{REPO_URL}data/{file_link}"
    carrera = carrera
    year = year
    asign = asign
    semestre = semestre
    prof = prof.replace(',', '\n')
    days_not_available = ', '.join(days_not_available)
    turnos_not_available = ', '.join(turnos_not_available)
    prof_other_subjects = prof_other_subjects
    act_full_year = ', '.join(act_full_year)
    need_joined = "Si" if need_joined else "No"
    precendence_conf = ', '.join(precendence_conf)

#         create a record to insert in the admin Excel file
    record = {
        "Marca Temporal": time,
        "Archivo P1": file_link,
        "Carrera": carrera,
        "Año": year,
        "Nombre corto de la asignatura": asign,
        "Semestre": semestre,
        "Nombre de profesores que participan": prof,
        "Días en que no se peuede impartir la asignatura": days_not_available,
        "Turnos en que no se puede impartir la asignatura": turnos_not_available,
        "Profesores que participan en otras asignaturas": prof_other_subjects,
        "Actividades al grupo (año) completo": act_full_year,
        "Necesidad d eunir carreras": need_joined,
        "Precedencia de las conferencias en la semana ": precendence_conf
    }

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # Read the existing data from the excel file
    try:
        contents = repo.get_contents(FILE_PATH, ref=BRANCH)
        # Wrap bytes in BytesIO and specify engine
        excel_data = io.BytesIO(contents.decoded_content)
        df = pd.read_excel(excel_data, engine='openpyxl')  # or 'xlrd' for older .xls files
    except Exception as e:
        print(f"Error reading file: {e}")
        df = pd.DataFrame()

    try:
        # Safely add record (ensure it's a dictionary or DataFrame)
        if isinstance(record, dict):
            record_df = pd.DataFrame([record])
        else:
            record_df = pd.DataFrame(record)

        df = pd.concat([df, record_df], ignore_index=True)

        # Save to Excel in memory
        output = io.BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        updated_excel = output.getvalue()

        # Verify file exists before committing
        try:
            repo.get_contents(FILE_PATH, ref=BRANCH)
            commit_message = "Update admin Excel file with new P1 form data"
            github_commit_file(FILE_PATH, updated_excel, commit_message, admin=True)
        except Exception as e:
            print(f"Error verifying file or committing: {e}")
            # Handle case where file doesn't exist - might need to create it
            github_commit_file(FILE_PATH, updated_excel, "Create new admin Excel file", admin=True)

    except Exception as e:
        print(f"Error processing or saving data: {e}")





def upload_p1_form(uploaded_file):
    """Function to handle the upload of the P1 form."""

    file_path = f"data/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with open(file_path, 'rb') as file:
        file_content = file.read()

    commit_message = f"Upload P1 form: {uploaded_file.name}"
    gh_file_path = github_commit_file(uploaded_file.name, file_content, commit_message, admin=False)
    print(f"File uploaded to GitHub: {gh_file_path}")
    return gh_file_path



def main():
    # Set the page configuration
    st.set_page_config(
        page_title="P1 ",
        page_icon=":guardsman:",  # Emoji icon
    )

    # Title of the app
    st.title("P1 Formularios")

    # Display a welcome message
    st.write("Bienvenido a la plataforma para la entrega del P1 a administración")
    st.write("Paso 1: Descargue el siguiente archivo excel y complete su formulario P1")

    # Provide a link to download the Excel file
    path = REPO_URL + "P1_Generar_pru.xlsm"
    st.markdown(f"[Download File P1_Generar]({path})", unsafe_allow_html=True)

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

    # separator
    st.markdown("---")
    year = st.selectbox(
        "Seleccione el año en que se imparte la asignatura",
        ['1er Año',
         '2do Año',
         '3er Año',
         '4to Año']
    )

    st.markdown("---")
    asign = st.text_input(
        "Ingrese la abreviatura del nombre de la asignatura que le generó automaticamente el archivo excel",
        placeholder="Ejemplo: BIO123"
    )

    st.markdown("---")

    semestre = st.selectbox(
        "Seleccione el semestre al que se imparte",
        ['Primer Semestre',
         'Segundo semestre']
    )
    st.markdown("---")

    prof = st.text_input(
        "Ingrese el nombre los nombres de los profesores que participen, separados por comas ",
        placeholder="Ejemplo: Juan Pérez, Juana Perez, Mengano Don Nadie"
    )
    st.markdown("---")

    days_not_available = st.multiselect(
        "Seleccione los días en que no se puede impartir la asignatura en ningun turno de clase",
        ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    )
    st.markdown("---")

    turnos_not_available = st.multiselect(
        "Seleccione los turnos en los que no se puede impartir la asignatura en ningun dia de la semana",
        ['1ero', '2do', '3ero', '4to', '5to', '6to',]
    )
    st.markdown("---")

    prof_other_subjects = st.text_area(
        """Especifique los nombres, las asignaturas y el tipo de docencia que imparten los profesores que participan en otras asignaturas, siguiendo este patrón:
Nombre del profesor, Nombre de la otra asignatura, Tipo de docencia que imparte
El tipo de la docencia debe ser Conf, CP, Sem, LAB, según corresponda.

Por ejemplo si el profesor Fulano De Tal imparte seminarios de otra asignatura y el profesor Mengano Don Nadie imparte conferencias de otra asignatura y también clases prácticas de una tercera, usted debe ponerlos así:

Fulano De Tal, Introducción a los apagones, Sem

Mengano Don Nadie, Introducción al arte de sobrevivir, Conf

Mengano Don Nadie, Como llegar temprano, CP""")
    st.markdown("---")

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
    st.markdown("---")

    need_joined = st.checkbox(
        "Necesito que se unan los grupos de la asignatura para poder impartirla",
        value=False
    )
    st.markdown("---")

    precendence_conf = st.multiselect(
        "Seleccione aquellas actividades que deben ser impartidas despues que las conferencias de la semana en curso",
        ['Seminarios', 'Clases Prácticas', 'Laboratorios']

    )
    st.markdown("---")

    if st.button("Enviar"):
        # Here you would typically handle the form submission,
        # e.g., save the data to a database or send it to an API.
        if uploaded_file is None or not asign or not prof:
            st.error("Por favor, complete todos los campos requeridos antes de enviar el formulario.")
        else:
            st.success("Formulario enviado con éxito. Gracias por su participación.")
            # Upload the P1 form
            p1_form = upload_p1_form(uploaded_file)
            # Update the admin Excel file
            update_admin_excel_file(
                p1_form, carrera, year, asign, semestre, prof,
                days_not_available, turnos_not_available,
                prof_other_subjects, act_full_year,
                need_joined, precendence_conf
            )



if __name__ == "__main__":
    main()
