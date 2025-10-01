pip install flask pandas openpyxl
import pandas as pd
from flask import Flask, render_template, request, jsonify

# Nombre del archivo Excel en la carpeta raíz
ARCHIVO_EXCEL = "CODIGOSJDESAP.xlsx"

# Inicializa la aplicación Flask
app = Flask(__name__)

# Variable global para almacenar el DataFrame
df = None

def cargar_datos():
    """Carga el archivo Excel en un DataFrame de Pandas."""
    global df
    try:
        # Intenta cargar la primera hoja del Excel.
        # Ajusta 'sheet_name' si necesitas una hoja específica.
        df = pd.read_excel(ARCHIVO_EXCEL, sheet_name=0) 
        # Convertir todas las columnas a string para evitar errores de tipo en la búsqueda
        df = df.astype(str)
        print(f"✅ Datos cargados exitosamente de {ARCHIVO_EXCEL}.")
    except FileNotFoundError:
        print(f"❌ ERROR: El archivo '{ARCHIVO_EXCEL}' no se encontró en la carpeta raíz.")
        df = pd.DataFrame() # Crear un DataFrame vacío para evitar fallos
    except Exception as e:
        print(f"❌ ERROR al cargar el archivo Excel: {e}")
        df = pd.DataFrame()

@app.before_first_request
def inicializar():
    """Función que se ejecuta una vez antes de la primera petición."""
    cargar_datos()

@app.route('/', methods=['GET', 'POST'])
def index():
    """Ruta principal: muestra el formulario y los resultados de búsqueda."""
    resultados = []
    termino_busqueda = ""
    
    # Comprueba si hay datos cargados
    if df.empty:
        return render_template('index.html', error="No se pudo cargar el archivo de datos.")

    if request.method == 'POST':
        # Obtener el término de búsqueda del formulario
        termino_busqueda = request.form.get('busqueda', '').strip().lower()

        if termino_busqueda:
            # Lógica de búsqueda:
            # Buscamos en TODAS las columnas por el término.
            # Convertimos todo a minúsculas para una búsqueda insensible a mayúsculas.
            
            # 1. Crear una máscara booleana que es True si el término está en CUALQUIER columna de esa fila
            mask = df.apply(
                lambda row: row.astype(str).str.lower().str.contains(termino_busqueda).any(),
                axis=1
            )
            
            # 2. Aplicar la máscara y convertir los resultados a una lista de diccionarios
            resultados = df[mask].to_dict('records')

    # Renderizar la plantilla con los resultados y el término de búsqueda
    return render_template('index.html', 
                           resultados=resultados, 
                           termino_busqueda=termino_busqueda,
                           columnas=df.columns.tolist() if not df.empty else [])

# Para ejecutar la aplicación
if __name__ == '__main__':
    # Usar debug=True solo durante el desarrollo
    app.run(debug=True)
