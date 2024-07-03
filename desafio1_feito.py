import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# Funções para obter o dia, mês e ano da data de nascimento de um usuário no arquivo JSON
def getDia(index, arq):
    _, _, dia = arq[index]['data-de-nascimento'].split('-')
    return dia

def getMes(index, arq):
    _, mes, _ = arq[index]['data-de-nascimento'].split('-')
    return mes

def getAno(index, arq):
    ano, _, _ = arq[index]['data-de-nascimento'].split('-')
    return ano

# Abrir o arquivo JSON e carregar os dados
with open('desafio_1.json', 'r') as f:
    dados = json.load(f)

try:
    # Inicializar o navegador Chrome
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)  # Esperar até 3 segundos por elementos

    # Abrir a página de desafio
    driver.get('https://curso-web-scraping.pages.dev/#/desafio/1')

    # Localizar elementos na página
    email = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/main/div[2]/div/form/div[1]/input')
    senha = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/main/div[2]/div/form/div[2]/input')
    dia = Select(driver.find_element(By.XPATH, '/html/body/div/div/div[2]/main/div[2]/div/form/div[3]/div/select'))
    mes = Select(driver.find_element(By.XPATH, '/html/body/div/div/div[2]/main/div[2]/div/form/div[3]/div/div[1]/select'))
    ano = Select(driver.find_element(By.XPATH, '/html/body/div/div/div[2]/main/div[2]/div/form/div[3]/div/div[2]/select'))
    botao = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/main/div[2]/div/form/div[4]/div/button')

except Exception as e:
    print(e)  # Imprimir mensagem de erro se ocorrer

try:
    # Preencher o formulário para cada usuário nos dados JSON
    for i in range(len(dados)):
        email.send_keys(dados[i]['email'])
        senha.send_keys(dados[i]['senha'])
        dia.select_by_index(int(getDia(i, dados)) - 1)
        mes.select_by_index(int(getMes(i, dados)) - 1)
        ano.select_by_visible_text(getAno(i, dados))

        if dados[i]['newsletter']:
            botao.click()  # Clicar no botão se o usuário desejar receber newsletter

        email.submit()  # Enviar o formulário
        email.clear()   # Limpar o campo de email
        senha.clear()   # Limpar o campo de senha
        driver.implicitly_wait(1)  # Esperar por 1 segundo entre operações

except Exception as e:
    print(e)  # Imprimir mensagem de erro se ocorrer

print('Código finalizado')

input("Pressione qualquer tecla para fechar")  # Esperar a entrada
driver.quit()