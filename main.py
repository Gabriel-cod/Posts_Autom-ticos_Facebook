from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from random import randint
from time import sleep


def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--start-maximized', '--incognito']
    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,
    })
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)

    return driver

def digitar_naturalmente(text, element):
    for letra in text:
        element.send_keys(f'{letra}')
        sleep(randint(1,5)/30)

def formatar_texto(text):
    print('-'*(len(text)+4))
    print(' '*2 + text)
    print('-'*(len(text)+4))

def login(email, senha):
    try:
        campo_email = driver.find_element(By.ID, 'email')
        campo_email.clear()
        digitar_naturalmente(text=email, element=campo_email)
    except:
        pass
    
    campo_senha = driver.find_element(By.ID, 'pass')
    campo_senha.clear()
    digitar_naturalmente(text=senha, element=campo_senha); sleep(1)

    login_button = driver.find_element(By.ID, 'loginbutton'); sleep(1)
    login_button.click()
    sleep(10)
    try:
        tentar_novo_login_button = driver.find_element(By.XPATH, "//div[@class='clearfix']//div[2]//a"); sleep(1)
        if tentar_novo_login_button is not None:
            tentar_novo_login_button.click(); sleep(1)
            return False
    except:
        return True

def publicar(texto, publico):
    digitar_publicacao = driver.find_element(By.XPATH, "//div[@class='xi81zsa x1lkfr7t xkjl1po x1mzt3pk xh8yej3 x13faqbe']//span")
    digitar_publicacao.click(); sleep(4)
    while True:
        try:
            selecionar_publico = driver.find_elements(By.XPATH, "//div[@class='x6s0dn4 x78zum5 x1q0g3np']//div//i"); sleep(1)
            if publico == 3:
                selecionar_publico[0].click(); sleep(1)
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') 
                sleep(2)
                selecionar_publico[4].click(); sleep(2)
            elif publico == 2:
                selecionar_publico[1].click(); sleep(2)
            else:
                selecionar_publico[0].click(); sleep(2)
            concluir_button = driver.find_element(By.XPATH, "//div[@aria-label='Concluir']"); sleep(1)
            concluir_button.click()
            break
        except:
            alterar_publico = driver.find_elements(By.XPATH, "//div[@role='button']//span[@dir='auto']//div//div")[0]; sleep(1)
            alterar_publico.click(); sleep(5)        
    campo_digitar = driver.find_element(By.XPATH, "//div[@role='textbox']//p"); sleep(1)
    campo_digitar.click(); sleep(1)
    digitar_naturalmente(texto, campo_digitar)
    publicar_button = driver.find_element(By.XPATH, "//div[@aria-label='Publicar']"); sleep(1)
    publicar_button.click(); sleep(5)
    
tipo_de_publico = ''
login_feito = True
driver = iniciar_driver()
driver.get('https://web.facebook.com/login')
sleep(5)

formatar_texto('Automação de Posts no Facebook')

while True:
    meu_email = str(input('Informe seu email de login: ')).strip().lower()
    minha_senha = str(input('Informe sua senha: '))
    while True:
        tipo_de_publico = str(input('Informe o tipo de público que verá sua publicação [Todos: 1, Amigos: 2, Somente você: 3]: ')).strip()
        if tipo_de_publico not in '123':
            formatar_texto('ATENÇÃO: Digite apenas 1, 2 ou 3 para definir os parâmetros de público.')
            continue
        tipo_de_publico = int(tipo_de_publico[0])
        break
    mensagem = str(input('Informe a mensagem que deseja publicar: '))
    login_feito = login(email=meu_email, senha=minha_senha)
    if login_feito == False:
        formatar_texto('ATENÇÃO: Email ou Senha incorretos, por favor verifique seu login e tente novamente.'); sleep(5)
        continue
    formatar_texto('AGUARDE...')
    publicar(mensagem, tipo_de_publico)
    formatar_texto('MENSAGEM PUBLICADA')
    input('Digite enter para finalizar.')
