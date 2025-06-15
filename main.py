registro = []
completados = []

def agg(registro, completados, dato, nombre):
    try:
        v_a_agg = int(input(f"Ingrese las veces que quiera agregar un {dato} a su lista de {nombre}: "))
        for i in range(v_a_agg):
            print(f"Su lista de {nombre} actual es: {registro}")
            dato_a_agg = input(f"Ingrese el {dato} que quiera agregar: ").capitalize()
            registro.append(dato_a_agg)
        print(f"Su lista de {nombre} actualizada es: {registro}")
        return True
    except ValueError:
        print("Error: Debe ingresar un número válido.")
        return False
    finally:
        print("Operación de agregar finalizada.")

def eliminar(registro, dato, nombre):
    try:
        v_a_eliminar = int(input(f"Ingrese las veces que quiera eliminar un {dato} de su lista de {nombre}: "))
        for i in range(v_a_eliminar):
            print(f"Su lista de {nombre} actual es: {registro}")
            dato_a_eliminar = input(f"Ingrese el {dato} que quiera eliminar de la lista de {nombre}: ").capitalize()
            if dato_a_eliminar in registro:
                registro.remove(dato_a_eliminar)
            else:
                print(f"{dato_a_eliminar} no se encuentra en la lista.")
        print(f"Su lista de {nombre} actualizada es: {registro}")
        return True
    except ValueError:
        print("Error: Debe ingresar un número válido.")
        return False
    finally:
        print("Operación de eliminación finalizada.")

def buscar(registro, dato, nombre):
    try:
        v_a_buscar = int(input(f"Ingrese las veces que quiera buscar un {dato} en su lista de {nombre}: "))
        for i in range(v_a_buscar):
            dato_a_buscar = input(f"Ingrese el {dato} que quiera buscar en su lista de {nombre}: ").capitalize()
            if dato_a_buscar in registro:
                indice = registro.index(dato_a_buscar)
                print(f"Su {dato} fue encontrado en la lista de {nombre} y está en el índice {indice}.")
            else:
                print(f"Su {dato} no fue encontrado en su lista de {nombre}.")
        return True
    except ValueError:
        print("Error: Debe ingresar un número válido.")
        return False
    finally:
        print("Operación de búsqueda finalizada.")

def remplazar(registro, dato, nombre):
    try:
        v_a_remplazar = int(input(f"Ingrese las veces que quiera reemplazar un {dato} de su lista de {nombre}: "))
        for i in range(v_a_remplazar):
            dato_a_remplazar = input(f"Ingrese el {dato} que quiera buscar en su lista de {nombre}: ").capitalize()
            if dato_a_remplazar in registro:
                indice = registro.index(dato_a_remplazar)
                nuevo_dato = input(f"Ingrese el {dato} que pondrá en su lugar: ").capitalize()
                registro[indice] = nuevo_dato
            else:
                print(f"{dato_a_remplazar} no se encuentra en la lista.")
        print(f"Su lista de {nombre} actualizada es: {registro}")
        return True
    except ValueError:
        print("Error: Debe ingresar un número válido.")
        return False
    finally:
        print("Operación de reemplazo finalizada.")

def n_de_datos(registro, datos):
    try:
        n_en_n = len(registro)
        print(f"Su lista tiene {n_en_n} {datos}.")
        return True
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False
    finally:
        print("Operación de conteo finalizada.")

def marcar_completado(registro, completados, dato, nombre):
    try:
        print(f"Lista actual de {nombre}: {registro}")
        dato_completado = input(f"Ingrese el {dato} que ha completado: ").capitalize()
        if dato_completado in registro:
            completados.append(dato_completado)
            registro.remove(dato_completado)
            print(f"El {dato_completado} ha sido marcado como completado.")
        else:
            print(f"{dato_completado} no se encuentra en la lista.")
        return True
    except ValueError:
        print("Error: Debe ingresar un valor válido.")
        return False
    finally:
        print("Operación de marcar como completado finalizada.")

def ver_completados(completados, nombre):
    if completados:
        print(f"Lista de tareas completadas en {nombre}: {completados}")
    else:
        print(f"No hay tareas completadas en {nombre}.")
    return True

iniciar = input("¿Quieres iniciar el programa (Si/No)?: ").capitalize()

if iniciar == "Si":
    try:
        nombre = input("Ingrese el nombre que defina como se llama su lista: ").capitalize()
        dato = input("Ingrese el nombre que defina el elemento que guardará su lista: ").capitalize()
        
        while iniciar == "Si":
            try:
                menu = int(input(f"Ingrese la opción que quiera realizar:\n"
                                 "1) Agregar\n"
                                 "2) Eliminar\n"
                                 "3) Buscar\n"
                                 "4) Reemplazar\n"
                                 "5) Contar elementos\n"
                                 "6) Marcar como completado\n"
                                 "7) Ver completados\n"
                                 "8) Cerrar\n"
                                 "Opción: "))
                
                if menu == 1:
                    agg(registro, completados, dato, nombre)
                elif menu == 2:
                    eliminar(registro, dato, nombre)
                elif menu == 3:
                    buscar(registro, dato, nombre)
                elif menu == 4:
                    remplazar(registro, dato, nombre)
                elif menu == 5:
                    n_de_datos(registro, dato)
                elif menu == 6:
                    marcar_completado(registro, completados, dato, nombre)
                elif menu == 7:
                    ver_completados(completados, nombre)
                elif menu == 8:
                    break
                else:
                    print("Opción no válida, ingrese un número entre 1 y 8.")
            except ValueError:
                print("Error: Debe ingresar un número válido.")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        print("Programa finalizado.")
else:
    while iniciar not in ["Si", "No"]:
        print("Lo que ingresaste no es válido, ingresa 'Si' o 'No'.")
        iniciar = input("¿Quieres iniciar el programa (Si/No)?: ").capitalize()
