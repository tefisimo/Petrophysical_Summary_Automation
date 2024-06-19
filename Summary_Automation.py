import pandas as pd
import os

print('''⠀⠀⠀⣾⣷⣦⡀⠀⠀⠀⢀⣴⣾⣷⡄⠀
⠀⠀⠀⠙⠿⣿⣷⡀⠀⢠⣿⣿⡿⣟⣀⠀
⠀⠰⣿⣿⣶⣄⠹⣇⢀⡿⠋⣵⣾⣿⣿⠆
⢰⣶⣶⣶⣤⣈⠓⢹⢸⢁⡾⠟⠋⠉⠁⠀
⠈⠛⠛⠉⠉⠙⠳⢌⠀⡞⠰⢶⡆⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣤⣤⣤⡄⠀⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⠃⢻⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡯⠓⠹⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣻⢟⠛⢛⢿⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⡯⠔⠋⠓⠬⣇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣸⠓⠢⣄⡤⠚⢻⡀⠀⠀⠀
⠀⠀⠀⠀⢀⣧⠔⠊⠁⠉⠒⢬⣇⠀⠀⠀
⠀⠀⣶⣶⣾⣷⣶⣶⣶⣶⣶⣶⣿⣶⣶⡆''')
print("Bienvenido al automatizador de sumarios petrofísicos")
nombreDePozo = input("Ingresa el nombre del pozo en MAYÚSCULAS: ")
os.system('cls')
rutaArchivo = input("Perfecto, ahora copia y pega la ruta del archivo por favor: \n")
df = pd.read_excel(f"{rutaArchivo}/PETROFISICA {nombreDePozo}.xls", sheet_name="NUMERICO")
os.system('cls')

df_without_nulls = df.dropna()
df_sin_ultima = df_without_nulls.drop(df_without_nulls.index[-1])

curvas = []
user_input = input("¿Cuales curvas quieres Usar? Separadas por coma y tal cual el cabezal del archivo excel \n")
os.system('cls')
curvas = user_input.split(",")

intervalos = {}
intervalos_lista = []
want_continue = True

while want_continue:
    intervalo_tope = int(input("¿Cual es el tope del intervalo?: \n"))
    intervalos.update({"Tope": intervalo_tope})
    
    intervalo_base = int(input("¿Cual es la base del intervalo?: \n"))
    intervalos.update({"Base": intervalo_base})
    
    intervalos.update({"Espesor": intervalo_base - intervalo_tope})
    intervalos.update({"ANP": intervalo_base - intervalo_tope})
    
    for column in curvas:
        average_per_column = df_sin_ultima.query(f"DEPTH >= {intervalo_tope} & DEPTH <= {intervalo_base}")[column].mean()
        intervalos.update({column: average_per_column.round(3)})
    
    intervalos_lista.append(intervalos)
    #print(intervalos_lista)
    
    intervalos = {}
    
    print("Excelente, ¿quisieras ingresar otro intervalo?")
    otro_intervalo = input('Oprime "S" en caso de que quieras, oprime "N" en caso de que hayas terminado. \n')
    os.system('cls')
    if otro_intervalo == "N":
        want_continue = False
        os.system('cls')

df_sumario = pd.DataFrame(columns = intervalos_lista[0].keys())

for i in range(0,len(intervalos_lista)):
    individual_row_data = (intervalos_lista[i].values())
    
    length = len(df_sumario)
    #print(len(df_sumario), " <- Fila cargada en el index")
    df_sumario.loc[length] = individual_row_data

df_sumario = df_sumario.astype({
    "Tope": "int",
    "Base": "int",
    "Espesor": "int",
    "ANP": "int"
})

df_sumario.to_csv(f"{rutaArchivo}/SumarioPetrofisico_{nombreDePozo}.csv", index = False)

print('Archivo creado satisfactoriamiente en la carpeta del archivo especificado...')
print(f'Nombre del archivo "SumarioPetrofisico_{nombreDePozo}.csv"')
print('Gracias por usar el automatizador de sumarios petrofisicos')