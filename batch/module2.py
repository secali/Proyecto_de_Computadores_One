import sys
import batch.functions
import batch.module3
from tabulate import tabulate
import pandas as pd
import numpy as np


def batchTwo():
    print("\n############ Ejecutando Batch 2: CSV y manejo de datos #############")
    # obtener ruta fichero a cargar
    print("\nCargando fichero...")
    file = batch.functions.obtener_ruta()

    # creamos dataframe con datos fichero
    dfDataSet = pd.read_csv(file, delimiter='\t')
    print(dfDataSet)

    # imprimir primera tabla pedida

    # Calcular el número total de instancias
    n_total = len(dfDataSet)
    # Filtrar instancias humanas y generadas
    dfHuman = dfDataSet[dfDataSet['Type'] == 'h']
    dfIA = dfDataSet[dfDataSet['Type'] == 'g']
    # Número de instancias humanas y generadas
    n_humano = len(dfHuman)
    n_generadas = len(dfIA)

    # Longitud media de caracteres para instancias humanas y generadas
    long_media_humano = dfHuman[
        'Text'].str.len().mean()
    long_media_generadas = dfIA[
        'Text'].str.len().mean()

    # Creamos una lista con los datos
    data = [
        ["Número total de instancias", n_total],
        ["Número de instancias humanas", n_humano],
        ["Número de instancias generadas", n_generadas],
        ["Longitud media de instancias humanas", f"{long_media_humano:.2f}"],
        ["Longitud media de instancias generadas", f"{long_media_generadas:.2f}"]
    ]
    # imprimimos los datos en forma de tabla tabulada
    print(tabulate(data, headers=["Campo", "Valor"], tablefmt="grid"))

    # balanceamos el numero de resultados
    if n_humano > n_generadas:
        # elegimos de forma random los indices a borrar
        indices_to_remove = np.random.choice(dfHuman.index, (n_humano - n_generadas), replace=False)
        # ajustamos el dataframe al tamaño adecuado
        dfHuman = dfHuman.drop(indices_to_remove)
    if n_humano < n_generadas:
        # elegimos de forma random los indices a borrar
        indices_to_remove = np.random.choice(dfIA.index, (n_generadas - n_humano), replace=False)
        # ajustamos el dataframe al tamaño adecuado
        dfIA = dfIA.drop(indices_to_remove)

    # construimos el dataset final
    dfDataSet = pd.concat([dfHuman, dfIA], ignore_index=True)

    batch.module3.batchThree(dfHuman, dfIA)
