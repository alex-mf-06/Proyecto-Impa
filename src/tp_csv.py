import json

from typing import Dict , List , Tuple , Any
import re
ruta_chicas_dev = "Todas.las.carreras27032018.csv"


def agrupar_solo_universidades(Ruta_archivo:str) -> List[Dict[str,str]]:

  """

  Esta funcion se va a encargar de que va a cargar de que la ruta de archivo que le pasen va a cargarlo y para posteriormente se carge a una lista que solo van a entrar los institutos educativos que empiecen en Universidad .
  precondiciones :
  El parametro que le pasen debe ser una ruta de archivo que exista y debe ser un archivo csv.
  postcondiciones :
  devuelve una lista de diccionarios que la institucion empiece con universidad .

  """
  try :
    with open (Ruta_archivo ,"rt", encoding="utf-8") as institutos :
      encabezado = institutos.readline()
      encabezado = encabezado.strip().split(",")
      universidades = []
      while True:
        linea = institutos.readline()
        if not linea :
          break
        else :
          datos = linea.strip().split(",")
          instituto = datos[1]
          if re.search(r"uni\w*", instituto, re.IGNORECASE):

            uni = dict(zip(encabezado,datos))
            universidades.append(uni)
    print("Archivo cargado con éxito")
    print(f"Se cargaron {len(universidades)} Universidades")
    return universidades
  except FileNotFoundError:
        print(f"Error: El archivo {Ruta_archivo} no se encuentra.")
        return []


def mostrar_solo_universidades(universidades:List[Dict[str,str]]) -> None :
  """


  """

  try :
    solo_universidades = set([universidad.get("Institución") for universidad in universidades if universidad.get("Institución")])

    for i in solo_universidades :
      print("="*50)
      print(f"\n{i}\n")




  except TypeError:
    print("Hubo un error en el recorrido")
def buscar_universidad(universidades:List[Dict[str,str]]) -> None :
  """

  """
  try :
    while True :
      mostrar_solo_universidades(universidades)
      universidad_a_buscar = input("Ingrese una universidad : ").lower()
      resultado = list(filter(lambda u: universidad_a_buscar in u.get("Institución", "").lower(), universidades))

      if not resultado : 
        print(f"No se encontraron resultados similares con el nombre {universidad_a_buscar}")
        return 

      else : 
        print(f"Se encontraron {len(resultado)} resultados en la busqueda de {universidad_a_buscar} ")
        formato ="{:<7} {:<25} {:<25} {:<20}"
        print(formato.format("Año","Institución","Título","Egresadas Mujeres"))
        print("-"*50)
        for uni in resultado :

          datos_universidad = formato.format(
                        str(uni.get("Año", "N/A")),          
                        str(uni.get("Institución", "N/A")[:25]),  # Cortamos el nombre de la institución a 25 chars para que entre
                        str(uni.get("Título", "N/A")[:25]),   # Cortamos el título a 25 chars para que entre
                        str(uni.get("Egresados Mujeres", "0")) 
                    )
          print(datos_universidad)
        return


  except TypeError:
    print("Hubo un error en el recorrido de la lista")
    return None
  except KeyboardInterrupt:
    print("El usuario cancelo la busqueda..")
    return None
  except Exception as e :
    print(f"Hubo un error en {e}")
    return None


def exportar_alumnos_por_universidad(universidades:List[Dict[str,str]],) -> None :

  """

  """
  try : 
    mostrar_solo_universidades(universidades)
    while True :

      universidad_a_buscar = input("Ingrese una universidad para exportar sus alumnos : ").lower()
      if not universidad_a_buscar :
        print("No ingreso nada...")
        continue
      nombre_real = None
      for uni in universidades:
        if universidad_a_buscar == uni.get("Institución", "").lower():
          nombre_real = uni.get("Institución", "")
          break
      if not nombre_real :
        print(f"No se encontro la universidad {universidad_a_buscar} intente nuevamente...")
        continue
      resultado = list(filter(lambda u: universidad_a_buscar in u.get("Institución", "").lower(), universidades))
      if not resultado :
        print(f"No se encontraron resultados similares con el nombre {universidad_a_buscar}")
        return 
      else :
        ruta_salida = f"{nombre_real.replace(' ','_')}_alumnos.json"
        with open (ruta_salida,"w", encoding="utf-8") as archivo_salida :
          json.dump(resultado,archivo_salida, indent=4, ensure_ascii=False)
        print(f"Se exportaron los datos de {nombre_real} en el archivo {ruta_salida}")
        return
  except Exception as e :
    print(f"Hubo un error en {e}")
    return None

def mostrar_menu(iterable:Tuple[str]) -> None :
  """
  Esta funcion se encarga de mostrar los elementos de un iterable que debe ser en su defecto una tupla no retorna nada.
  precondiciones : El parametro que se necesita para la funcion debe ser una tupla con elementos que deben ser strings .
  postcondicines : No retorna nada pero muestra los elemtos de la tupla que serian las opciones del menu principal .
  """
  try :
    for i in iterable :
      print("="*50)
      print(f"\n{i}\n")


  except TypeError:
    print("ERROR - Hubo un error en el parametro que le dieron ....")


def mostrar_estadisticas_mujeres_egresadas(universidades: List[Dict[str, str]]) -> None:
    """
    Muestra un ranking de las carreras con más mujeres egresadas 
    para las universidades que coincidan con la búsqueda.
    """
    try:
        mostrar_solo_universidades(universidades)
        
        while True:
            print("\n" + "="*60)
            universidad_a_buscar = input("Ingrese nombre de universidad para ver estadísticas (o 'z' para volver): ").strip().lower()
            
            if universidad_a_buscar == 'z':
                return
            
            if not universidad_a_buscar:
                print("No ingresó nada. Intente nuevamente.")
                continue

            
            resultado = list(filter(
                lambda u: universidad_a_buscar in u.get("Institución", "").lower(), 
                universidades
            ))

            if not resultado:
                print(f"No se encontraron resultados para '{universidad_a_buscar}'.")
            else:
                universidades_egresados = []
                
               
                for uni in resultado:
                    raw_mujeres = uni.get("Egresados Mujeres", "0")
                    
                    
                    if not raw_mujeres or raw_mujeres.strip() == "":
                        cant_mujeres = 0
                    else:
                        try:
                            cant_mujeres = int(raw_mujeres)
                        except ValueError:
                            cant_mujeres = 0

                    uni_y_egresadas = {
                        "Institución": uni.get("Institución", "N/A"),
                        "Título": uni.get("Título", "N/A"), 
                        "Egresadas Mujeres": cant_mujeres  
                    }
                    universidades_egresados.append(uni_y_egresadas)

               
                uni_ordenado = sorted(universidades_egresados, key=lambda x: x["Egresadas Mujeres"], reverse=True)

                print(f"\nResultados para '{universidad_a_buscar}' (Ordenado por mayor cantidad de egresadas):")
                
                
                formato = "{:<35} {:<30} {:<10}"
                
                print("-" * 80)
                print(formato.format("INSTITUCIÓN", "CARRERA/TÍTULO", "MUJERES"))
                print("-" * 80)
                
                for uni in uni_ordenado:
                    datos_universidad = formato.format(
                        str(uni.get("Institución")[:33]),  # Cortamos para que entre
                        str(uni.get("Título")[:28]),       # Cortamos título
                        str(uni.get("Egresadas Mujeres"))
                    )
                    print(datos_universidad)
                
                # Pausa para leer
                input("\nPresione Enter para realizar otra búsqueda...")

    except Exception as e:
        print(f"Hubo un error inesperado: {e}")
        return None
def menu () -> None :



  opciones = (" a- Importar datos"," b- Buscar Universidad"," c- Exportar Alumnos por Universidad"," d- Estadísticas de total de Mujeres egresadas por universidad"," z- Salir")
  universidades = []
  while True :
    mostrar_menu(opciones)
    opcion = input("Ingresa la opcion que se te mostró : ").strip().lower()
    if opcion.lower() == "z":
      break
    elif opcion.lower() == "a":
      universidades = agrupar_solo_universidades(ruta_chicas_dev)

    elif opcion.lower() == "b" :
      if not universidades:
        print("No Estan cargadas las universidades....")
      else :
        buscar_universidad(universidades)

    elif opcion.lower() == "c" :
      if not universidades:
        print("No Estan cargadas las universidades....")
      else:
        exportar_alumnos_por_universidad(universidades)

    elif opcion.lower() == "d" :
      if not universidades :
        print("No Estan cargadas las universidades....")
      else :
        mostrar_estadisticas_mujeres_egresadas(universidades)
    else:
      print("ERROR Ingrese una de las opciones que se les muestre ")



if __name__ == "__main__":
  menu()



