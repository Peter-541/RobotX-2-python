#Importamos las librerías necesarias de Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
import time
import comprobacionXternall
import capchaAWS # Esta es una librería personalizada que nos permite llamar los metodos del scrip capchaAWS

#Configuramos las opciones del navegador
options = webdriver.ChromeOptions()
options.add_argument('--normal-page')
options.add_argument('--start-maximized')
#options.add_argument("--user-data-dir=chrome-data")
#options.add_argument("--profile-directory=Default")

# Función para consultar una factura en el portal del SAT
def consultaFactura(id,rfc_emi,rfc_rcp,fiscal_id):
    # Inicializamos el driver de Selenium con las opciones configuradas
    driver = webdriver.Chrome(options=options)

    # Nos dirigimos al portal del SAT
    driver.get('https://verificacfdi.facturaelectronica.sat.gob.mx/')
    time.sleep(1) # Esperamos un segundo para que cargue la página

     # Localizamos los elementos de la página que necesitamos interactuar
    input_fiscal_ID = driver.find_element(By.ID,"ctl00_MainContent_TxtUUID")
    input_RFC_emi = driver.find_element(By.ID,"ctl00_MainContent_TxtRfcEmisor")
    input_RFC_rcp = driver.find_element(By.ID,"ctl00_MainContent_TxtRfcReceptor")
    input_imgCapcha = driver.find_element(By.ID,"ctl00_MainContent_ImgCaptcha") 
    input_capcha = driver.find_element(By.ID,"ctl00_MainContent_TxtCaptchaNumbers")
    btn_verificar = driver.find_element(By.ID,"ctl00_MainContent_BtnBusqueda")
    time.sleep(2) # Esperamos dos segundos para asegurarnos de que todos los elementos hayan cargado

     # Introducimos la información de la factura en los campos correspondientes
    input_fiscal_ID.click() # Hacemos clic en el campo de ID fiscal
    input_fiscal_ID.send_keys(fiscal_id) # Introducimos el ID fiscal
    time.sleep(1) # Esperamos un segundo

    input_RFC_emi.send_keys(rfc_emi) # Introducimos el RFC del emisor
    input_RFC_rcp.send_keys(rfc_rcp) # Introducimos el RFC del receptor
    link = input_imgCapcha.get_attribute('src') # Obtenemos la URL de la imagen CAPTCHA
    img_capcha = requests.get(link) # Descargamos la imagen CAPTCHA

    if img_capcha.status_code == 200: # Verificamos que exista la imagen 
        #print(link)
        name_img = 'capt'+str(id)+'.png' # Creamos un nombre de archivo para la imagen CAPTCHA
        with open(name_img, 'wb') as img: 
            img.write(img_capcha.content)  # Escribimos la imagen CAPTCHA en el archivo correspondiente
            img.close

    time.sleep(2) # Esperamos dos segundos
    
    # Utilizamos la funcion de la libreria que antes importamos 
    capcha = capchaAWS.capchaUpload(name_img) # Guardamos el capcha ya procesado de la imagen en forma de texto
    input_capcha.send_keys(capcha) # Introducimos el texto de la imagen
    time.sleep(1)

    driver.execute_script("document.body.style.zoom='90%'") #Mediante un scrip disminuimos en 90% el zoom de la pagina
    time.sleep(1.5)

    name_ss = id+'.png' 
    driver.save_screenshot(name_ss) #Tomamos una captura 
    btn_verificar.submit() #Enviamos los datos para consultar
    time.sleep(2)
    driver.close() #Cerramos la pagina

    comprobacionXternall.compobationXternall(fiscal_id,name_ss)
    time.sleep(2)

    
    

