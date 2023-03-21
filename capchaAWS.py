#Importamos las librerías necesarias de Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import subprocess

#Configuramos las opciones del navegador
options = webdriver.ChromeOptions()
options.add_argument('--normal-page')
options.add_argument('--start-maximized')
#options.add_argument("--user-data-dir=chrome-data")
#options.add_argument("--profile-directory=Default")

#Creamos variables con las credenciales de acceso al AWS
USSER = '*******'
PASS = '*******'
#name_img = 'capt1401366'

# Creamos una función que realiza el proceso de subir una imagen y obtener el texto del captcha
def capchaUpload(name_img):
    # Creamos una instancia del navegador Chrome con las opciones previamente configuradas
    driver = webdriver.Chrome(options=options)

    # Accedemos a la página de AWS Rekognition Text Detection
    driver.get('https://us-east-2.console.aws.amazon.com/rekognition/home?region=us-east-2#/text-detection')
    time.sleep(3)
    
    # Verificamos si ya inició sesión en AWS a través de un try/except
    try:
            #Si aún no se ha iniciado sesión, se muestra la pantalla de Logeo.
            aws_Session = driver.find_element(By.XPATH,'//*[@id="signin_head"]')
            session = aws_Session.text

            # Se ingresan las credenciales y se hace clic en el botón de inicio de sesión
            if session == 'Iniciar Session' or session == 'Sign in':
                input_username = driver.find_element(By.XPATH,'//*[@id="resolving_input"]')
                btn_next = driver.find_element(By.XPATH,'//*[@id="next_button"]')
                time.sleep(2)

                input_username.send_keys(USSER)
                btn_next.click()
                time.sleep(2)

                input_password = driver.find_element(By.XPATH,'//*[@id="password"]')
                btn_login = driver.find_element(By.XPATH,'//*[@id="signin_button"]')

                input_password.send_keys(PASS)
                time.sleep(3)
                btn_login.click()
                time.sleep(3)
                
                # Una vez iniciada la sesión, se hace busca el elemento del botón de carga de imagen
                btn_upload = driver.find_element(By.XPATH,'//*[@id="app"]/div/div/div/div/div/main/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/button')
                
                # Hacemos scroll para mostrar el botón de carga de imagen y luego hacemos clic en él
                for i in range(2):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)

                btn_upload.click()
                #Falta codigo para cargar la imagen en el aws
                time.sleep(5)

                # Obtenemos el texto del captcha
                out_text = driver.find_element(By.XPATH,'//*[@id="6-1678483709494-6248"]/div/div[1]/h5')
                capcha =  out_text.text
                print(capcha)
                driver.close()
                return capcha

    except NoSuchElementException:
                # Una vez iniciada la sesión, se hace busca el elemento del botón de carga de imagen
                btn_upload = driver.find_element(By.XPATH,'//*[@id="app"]/div/div/div/div/div/main/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/button')
                
                # Hacemos scroll para mostrar el botón de carga de imagen y luego hacemos clic en él
                for i in range(2):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)

                btn_upload.click()
                #Falta codigo para cargar la imagen en el aws
                time.sleep(5)

                # Obtenemos el texto del captcha
                out_text = driver.find_element(By.XPATH,'//*[@id="6-1678483709494-6248"]/div/div[1]/h5')
                capcha =  out_text.text
                print(capcha)
                driver.close()
                return capcha
    
time.sleep(30)