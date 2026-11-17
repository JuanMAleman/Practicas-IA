import numpy as np
import pandas as pd
from sklearn.datasets import make_classification, load_iris

# Generar el dataset sintético con tres clases y ruido estructurado
def cargar_dataset_sintetico():
    X, y = make_classification(
        n_samples=1000,
        n_features=4,
        n_informative=3,
        n_redundant=1,
        n_repeated=0,
        n_classes=3,
        n_clusters_per_class=1,
        class_sep=1.2,
        flip_y=0,
        random_state=42
    )

    # Definir el porcentaje de ruido que se desea introducir
    porcentaje_ruido = 0.80

    if not 0 <= porcentaje_ruido <= 1:
        raise ValueError("El porcentaje de ruido debe estar entre 0 y 1.")

    # Seleccionar una región específica para introducir ruido
    rng = np.random.default_rng(42)
    x1_min, x1_max = np.quantile(X[:, 0], [0.40, 0.70])
    x2_min, x2_max = np.quantile(X[:, 1], [0.35, 0.65])
    mascara = (
        (X[:, 0] >= x1_min) & (X[:, 0] <= x1_max) &
        (X[:, 1] >= x2_min) & (X[:, 1] <= x2_max)
    )

    # Modificar el porcentaje seleccionado de las etiquetas dentro de la región
    indices_region = np.where(mascara)[0]
    cantidad_ruido = int(len(indices_region) * porcentaje_ruido)
    clases_originales = np.array([], dtype=int)

    if cantidad_ruido > 0:
        indices_ruidosos = rng.choice(
            indices_region,
            size=cantidad_ruido,
            replace=False
        )
        clases_originales = y[indices_ruidosos].copy()
        y[indices_ruidosos] = (y[indices_ruidosos] + 1) % 3

    # Calcular la distribución de las etiquetas modificadas
    cambios_clases = {}
    for clase in range(3):
        cantidad = np.sum(clases_originales == clase)
        cambios_clases[f"Clase {clase} -> Clase {(clase + 1) % 3}"] = int(cantidad)

    # Organizar la información del ruido estructurado
    informacion_ruido = {
        "caracteristicas": "Caracteristica_1 y Caracteristica_2",
        "limites": {
            "caracteristica_1": (x1_min, x1_max),
            "caracteristica_2": (x2_min, x2_max)
        },
        "registros_region": len(indices_region),
        "porcentaje_ruido": porcentaje_ruido * 100,
        "registros_modificados": cantidad_ruido,
        "porcentaje_dataset": cantidad_ruido / len(y) * 100,
        "cambios_clases": cambios_clases
    }

    # Organizar los datos en DataFrames
    columnas = [f"Caracteristica_{i}" for i in range(1, 5)]
    X = pd.DataFrame(X, columns=columnas)
    y = pd.Series(y, name="Clase")

    return X, y, informacion_ruido

# Cargar el dataset Iris de Scikit-learn
def cargar_dataset_iris():
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target, name="Clase")
    return X, y

# Obtener los datasets
def obtener_datasets():
    X_iris, y_iris = cargar_dataset_iris()
    X_sintetico, y_sintetico, informacion_ruido = cargar_dataset_sintetico()

    return {
        "iris": {
            "nombre": "Dataset Iris",
            "X": X_iris,
            "y": y_iris
        },
        "sintetico": {
            "nombre": "Dataset Sintetico",
            "X": X_sintetico,
            "y": y_sintetico,
            "ruido": informacion_ruido
        }
    }

# Mostrar información general del dataset
def mostrar_informacion_dataset(datos):
    X, y = datos["X"], datos["y"]

    print("\n" + "=" * 60)
    print(f"INFORMACION: {datos['nombre'].upper()}")
    print("=" * 60)

    print(f"Registros: {len(X)}")
    print(f"Características: {X.shape[1]}")
    print(f"Clases: {y.nunique()}")

    # Mostrar la distribución de clases
    print("\nDistribución de clases:")
    for clase, cantidad in y.value_counts().sort_index().items():
        print(f"Clase {clase}: {cantidad} ({cantidad / len(y) * 100:.2f}%)")

    # Mostrar información del ruido estructurado
    if "ruido" in datos:
        ruido = datos["ruido"]
        limites = ruido["limites"]

        print("\nINFORMACIÓN DEL RUIDO ESTRUCTURADO")
        print("-" * 60)
        print("Tipo de ruido: Modificación estructurada de etiquetas")
        print(f"Características utilizadas: {ruido['caracteristicas']}")

        print("\nLímites de la región afectada:")
        print(f"Característica 1: {limites['caracteristica_1'][0]:.3f} a {limites['caracteristica_1'][1]:.3f}")
        print(f"Característica 2: {limites['caracteristica_2'][0]:.3f} a {limites['caracteristica_2'][1]:.3f}")

        print(f"\nRegistros dentro de la región: {ruido['registros_region']}")
        print(f"Porcentaje de ruido aplicado: {ruido['porcentaje_ruido']:.2f}%")
        print(f"Etiquetas modificadas: {ruido['registros_modificados']}")
        print(f"Porcentaje respecto al dataset completo: {ruido['porcentaje_dataset']:.2f}%")

        print("\nDistribución de etiquetas modificadas:")
        for cambio, cantidad in ruido["cambios_clases"].items():
            print(f"{cambio}: {cantidad}")

    # Mostrar los primeros cinco registros
    print("\nPrimeros cinco registros:")
    muestra = X.head().copy()
    muestra["Clase"] = y.head().values
    print(muestra.to_string(index=False))

    # Mostrar estadísticas descriptivas
    print("\nEstadísticas descriptivas:")
    print(X.describe().round(2).to_string())

    # Comprobar los valores faltantes
    print("\nValores faltantes:")
    faltantes = X.isnull().sum()
    print(faltantes.to_string())
    print(f"\nTotal de valores faltantes: {faltantes.sum()}")

    print("=" * 60)
