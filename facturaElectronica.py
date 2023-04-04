#Importamos las librerías necesarias de Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import requests
import time
import comprobacionXternall
import capchaAWS # Esta es una librería personalizada que nos permite llamar los metodos del scrip capchaAWS

#Configuramos las opciones del navegador
options = webdriver.ChromeOptions()
options.add_argument('--normal-page')
options.add_argument('--start-maximized')

# Función para consultar una factura en el portal del SAT
def consultaFactura(id,rfc_emi,rfc_rcp,fiscal_id):
    # Inicializamos el driver de Selenium con las opciones configuradas
    driver = webdriver.Chrome(options=options)

    # Nos dirigimos al portal del SAT
    # driver.execute_script("window.open('');")
    driver.get('https://verificacfdi.facturaelectronica.sat.gob.mx/')
    time.sleep(1) # Esperamos un segundo para que cargue la página
       
    # Localizamos los elementos de la página que necesitamos interactuar
    input_fiscal_ID = driver.find_element(By.ID,"ctl00_MainContent_TxtUUID")
    input_RFC_emi = driver.find_element(By.ID,"ctl00_MainContent_TxtRfcEmisor")
    input_RFC_rcp = driver.find_element(By.ID,"ctl00_MainContent_TxtRfcReceptor")
    input_imgCapcha = driver.find_element(By.ID,"ctl00_MainContent_ImgCaptcha")
    input_capcha = driver.find_element(By.ID,"ctl00_MainContent_TxtCaptchaNumbers")
    btn_verificar = driver.find_element(By.ID,"ctl00_MainContent_BtnBusqueda")
    time.sleep(1) # Esperamos dos segundos para asegurarnos de que todos los elementos hayan cargado

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
    time.sleep(1) # Esperamos un segundo
    
    # Utilizamos la funcion de la libreria que antes importamos 
    capcha = capchaAWS.capchaUpload(name_img) # Guardamos el capcha ya procesado de la imagen en forma de texto
    #print(capcha)
    #time.sleep(1)
    input_capcha.send_keys(capcha) # Introducimos el texto de la imagen
    time.sleep(2)

    try:
        error_capcha = driver.find_element(By.XPATH,'//*[@id="ctl00_MainContent_pnlErrorCaptcha"]')
        error = error_capcha.text
        
        if error_capcha:
            print(error)
            driver.close()
            driver.quit()
        else:
            btn_verificar.click() #Enviamos los datos para consultar
            time.sleep(1)
            name_ss = id+'.png'
            # Encontrar un elemento en la página para activar el foco
            elem = driver.find_element(By.TAG_NAME,"body")
            elem.click()
            # Crear objeto de la clase ActionChains
            actions = ActionChains(driver)
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(1)
            driver.save_screenshot(name_ss) #Tomamos una captura 
            time.sleep(1)
            driver.close()
            driver.quit() #Cerramos la pagina
            comprobacionXternall.compobationXternall(fiscal_id,name_ss,id)   
       
    except NoSuchElementException:
        btn_verificar.click() #Enviamos los datos para consultar
        time.sleep(1)
        name_ss = id+'.png'
        # Encontrar un elemento en la página para activar el foco
        elem = driver.find_element(By.TAG_NAME,"body")
        elem.click()
        # Crear objeto de la clase ActionChains
        actions = ActionChains(driver)
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1)
        driver.save_screenshot(name_ss) #Tomamos una captura 
        time.sleep(1)
        driver.close() #Cerramos la pagina
        driver.quit()
        comprobacionXternall.compobationXternall(fiscal_id,name_ss,id)
        time.sleep(1)    
