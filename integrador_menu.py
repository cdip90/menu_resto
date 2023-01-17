from time  import asctime
import sqlite3
import os

#######################################

borrado = "cls"
os_name = os.name
if os_name == "posix":
    borrado = "clear"

######## Defino funciones a utilizar #################

def ingreso_encargado():
    os.system(borrado)
    print(f'Bienvenido a Hamburguesas IT')
    encargado = input(f'Ingrese su nombre encargad@: ')  
    print("")
    print("Hamburgesas IT")
    print(f'Encargad@: {encargado}')
    print(f'Recuerda siempre hay que recibir al cliente con una sonrisa =D\n')
    return encargado


def menu():
    while True:
        try:
            opcion = int(input(f'1 - Ingrese nuevo pedido\n2 - Cambio de turno\n3 - Apagar sistema\n'))
            while 1 > opcion > 3:
                print('Opción no válida')
                opcion = int(input(f'1 - Ingrese nuevo pedido\n2 - Cambio de turno\n3 - Apagar sistema\n'))
            break
        except ValueError:
            print('Error al ingresar opción')
            opcion = int(input(f'1 - Ingrese nuevo pedido\n2 - Cambio de turno\n3 - Apagar \n'))
        
    return opcion

def nuevo_pedido():
    cliente = input('Ingrese nombre cliente: ').capitalize()  
    while True:
        try:
            combo_s = int(input('Ingrese cantidad Combo S: '))
            break
        except ValueError:
            print('Error al ingresar la cantidad')

    while True:
        try:
            combo_d = int(input('Ingrese cantidad Combo D: '))
            break
        except ValueError:
            print('Error al ingresar la cantidad')

    while True:
        try:
            combo_t = int(input('Ingrese cantidad Combo T: '))
            break
        except ValueError:
            print('Error al ingresar la cantidad')

    while True:
        try:
            flurby = int(input('Ingrese cantidad Flurby: '))
            break
        except ValueError:
            print('Error al ingresar la cantidad')
    
    total = (combo_s*5) + (combo_d*6) +(combo_t*7) + (flurby*2)
    print(f'Total ${total}')

    while True:
        try:
            pago = int(input('Abona con: '))
            break
        except ValueError:
            print('Error al ingresar el valor')
    
    vuelto = pago - total

    return(cliente,combo_s,combo_d,combo_t,flurby,total,pago,vuelto)

def registro_ventas(cliente,combo_s,combo_d,combo_t,flurby,total):

    fecha = asctime()
    conn = sqlite3.connect("registro_ventas.sqlite")
    cursor = conn.cursor()
    query_agregar = ("insert into ventas Values (?,?,?,?,?,?)")
    try:
        cursor.execute(query_agregar,(cliente,combo_s,combo_d,combo_t,flurby,total))
        conn.commit()
        conn.close()

    except sqlite3.OperationalError:
         cursor.execute("CREATE TABLE ventas(cliente Text,combo_s int ,combo_d int ,combo_t int,flurby int ,total int);")
         cursor.execute(query_agregar,(cliente,combo_s,combo_d,combo_t,flurby,total))
         conn.commit()
         conn.close()


def registro_encargado(encargado,tipo,total=None):

    fecha = asctime()
    conn = sqlite3.connect("registro_encargados.sqlite")
    cursor = conn.cursor()
    query_ingreso = ("insert into encargados Values (?,?,?,?)")
    query_egreso = ("insert into encargados Values (?,?,?,?)")


    if tipo.upper() == 'IN':
        try:
            cursor.execute(query_ingreso,(tipo,fecha,encargado,total))
            conn.commit()
            conn.close()

        except sqlite3.OperationalError:
            cursor.execute("CREATE TABLE encargados (tipo Text, fecha Text, encargado Text, total int);")
            cursor.execute(query_ingreso,(tipo,fecha,encargado,total))
            conn.commit()
            conn.close()
        
    else:
        cursor.execute(query_egreso,(tipo,fecha,encargado,total))
        conn.commit()
        conn.close()



            

###################### Main ###################################


os.system(borrado)
encargado=ingreso_encargado()
registro_encargado(encargado,"IN")

os.system(borrado)
opcion=menu()
total_turno = 0

while True:
    if opcion == 1:
        os.system(borrado)
        (cliente,combo_s,combo_d,combo_t,flurby,total,pago,vuelto) = nuevo_pedido()
        total_turno += total
        os.system(borrado)
        print(f'Cliente: {cliente}')
        print(f'Cantidad de combo S: {combo_s}')
        print(f'Cantidad de combo D: {combo_d}')
        print(f'Cantidad de combo T: {combo_t}')
        print(f'Cantidad de Flurby: {flurby}')
        print(f'Total: ${total}')
        print(f'Abona con: ${pago}')
        print(f'vuelto: ${vuelto}\n')

        confirmacion = input(f'¿Confirma pedido? Y/N\n')
        while True:
            if confirmacion.upper() == 'Y' or confirmacion.upper() == 'N':
                break
            else:
                os.system(borrado)
                print('Opcion no valida')
                confirmacion = input(f'¿Confirma pedido? Y/N\n')
        if confirmacion.upper() == 'Y':
            registro_ventas(cliente,combo_s,combo_d,combo_t,flurby,total)
            os.system(borrado)
            opcion = menu()
        else:
            os.system(borrado)
            opcion = menu()

    elif opcion == 2:
        registro_encargado(encargado,"OUT",total_turno)
        total_turno = 0
        encargado=ingreso_encargado()
        registro_encargado(encargado,"IN")
        opcion = menu()
    else:
        registro_encargado(encargado,"OUT",total_turno)
        os.system(borrado)
        break

print("Adios")
exit