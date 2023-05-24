import os
import json

"""
    menu()
    Muestra por consola las opciones y pide al usuario que opcion usar
    Las opciones ejecutan funciones
    no retorna nada 
"""
def menu ():
    flagCargar = 0
    listaDeInsumos = []
    opcion = 0
    while opcion != -1:
        print("\
            1. Cargar datos desde archivo\n\
            2. Listar cantidad por marca\n\
            3. Listar insumos por marca\n\
            4. Buscar insumo por característica\n\
            5. Listar insumos ordenados\n\
            6. Realizar compras\n\
            7. Guardar en formato JSON\n\
            8. Leer desde formato JSON\n\
            9. Actualizar precios\n\
            10. Salir del programa")
        opcion = int(input("ingresar opcion : "))
        if (opcion >= 1 and opcion <= 10):
            os.system("cls")
            match opcion:
                case 1:
                    if flagCargar == 0:
                        listaDeInsumos = leerCSV()
                        print("Se cargo el archivo correctamente")
                        flagCargar = 1
                    else:
                        print("ya fue cargada el archivo")
                case 2:
                    cantidaMarca(listaDeInsumos)
                case 3:
                    listarInsumosMarca(listaDeInsumos)
                case 4:
                    buscarInsumosCaracteristicas(listaDeInsumos)
                case 5:
                    listarInsumosOrdenado(listaDeInsumos)
                case 6:
                    compra(listaDeInsumos)
                case 7:
                    guardarAlimentoJSON(listaDeInsumos)
                case 8:
                    cargarAlimentoJSON()
                case 9:
                    cargarAumento(listaDeInsumos)
                case 10:
                    break
        input("Presione Enter para continuar...")
        os.system("cls")

"""
    leerCSV()
    lee el archivo CSV linea por linea creando diccionarios de cada una y los guarda en una lista
    no retorna nada
"""
def leerCSV():
    listaInsumos = []
    productosDatos = []
    llave = []
    with open("insumos.csv", "r", encoding="utf-8") as archivo:
        productosInfo = {}
        llave = archivo.readline().replace("\n","").split(",")
        for linea in archivo:
            productosDatos = linea.replace("\n ","").split(",")
            productosInfo = {
                llave[0]:productosDatos[0],
                llave[1]:productosDatos[1],
                llave[2]:productosDatos[2],
                llave[3]:productosDatos[3],
                llave[4]:productosDatos[4]
            }
            listaInsumos.append(productosInfo)
    return listaInsumos

"""
    listMarca(listaInsumos)
    Ingresa por parametro la lista cargada por el CSV
    Crea un lista de todas la marcas (Con repetidos)
    retorna la lista de marcas
"""
def listMarca(listaInsumos):
    auxMarca = []
    for marca in listaInsumos:
        auxMarca.append(marca["MARCA"])
    return auxMarca

"""
    cantidaMarca(listaInsumos)
    Ingresa por parametro la lista cargada por el CSV
    esta funcion muestra usa set para borrar los repetidos de listaMarca(listaInsumos)
    y usa el tuple para buscar la cantidad de veces que se repite las marcas para dar con la cantidad de insumos por marca
    no retorna nada
"""
def cantidaMarca(listaInsumos):
    auxMarca = listMarca(listaInsumos)
    tMarca = tuple(auxMarca)
    sMarca = set(auxMarca)
    for marca in sMarca:
        print(marca + " tiene " + str(tMarca.count(marca)) + " cantidad de insumos")

"""
    listarInsumosMarca(listaInsumos)
    ingresa por paraametro la lista cargada por el CSV
    crear una lista set de marca para poder listar los insumos de cada marca por separado
"""
def listarInsumosMarca(listaInsumos):
    sMarca = set(listMarca(listaInsumos))
    for marcaS in sMarca:
        print(marcaS)
        for insumos in listaInsumos:
            if marcaS == insumos["MARCA"]:
                print("  _"+ insumos["NOMBRE"] + " Precio : " + insumos["PRECIO"])

"""
   buscarInsumosCaracteristicas(listaInsumos)
   ingresa por parametro la lista cargada por el CSV
   pide a usuario la caracteristica que busca
   uso una lista auxiliar texto = [] para comprobar si la caracteristica especifica esta en el insumo
   no retorna nada
"""
def buscarInsumosCaracteristicas(listaInsumos):
    texto = []
    caracteristica = input("Ingresar caracteristica para buscar \n").lower()
    for insumo in listaInsumos:
        texto = (str(insumo["CARACTERISTICAS"]).lower()).replace("\n", "").split("~")
        for validando in texto:
            if validando == caracteristica:
                print(" _" + insumo["MARCA"] + " " + insumo["NOMBRE"] )
        texto.clear

"""
    listarInsumosOrdenado(listaInsumos)
    ingresa por parametro la lista cargada por el CSV
    se crea una copia de la lista para no interferir con la base
    se usa el metodo burbuja para ordenar de la A a la Z por Marca
    si las Marcas son iguales se ordena por precio descendente
    se muestra por consola y las caracteristicas solo se muestra la primera
    no retorna nada
"""
def listarInsumosOrdenado(listaInsumos):
    listaInsumosCopia = listaInsumos
    aux = None
    tam = len(listaInsumosCopia)
    for i in range(tam-1):
       for j in range(i + 1, tam):
            if(str(listaInsumosCopia[i]["MARCA"]) > str(listaInsumosCopia[j]["MARCA"])):
                aux = listaInsumosCopia[i]
                listaInsumosCopia[i] = listaInsumosCopia[j]
                listaInsumosCopia[j] = aux
            elif str(listaInsumosCopia[i]["MARCA"]) == str(listaInsumosCopia[j]["MARCA"]) and (str(listaInsumosCopia[i]["PRECIO"]).replace("$","") < str(listaInsumosCopia[j]["PRECIO"]).replace("$","")):
                aux = listaInsumosCopia[i]
                listaInsumosCopia[i] = listaInsumosCopia[j]
                listaInsumosCopia[j] = aux
    for insumoCopia in listaInsumosCopia:
        print(str(insumoCopia["ID"]) + " " + str(insumoCopia["NOMBRE"]) + " " + str(insumoCopia["MARCA"]) + str(insumoCopia["PRECIO"]) + " " + str(insumoCopia["CARACTERISTICAS"]).split("~")[0])

"""
    compra(listaInsumos)
    ingresa por parametro la lista cargada por el CSV
    llama a la funcion listarProductosMarca(listaInsumos, usuarioMarca) para mostrar los productos de la marca ingresada por el usuario
    despues pide al usuario ingresar el id del producto, se busca en la lista general y se pide la cantidad a comprar
    cuando el usuario finaliza la compra de manda a factura(compra, cantidad) para mostrar en un txt
    no retorna nada 
"""
def compra(listaInsumos):
    seguir = 1
    compra = 0
    cantidad = []
    compras = []
    usuarioMarca = None
    while seguir != 0:
        usuarioMarca = input("Ingresar marca que ").lower()
        listarProductosMarca(listaInsumos, usuarioMarca)
        compra = input("Ingresa la id del producto que desea comprar")
        for insumosC in listaInsumos:
            if compra == insumosC["ID"]:
                cantidad.append(input("Ingresar cantidad"))
                compras.append(insumosC) 
        seguir = int(input("ingresar 0 si quiere finalizar la compra o ingrese 1 para continuar"))
    factura(compras, cantidad)

"""
    factura(compra, cantidad)
    se recibe por parametro las compras ingresadas por el usuario y la cantidad de ellas
    se hace la cuenta del subtotal y se acumula los subtotal para sacar el total
    despues se escribe en el txt la factura 
    no retorna nada
"""
def factura(compra, cantidad):
    archivo = open("factura.txt","w")
    subtotal = 0
    total = 0
    archivo.write("cantidad     Producto       subtotal\n")
    for x in range(len(compra)):
        texto = str(compra[x]["PRECIO"]).replace("$","") 
        precioInt = int(round(float(texto)))
        subtotal = precioInt * int(cantidad[x])
        total = total + subtotal
        archivo.write(str(cantidad[x]) + "   " + str(compra[x]["NOMBRE"]) + "   " + str(subtotal) + "\n")
    archivo.write("Total "+ str(total))
    archivo.close()

"""
    listarProductoMarca(listaInsumos, usuarioMarca)
    ingresa por parametra la lista cargada por el CSV
    ingresa por parametro la marca ingresada por el usuario
    La funcion busca en la lista general todas las marcas que coincidan con la que ingreso el usuario
    muestra por consola la id y nombre de los productos
    retorna una lista con los productos de la marca ingresada por el usuario
"""
def listarProductosMarca(listaInsumos, usuarioMarca):
    listMarcaProducto = []
    for insumo in listaInsumos:
            if str(insumo["MARCA"]).lower() == usuarioMarca:
                listMarcaProducto.append(insumo)
                print("ID: " + insumo["ID"]+ " " +insumo["NOMBRE"])
    return listMarcaProducto

"""
    guardarAlimentoJson(listaInsumo)
    se ingresa por parametro la lista cargada por el CSV
    se llama a la funcion filtrarAlimento(listaInsumos) para recibir una lista solo con los productos que tengan alimento en el nombre
    se escribe todo en un archivo .json
    no retorna nada
"""
def guardarAlimentoJSON(listaInsumos):
    listaAlimentos = filtrarAlimento(listaInsumos)
    with open("alimentos.json","w") as archivo:
        json.dump(listaAlimentos, archivo)

"""
    filtrarAlimento(listaInsumos)
    ingresa por parametro la lista cargada por el CSV
    recorre todo la lista para comprobar sin en nombre contienen la palabrea alimento
    y se agrega a una lista aparte todos los insumos alimento
    retorna la lista que solo son alimentos
"""
def filtrarAlimento(listaInsumos):
    listaAlimentos = []
    auxtext = []
    for insumos in listaInsumos:
        auxtext = str(insumos["NOMBRE"]).lower().split(" ")
        for text in auxtext:
            if text == "alimento":
                listaAlimentos.append(insumos)
    return listaAlimentos

"""
    cargarAlimentoJson()
    lee el archivo .json de alimentos y los muestra por consola
    no retorna nada
"""
def cargarAlimentoJSON():
    with open("alimentos.json", "r") as archivo:
        listaAlimentos = json.load(archivo)
    for alimento in listaAlimentos:
        print(alimento)    

"""
    aumento(numero)
    esta funcion recibe por parametro el precio
    aumenta el precio un 8.4%
    retornando el aumento
"""
def aumento(numero):
    return numero * 1.084

"""
    preciosInsumo(listaInsumos)
    se ingresa por parametro la lista cargada por el CSV
    se crea una lista auxiliar en la qque se guarda todos los precios del CSV 
    retorna el map aplicando la funcion de aumento del 8.4% de la lista auxiliar de precios
"""
def preciosInsumo(listaInsumos):
    preciosF = []
    for precio in listaInsumos:
        preciosF.append(float(str(precio["PRECIO"]).replace("$", "")))
    return map(aumento, preciosF)

"""
    aplicarAumento(listaInsumos, listaAumento)
    se ingresa por parametro la la lista cargada por el CSV
    se ingresa por parametro la lista con los aumentos
    La funcion recorre la lista general del CSV y le aplica el aumento
    retorna la lista modificada con los precios
"""
def aplicarAumento(listaInsumos, listaAumentos):
    if len(listaInsumos) == len(listaAumentos):
        for x in range(len(listaInsumos)):
            listaInsumos[x]["PRECIO"] = "$"+str(round(float(listaAumentos[x]),2))
    return listaInsumos
"""
    cargarAumento(listaInsumos)
    ingresa por parametro la lista cargada por el CSV
    pide la lista con los aumentos y despues se aplica los aumentos en la lista cargada por el CSV
    se carga todo la lista al CSV de insumos.csv con todos los cambios(el aumento)
    no retorna nada
"""
def cargarAumento(listaInsumos):
    listaAumento = list(preciosInsumo(listaInsumos))
    listaAumentado = aplicarAumento(listaInsumos , listaAumento)
    with open("insumos.csv", "w", encoding="utf-8") as archivo:
        archivo.write("ID,NOMBRE,MARCA,PRECIO,CARACTERISTICAS\n")
        for aumentos in listaAumentado:
            archivo.write(str(aumentos["ID"])+ "," + str(aumentos["NOMBRE"]) + "," + str(aumentos["MARCA"])+ "," + str(aumentos["PRECIO"])+ "," + str(aumentos["CARACTERISTICAS"]))
   