import pytest 
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



@pytest.fixture(scope="module") #con module para dejar abierta la sesión hasta el final de los tests
def driver():
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    
    driver.implicitly_wait(10)
    yield driver
# luego para que se cierre:
    driver.quit()
    
    
# Primer test: AUTOMATIZACION DE LOGIN EXITOSO
# navegar al login
# aplicar las credenciales
# validar un login exitoso verificando que se haya redirigido a la página de inventario

def test_01_login(driver):
    driver.get("https://www.saucedemo.com/") #para abrir el navegador, paso la url
    driver.find_element(By.ID, "user-name").send_keys("standard_user") 
    driver.find_element(By.ID, "password").send_keys("secret_sauce")    
    driver.find_element(By.ID, "login-button").click()
    
    # proporciona la url en la que me encuentro. Con esto verifico si inventory.html está en la current url   
    assert "/inventory.html" in driver.current_url , "ERROR: No se redirigió a /inventory.html" 
    
        
def test_02_verificar_inventario(driver):
    page_title = driver.title
    section_title = driver.find_element(By.CLASS_NAME, "title").text
    
    assert page_title == "Swag Labs" , f'ERROR: Título de ventana esperado "Swag Labs", Obtenido (page_title)'
    assert section_title == "Products" , f'ERROR: Título de seccion esperado "Products", Obtenido (section_title)'
    
    
#comprobar que haya un producto visible en la página
def test_03_producto_visible(driver):
    inventory_item = driver.find_elements(By.CLASS_NAME, 'inventory_item')
    
    assert len(inventory_item) > 0, f'ERROR: No se encontraron productos visibles' # espero que la lista de productos visibles tenga al menos 1 (mayor a cero)
    

# tomar un producto de la lista y verificar si existe ese nombre
def test_04_producto(driver):
    # Busco el primer elemento de inventario disponible en la página
    primer_producto = driver.find_element(By.CLASS_NAME, "inventory_item")
    
    # Dentro de ese producto, busco el elemento que contiene el texto del nombre
    nombre_producto = primer_producto.find_element(By.CLASS_NAME, "inventory_item_name").text
    
    # Verifico que el nombre sea el esperado (el primero de la lista en Saucedemo)
    assert nombre_producto == "Sauce Labs Backpack", f"ERROR: El nombre del producto obtenido fue '{nombre_producto}'"
       
    
# validación de la existencia/visibilidad de elementos importantes: Menú, Filtro    
def test_05_valida_interfaz(driver):
    menu_button = driver.find_element(By.ID, "react-burger-menu-btn")
    filtro = driver.find_element(By.CLASS_NAME, "product_sort_container")
    
    assert filtro.is_displayed() , f'ERROR: Filtro no está visible'
    assert menu_button.is_displayed() , f'ERROR: Menu no esta visible'
    
# Interacción con productos  -> añadir un producto al carrito:
def test_06_añadir_producto_carrito(driver):
    first_item = driver.find_elements(By.CLASS_NAME, "inventory_item")[0]    
    boton_agregar = first_item.find_element(By.TAG_NAME, "button")
    boton_agregar.click()
    
    
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.inventory_item button'), 'Remove')
    )
    boton_agregar = first_item.find_element(By.TAG_NAME,'button')

    assert boton_agregar.text == 'Remove' , 'ERROR: el boton no cambio a "Remove"'


# Verificar el contador del carrito (que se incremente) 
def test_07_verificar_contador_carrito(driver)   :
    contador_carrito = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    
    assert contador_carrito == "1" , f'ERROR: Se esperaba 1, Obtuvo (contador_carrito)'
    
    
# Navegar al carrito de compras    
def test_08_navegar_carrito(driver):
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    
    assert "/cart.html" in driver.current_url , "ERROR: No se redirigió a /cart.html"

# Comprobar que aparezca el producto añadido
def test_09_comprobar_producto_carrito(driver):
    producto_en_carrito = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    
    assert producto_en_carrito == "Sauce Labs Backpack" , f'ERROR: No es el mismo nombre de producto'
    

    