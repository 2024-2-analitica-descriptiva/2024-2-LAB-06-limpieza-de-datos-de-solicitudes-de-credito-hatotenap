"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd
import os
# Vamos a usar funciones auxiliares de limpieza para las distintas columnas críticas como lo son:
#  fecha de beneficio, monto del crédito 

# vamos a usar una función para normalizar las demás columnas 

def limpiar_fecha(df):
    # separamos la fecha_de_beneficio en día, mes y año
    df[['día', 'mes', 'año']] = df['fecha_de_beneficio'].str.split('/', expand=True)
    # filtramos las filas donde el año tiene menos de 4 dígitos, y seleccionamos el dia y año de esas filas
    df.loc[df['año'].str.len() < 4, ['día', 'año']] = df.loc[
        # sobre-escribe las columnas dia y año con valores intercambiados (año pasa a día y visceversa)
        df['año'].str.len() < 4, ['año', 'día']
    ].values
    # combinamos las colunas en un formato de fecha AAAA-MM-DD
    df['fecha_de_beneficio'] = df['año'] + '-' + df['mes'] + '-' + df['día']
    # Eliminamos las columnas que se crearon 
    df.drop(['día', 'mes', 'año'], axis=1, inplace=True)
    return df
# Normalizamos las columnas a minúscylas y quitamos puntuación innecesaria
def limpiar_columnas_texto(df):
    """Normaliza las columnas de texto."""
    columnas_objeto = ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'línea_credito']
    df[columnas_objeto] = df[columnas_objeto].apply(
        lambda x: x.str.lower().replace(['-', '_'], ' ', regex=True).str.strip()
    )
    df['barrio'] = df['barrio'].str.lower().replace(['-', '_'], ' ', regex=True)
    return df
# Otra columna crítica es el monto, entonces normalizamos los valores NaN , los convertimos a 0y quitamos los decimales.00
def limpiar_monto(df):
    """Limpia y convierte 'monto_del_credito'."""
    df['monto_del_credito'] = (
        df['monto_del_credito']
        .str.replace("[$, ]", "", regex=True)
        .str.strip()
    )
    df['monto_del_credito'] = pd.to_numeric(df['monto_del_credito'], errors='coerce')
    df['monto_del_credito'] = df['monto_del_credito'].fillna(0).astype(int)
    df['monto_del_credito'] = df['monto_del_credito'].astype(str).str.replace('.00', '')
    return df


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    
    data = 'files/input/solicitudes_de_credito.csv'
    df = pd.read_csv(data, sep=';')

    df.drop(['Unnamed: 0'], axis=1, inplace=True)

    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    df = limpiar_fecha(df)
    df = limpiar_columnas_texto(df)
    df = limpiar_monto(df)

    df.drop_duplicates(inplace=True)

    os.makedirs('files/output', exist_ok=True)
    df.to_csv('files/output/solicitudes_de_credito.csv', sep=';', index=False)

    return df.head()