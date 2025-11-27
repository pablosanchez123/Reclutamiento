
from core.candidato import Candidato
from db.dbActions import insertar_cv

def guardar_candidato(candidato: Candidato):

    insertar_cv(
        candidato.nombre_persona,
        candidato.nombre_archivo,
        candidato.texto_cv
    )

    print("Guardado a la base de datos.")
