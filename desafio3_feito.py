from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def obter_dados(usuario):
    return {
        'nome': usuario.find_element(By.CSS_SELECTOR, 'h3').text,
        'profissao': usuario.find_element(By.CSS_SELECTOR, 'span').text,
        'email': usuario.find_element(By.CSS_SELECTOR, 'ul li:nth-child(1)').text.replace('E-mail: ', ''),
        'telefone': usuario.find_element(By.CSS_SELECTOR, 'ul li:nth-child(2)').text.replace('Telefone: ', ''),
        'user': usuario.find_element(By.CSS_SELECTOR, 'ul li:nth-child(3)').text.replace('Usuário: ', ''),
        'estado': usuario.find_element(By.CSS_SELECTOR, 'ul li:nth-child(4)').text.replace('Estado: ', '')
    }

def localizar_elementos(driver):
    try:
        return {
            'nome': driver.find_element(By.NAME, 'nome'),
            'profissao': driver.find_element(By.NAME, 'profissao'),
            'email': driver.find_element(By.NAME, 'email'),
            'telefone': driver.find_element(By.NAME, 'telefone'),
            'usuario': driver.find_element(By.NAME, 'usuario'),
            'estado': Select(driver.find_element(By.NAME, 'estado')),
            'btn_enviar': driver.find_element(By.XPATH, '/html/body/div/div/div[2]/main/div[2]/div/form/button')
        }
    except Exception as e:
        print(f"Erro ao localizar elementos: {e}")
        return None

def pesquisar_nome(driver, abas, wait):
    principal = driver.find_element(By.ID, 'usuario').text
    driver.switch_to.window(window_name=abas['ex2'])
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'main')))

    pesquisar = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/main/div[2]/div/div[2]/input')
    botao = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/main/div[2]/div/div[2]/button')

    pesquisar.send_keys(principal)
    botao.click()
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/main/div[2]/div/section/div/div[2]')))

    return driver.find_elements(By.CSS_SELECTOR, 'section div div div div')

def preencher_formulario(elementos, dados):
    try:
        elementos['nome'].send_keys(dados['nome'])
        elementos['profissao'].send_keys(dados['profissao'])
        elementos['email'].send_keys(dados['email'])
        elementos['telefone'].send_keys(dados['telefone'])
        elementos['usuario'].send_keys(dados['user'])
        elementos['estado'].select_by_visible_text(dados['estado'])
        elementos['btn_enviar'].click()
    except Exception as e:
        print(f"Erro ao preencher o formulário: {e}")
    finally:
        limpar_campos(elementos)

def limpar_campos(elementos):
    elementos['nome'].clear()
    elementos['profissao'].clear()
    elementos['email'].clear()
    elementos['telefone'].clear()
    elementos['usuario'].clear()

def main():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    driver.implicitly_wait(10)

    driver.get("https://curso-web-scraping.pages.dev/#/desafio/2")
    driver.switch_to.new_window('tab')
    driver.get("https://curso-web-scraping.pages.dev/#/desafio/3")

    abas = {'ex2': driver.window_handles[0], 'ex3': driver.window_handles[1]}

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'main')))

    elementos = localizar_elementos(driver)
    if not elementos:
        return

    pessoas = pesquisar_nome(driver, abas, wait)
    dados_lista = [obter_dados(pessoa) for pessoa in pessoas]

    driver.switch_to.window(window_name=abas['ex3'])

    for dados in dados_lista:
        preencher_formulario(elementos, dados)

    # Adicionando um usuário específico
    usuario_extra = {
        'nome': 'Dalton Pereira',
        'profissao': 'Engenheiro',
        'email': 'dalton_pereira31@example.org',
        'telefone': '(45) 10655-0760',
        'user': 'dalton_pereira61',
        'estado': 'Goiás'
    }
    preencher_formulario(elementos, usuario_extra)

if __name__ == "__main__":
    main()