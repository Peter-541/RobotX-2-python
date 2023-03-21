#Importamos las librerías necesarias de Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

#Configuramos las opciones del navegador
options = webdriver.ChromeOptions()
options.add_argument('--normal-page')
options.add_argument('--start-maximized')
#options.add_argument("--user-data-dir=chrome-data")
#options.add_argument("--profile-directory=Default")

def compobationXternall(fiscal_id,):
    # Inicializamos el driver de Selenium con las opciones configuradas
    driver = webdriver.Chrome(options=options)

    # Nos dirigimos al portal de Xternall
    driver.get('https://apexapi.xternall.com/ords/f?p=159:276:7997459797743::::P276_ID:&tz=-6:00')
    time.sleep(1) # Esperamos un segundo para que cargue la página

    # Localizamos los elementos de la página que necesitamos interactuar
    input_folio = driver.find_element(By.XPATH,'//*[@id="P276_NUM_FOLIO"]')
    input_img = driver.find_element(By.XPATH,'//*[@id="P276_ROBO_REC_NOMINA_XML_DROPZONE"]/div[2]/span[1]')
    btn_ok = driver.find_element(By.XPATH,'//*[@id="B300968115005400343"]')

    input_folio.send_keys(fiscal_id) 
    input_img.click() 
        #Falta codigo para cargar la imagen en el Xternall
    time.sleep(1.5)

    btn_ok.click()
    driver.close()