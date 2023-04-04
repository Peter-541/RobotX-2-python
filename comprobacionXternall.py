#Importamos las librerías necesarias de Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import pyautogui

#Configuramos las opciones del navegador
options = webdriver.ChromeOptions()
options.add_argument('--normal-page')
options.add_argument('--start-maximized')

def compobationXternall(fiscal_id,name_ss,id):
    # Inicializamos el driver de Selenium con las opciones configuradas
    driver = webdriver.Chrome(options=options)

    # Nos dirigimos al portal de Xternall
    driver.get('https://apexapi.xternall.com/ords/f?p=159:276:7997459797743::::P276_ID:'+id)
    time.sleep(3) # Esperamos un segundo para que cargue la página

    # Localizamos los elementos de la página que necesitamos interactuar
    input_folio = driver.find_element(By.XPATH,'//*[@id="P276_NUM_FOLIO"]')
    input_img = driver.find_element(By.XPATH,'//*[@id="P276_ROBO_REC_NOMINA_XML_DROPZONE"]/div[2]/span[1]')
    btn_ok = driver.find_element(By.XPATH,'//*[@id="B300968115005400343"]') 

    input_folio.send_keys(fiscal_id) 
    time.sleep(1)
    input_img.click()
    time.sleep(2) 
    #archivo = 'C:\\Users\\GTIM\\Documents\\Robots\\RobotX-2-python-main\\'+name_ss
    path = 'C:\\Users\\GTIM\\Documents\\Robots\\RobotX-2-python-main\\'+name_ss
    pyautogui.write(path)# Escribe la ruta del archivo en la ventana de subir archivos
    time.sleep(1)
    pyautogui.press('enter') # Presiona la tecla Enter para seleccionar el archivo
    time.sleep(1)
    pyautogui.press('tab') # Navega hasta el botón "Abrir"
    time.sleep(1)
    pyautogui.press('enter') # Presiona la tecla Enter para hacer clic en el botón "Abrir"
    time.sleep(1) # Espera un segundo para que se cargue la página web
    btn_ok.click()
    time.sleep(3)
    driver.close()
    driver.quit()