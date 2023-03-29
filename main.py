#APi link XTERNALL
# https://apexapi.xternall.com/ords/f?p=159:252:0:::252:P252_INICIO,P252_FIN:51,60
#APi link XTERNALL RobotX-9
# https://apexapi.xternall.com/ords/f?p=159:252:0:::252:P252_INICIO,P252_FIN:1,10

#PAGE URL Consulta del SAT
# https://verificacfdi.facturaelectronica.sat.gob.mx/

#PAGE URL AWS
#https://us-east-2.console.aws.amazon.com/rekognition/home?region=us-east-2#/text-detection

#PAGE XTERNAL COMPROBATION
# https://apexapi.xternall.com/ords/f?p=159:276:::::P276_ID:

#Importamos las librerías necesarias de Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import facturaElectronica # Esta es una librería personalizada que nos permite llamar los metodos del scrip factuarElectronica

# Especificamos la ruta donde se encuentra el driver de Chrome
PATH = "C:\\Users\\Omar\\Documents\\Projects\\Automatization-python\\chromedriver"

# Crea una instancia del WebDriver de Chrome
options = webdriver.ChromeOptions()
options.add_argument('--normal-page')
options.add_argument('--start-maximized')
#options.add_argument("--user-data-dir=chrome-data")
#options.add_argument("--profile-directory=Default")

# Inicializamos el WebDriver de Chrome
driver = webdriver.Chrome(options=options)

# Iniciamos un ciclo infinito
while 1 == 1:
    # Accedemos al api para consultar los datos 
    driver.get('https://apexapi.xternall.com/ords/f?p=159:252:0:::252:P252_INICIO,P252_FIN:1,10')
    time.sleep(3) #Espera 3 seg mientras carga la página 
    
    i = 1 #Creamos un acumulador 

    # Verificamos que exita una tabla con datos a travéz de un try/except
    try:
        # Buscamos una tabla en la página web usando XPath
        table = driver.find_element(By.XPATH, '//*[@id="803996574452225403_orig"]') 
        data = []
        # Obtenemos los datos de la tabla y los almacenamos en una lista
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = []
            for cell in cells:
                row_data.append(cell.text)
            data.append(row_data)
            #print(row_data)
            
        # Para cada fila de la tabla, obtenemos ciertos datos y los usamos para llamar el método consultaFactura 
        for row in data:
            if i < 11:
                id = data[i][1]
                rfc_emi = data[i][2]
                rfc_rcp = data[i][3]
                fiscal_id = data[i][4]
                i = i + 1
            #print('Fila:'+str(i-1))
            #print(id, rfc_emi, rfc_rcp, fiscal_id)
            try:
                facturaElectronica.consultaFactura(id,rfc_emi,rfc_rcp,fiscal_id)
            except Exception:
                # guardar la ventana actual
                main_window = driver.current_window_handle
                # obtener todos los identificadores de ventana
                all_windows = driver.window_handles
                # cerrar todas las ventanas excepto la actual
                for window in all_windows:
                    if window != main_window:
                        driver.switch_to.window(window)
                        driver.close()
                # cambiar el enfoque de la ventana de vuelta a la ventana principal
                driver.switch_to.window(main_window)
                facturaElectronica.consultaFactura(id,rfc_emi,rfc_rcp,fiscal_id)

        time.sleep(3)
        driver.close() # Cerramos la pagina web
    except NoSuchElementException:
        #En caso de nos existir una tabla con datos se refresca la pagina hasta que se encuentren nuevamente los datos
        time.sleep(5)
        driver.refresh()