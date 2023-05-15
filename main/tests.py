from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from .forms import SignUpForm
from .selPath import SELENIUM_DIRS

class cleo(TestCase):
    def test(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(SELENIUM_DIRS, options=chrome_options)

        driver.get("http://127.0.0.1:8000/")


    def register(self, driver):
        register = driver.find_element(By.ID,"signUp")
        register.click()
        time.sleep(2)
        username_register = driver.find_element(By.NAME,"username")
        username_register.send_keys("thanos")
        email_register = driver.find_element(By.NAME,"email")
        email_register.send_keys("thanos@gmail.com")
        password_register = driver.find_element(By.NAME,"password1")
        password_register.send_keys("inevitavel40")
        confirm_register = driver.find_element(By.NAME,"password2")
        confirm_register.send_keys("inevitavel40")
        login = driver.find_element(By.ID,"Sign Up")
        login.click()
    def login(self, driver):
        escrever_username = driver.find_element(By.NAME,"Username")
        escrever_username.send_keys("thanos")
        password_login = driver.find_element(By.NAME,"password")
        password_login.send_keys("inevitavel40")
        botao_login = driver.find_element(By.NAME,"login")
        botao_login.click()
    def status_pedido(self, driver):
        view_order_status = driver.find_element(By.ID,'sino')
        view_order_status.click()
        backtocatalog1 = driver.find_element(By.ID,'arrow')
        backtocatalog1.click()
    def busca_produto_existente(self, driver):
        busca = driver.find_element(By.NAME,"search")
        busca.send_keys("pastel")
        btn_busca = driver.find_element(By.ID,"btn-busca")        
        btn_busca.click()
        busca = driver.find_element(By.NAME,"search")
        busca.clear()
        btn_busca = driver.find_element(By.ID,"btn-busca")
        btn_busca.click()
    def busca_produto_inexistente(self, driver):
        busca = driver.find_element(By.NAME,"search")
        busca.send_keys("lasanha")
        btn_busca = driver.find_element(By.ID,"btn-busca")
        btn_busca.click()
        busca = driver.find_element(By.NAME,"search")
        busca.clear()
        btn_busca = driver.find_element(By.ID,"btn-busca")
        btn_busca.click()
    def adicionarcarrinho(self, driver):
        adicionar_carrinho = driver.find_element(By.NAME,"cartAdd")
        adicionar_carrinho.click()
    def detalhes_produto(self, driver):
        first_product = driver.find_element(By.NAME, "product-link")
        first_product.click()
        for i in range(4):
            increase_button = driver.find_element(By.NAME, "increase")
            increase_button.click()
        for i in range(4):
            decrease_button = driver.find_element(By.NAME, "decrease")
            decrease_button.click()
        adicionar_carrinho2 = driver.find_element(By.NAME, "cartAdd")
        adicionar_carrinho2.click()
        time.sleep(2)
        # leftArrowBack = driver.find_element(By.NAME, 'go-back')
        # leftArrowBack.click()
        # time.sleep(2)
    def entrar_carrinho(self, driver):
        cartBtn = driver.find_element(By.NAME, "cart")
        cartBtn.click()
    def alterar_quantidade(self, driver):
        for i in range(2):
            cartDecrease = driver.find_element(By.NAME, "decreaseCart")
            cartDecrease.click()
        for i in range(2):
            cartIncrease = driver.find_element(By.NAME, "increaseCart")
            cartIncrease.click()
    def adicionar_obs(self, driver):
        cartObs = driver.find_element(By.NAME, "text_box_obs")
        cartObs.send_keys("Eu sou inevitavel!")
        cartObsBtn = driver.find_element(By.NAME, "obsCartBtn")
        cartObsBtn.click()
    def finalizar_compra(self, driver):
        finalizarCompra = driver.find_element(By.NAME, "finalizarCompra")
        finalizarCompra.click()
    def metodo_pagamento(self, driver):
        paymentMethod = driver.find_element(By.NAME, 'payment-method')
        paymentMethod.click()
        pixPay = driver.find_element(By.NAME, "pixPay")
        pixPay.click()
        qrCodeGen = driver.find_element(By.NAME, "generateQrCode")
        qrCodeGen.click()
    def confirmar_compra(self, driver):
        confirmPurchase = driver.find_element(By.NAME, "confirmPurchase")
        confirmPurchase.click()
    def voltar_home(self, driver):
        backtocatalog2 = driver.find_element(By.ID,'arrow')
        backtocatalog2.click()
        # cartClear = driver.find_element(By.NAME, "clearCart")
        # cartClear.click()
        # time.sleep(2)
        driver.quit()