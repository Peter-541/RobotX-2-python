#Importamos las librerías necesarias de Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import pyautogui

#Configuramos las opciones del navegador
options = webdriver.ChromeOptions()
options.add_argument('--normal-page')
options.add_argument('--start-maximized')
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--disable-features=VizDisplayCompositor")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-web-security")
options.add_argument("--disable-default-apps")
options.add_argument("--disable-popup-blocking")
options.add_argument("--enable-logging")
options.add_argument("--log-level=0")
options.add_argument("--single-process")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--user-data-dir=/tmp/ChromeUserData")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

#Creamos variables con las credenciales de acceso al AWS
USSER ='carlos.rabadan@gmail.com'
PASS = 'Rabax9858781108$#$'

# Creamos una función que realiza el proceso de subir una imagen y obtener el texto del captcha
def capchaUpload(name_img):
    # Creamos una instancia del navegador Chrome con las opciones previamente configuradas
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": True})
    ventanas = driver.window_handles

        # Accedemos a la página de AWS Rekognition Text Detection
    driver.get('https://us-east-2.console.aws.amazon.com/rekognition/home?region=us-east-2#/text-detection')
    time.sleep(3)
            
        # Verificamos si ya inició sesión en AWS a través de un try/except
    try:
        #Si aún no se ha iniciado sesión, se muestra la pantalla de Logeo.
        aws_Session = driver.find_element(By.XPATH,'//*[@id="signin_head"]')
        session = aws_Session.text
        print(session)

        # Se ingresan las credenciales y se hace clic en el botón de inicio de sesión
        if session == 'Iniciar sesión' or session == 'Sign in':
            print('Se inicio sesion en AWS')
            input_username = driver.find_element(By.XPATH,'//*[@id="resolving_input"]')
            btn_next = driver.find_element(By.XPATH,'//*[@id="next_button"]')
            time.sleep(1)

            input_username.send_keys(USSER)
            btn_next.click()
            time.sleep(1)

            input_password = driver.find_element(By.XPATH,'//*[@id="password"]')
            btn_login = driver.find_element(By.XPATH,'//*[@id="signin_button"]')

            input_password.send_keys(PASS)
            time.sleep(3)
            btn_login.click()
            time.sleep(2)
                        
            # Una vez iniciada la sesión, se hace busca el elemento del botón de carga de imagen
            btn_upload = driver.find_element(By.XPATH,'//*[@id="app"]/div/div/div/div/div/main/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/button')

            # Hacemos scroll para mostrar el botón de carga de imagen y luego hacemos clic en él
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            btn_upload.click()
            time.sleep(2) # Espera un segundo para que aparezca la ventana de subir archivos
            #archivo = 'C:\\Users\\Omar\\Documents\\Projects\\Automatization-python\\'+name_img
            archivo1 = 'C:\\Users\\Omar\\Documents\\Projects\\Automatization-python\\'+name_img
            pyautogui.write(archivo1) # Escribe la ruta del archivo en la ventana de subir archivos
            time.sleep(1)
            pyautogui.press('enter') # Presiona la tecla Enter para seleccionar el archivo
            time.sleep(1)
            pyautogui.press('tab') # Navega hasta el botón "Abrir"
            time.sleep(1)
            pyautogui.press('enter') # Presiona la tecla Enter para hacer clic en el botón "Abrir"
            time.sleep(2)
                            
            # Obtenemos el texto del captcha
            out_text = driver.find_element(By.XPATH,'//*[@id="app"]/div/div/div/div/div/main/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/div[1]/div[2]')
            capchas = out_text.find_elements(By.TAG_NAME, "h5")

            for capcha in capchas:
                capcha_text = capcha.text

            #print(capcha_text)
            driver.close()
            return capcha_text
        else:
            print('No se inicio sesion en AWS')
            driver.close()
            driver.quit()
                            
    except NoSuchElementException:    
        # Una vez iniciada la sesión, se hace busca el elemento del botón de carga de imagen
        btn_upload = driver.find_element(By.XPATH,'//*[@id="app"]/div/div/div/div/div/main/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/button')

        # Hacemos scroll para mostrar el botón de carga de imagen y luego hacemos clic en él
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
                   
        btn_upload.click()
        time.sleep(2) # Espera un segundo para que aparezca la ventana de subir archivos
        archivo = 'C:\\Users\\GTIM\\Documents\\Robots\\RobotX-2-python-main\\'+name_img
        pyautogui.write(archivo) # Escribe la ruta del archivo en la ventana de subir archivos
        time.sleep(1)
        pyautogui.press('enter') # Presiona la tecla Enter para seleccionar el archivo
        time.sleep(1)
        pyautogui.press('tab') # Navega hasta el botón "Abrir"
        time.sleep(1)
        pyautogui.press('enter') # Presiona la tecla Enter para hacer clic en el botón "Abrir"
        time.sleep(3)
                       
        # Obtenemos el texto del captcha
        out_text = driver.find_element(By.XPATH,'//*[@id="app"]/div/div/div/div/div/main/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/div[1]/div[2]')
        capchas = out_text.find_elements(By.TAG_NAME, "h5")

        for capcha in capchas:
            capcha_text = capcha.text

        #print(capcha_text)
        driver.close()
        driver.quit()
        return capcha_text