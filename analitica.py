import pandas as pd

def convertir_a_mib(valor):
    """Convierte valores de RAM en GiB, MiB, KiB o B a MiB."""
    if isinstance(valor, str):
        if 'GiB' in valor:
            return float(valor.replace(' GiB', '')) * 1024
        elif 'MiB' in valor:
            return float(valor.replace(' MiB', ''))
        elif 'KiB' in valor:
            return float(valor.replace(' KiB', '')) / 1024
        elif 'B' in valor:
            return float(valor.replace(' B', '')) / (1024 * 1024)
    return float(valor) 

def convertir_a_kbps(valor):
    """Convierte valores de tráfico de red en Mb/s, kb/s o b/s a kb/s."""
    if isinstance(valor, str):
        if 'Mb/s' in valor:
            return float(valor.replace(' Mb/s', '')) * 1000 
        elif 'kb/s' in valor:
            return float(valor.replace(' kb/s', '')) 
        elif 'b/s' in valor:
            return float(valor.replace(' b/s', '')) / 1000 
    return float(valor) 

def convertir_a_porcentaje(valor):
    """Convierte valores de porcentaje (con '%') a números flotantes."""
    if isinstance(valor, str):
        return float(valor.replace('%', ''))
    return float(valor) 

def analizar_csv(ruta, conversion=None):
    df = pd.read_csv(ruta, delimiter=',')

    if conversion:
        for col in df.columns[1:]:
            df[col] = df[col].apply(conversion)

    if df.empty or not all(pd.api.types.is_numeric_dtype(df[col]) for col in df.columns[1:]):
        raise ValueError("El DataFrame está vacío o no contiene datos numéricos.")

    df_stats = df.describe().loc[['min', 'max', 'mean']].round(2)
    return df_stats

# Archivos de entrada
archivo_ram = "./data/ram-data.csv"
archivo_red = "./data/network-data.csv"
archivo_cpu = "./data/cpu-data.csv"

try:
    # Análisis de cada archivo
    df_ram_stats = analizar_csv(archivo_ram, convertir_a_mib)
    df_red_stats = analizar_csv(archivo_red, convertir_a_kbps)
    df_cpu_stats = analizar_csv(archivo_cpu, convertir_a_porcentaje)

    # Guardar estadísticas en un solo archivo CSV con tablas separadas
    with open("estadisticas.csv", "w") as f:
        f.write("=== Estadísticas de RAM ===\n")
        df_ram_stats.to_csv(f)
        f.write("\n=== Estadísticas de Tráfico de Red ===\n")
        df_red_stats.to_csv(f)
        f.write("\n=== Estadísticas de CPU ===\n")
        df_cpu_stats.to_csv(f)

    print("Análisis completado. Se guardaron los resultados en 'estadisticas.csv'")
except Exception as e:
    print(f"Error durante el análisis: {e}")