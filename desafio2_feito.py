from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import csv
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Função para escrever os dados dos usuários em um arquivo CSV
def escrever_csv(usuarios, arq='banco_usuarios.csv'):
    with open(arq, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        writer.writerow(['foto', 'nome', 'emprego', 'email', 'telefone', 'usuario', 'estado'])
        for i in usuarios:
            writer.writerow([i['foto'],
                             i['nome'],
                             i['emprego'],
                             i['email'],
                             i['telefone'],
                             i['usuario'],
                             i['estado']])
            
# Função para obter os dados dos usuários
def obterDadosUsuario(usuario):
    try: 
        foto = usuario.find_element(By.TAG_NAME, 'img').get_attribute('src')
        nome = usuario.find_element(By.TAG_NAME, 'h3').text
        emprego = usuario.find_element(By.CSS_SELECTOR, 'div > span').text
        email = usuario.find_element(By.CSS_SELECTOR, 'ul > li:nth-child(1)').text.replace('E-mail: ', '')
        telefone = usuario.find_element(By.CSS_SELECTOR, 'ul > li:nth-child(2)').text.replace('Telefone: ', '')
        login = usuario.find_element(By.CSS_SELECTOR, 'ul > li:nth-child(3)').text.replace('Usuário: ', '')
        estado = usuario.find_element(By.CSS_SELECTOR, 'ul > li:nth-child(4)').text.replace('Estado: ', '')

        return {'foto': foto,
                        'nome': nome,
                        'emprego': emprego,
                        'email':email,
                        'telefone':telefone,
                        'usuario':login,
                        'estado':estado}
    except Exception as e:
        print(f"Erro: {e}")
        return None

# Inicializando o Chrome
driver = webdriver.Chrome()

driver.implicitly_wait(3.5)

wait = WebDriverWait(driver=driver, timeout=20, poll_frequency=0.2)

# Lendo o arquivo JSON
with open('desafio_2.json', 'r') as f:
    dados = json.load(f)

driver.get('https://curso-web-scraping.pages.dev/#/desafio/2')

# Obtendo botões de pesquisa
input = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/main/div[2]/div/div[2]/input')
botao = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/main/div[2]/div/div[2]/button')

usuario_list = []

# Itera sobre os dados JSON, insere cada dado no campo de entrada, clica no botão, limpa o campo, espera os elementos
# carregarem, busca os elementos de usuário, obtém os dados de cada usuário e adiciona à lista de usuários
try:
    for dado in dados:
        input.send_keys(dado)
        botao.click()
        input.clear()

        wait.until(EC.presence_of_all_elements_located(locator=(By.CSS_SELECTOR, 'section > div > div')))

        users = driver.find_elements(By.CSS_SELECTOR, 'div.users-list > div')

        for user in users:
            
            usuario = obterDadosUsuario(user)
            if usuario:
                usuario_list.append(usuario)

except Exception as e:
    print(f"Erro: {e}")
finally:
    driver.quit()

escrever_csv(usuario_list)
print("Codigo finalizado.")