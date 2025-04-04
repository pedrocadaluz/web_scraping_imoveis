from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
from dotenv import load_dotenv
import os

# -----------------------------
# ENTRADA DOS FILTROS VIA USUÁRIO
# -----------------------------
TIPO = input("Digite o tipo de imóvel (ex: APARTAMENTO, CASA): ").upper()
MODALIDADE = input("Digite a modalidade (ex: VENDA, ALUGUEL): ").upper()
ESTADO = input("Digite o estado: ").upper()
CIDADE = input("Digite a cidade (ex: BRASILIA / PLANO PILOTO): ").upper()
BAIRRO = input("Digite o bairro (ex: ASA SUL): ").upper()
QUARTOS = input("Número de quartos (ex: 3): ")
VALOR = input("Valor máximo (ex: 1500000): ")
ENDERECO = input("Digite o endereço ou rua específica (opcional): ")

# -----------------------------
# INICIALIZAÇÃO DO DRIVER
# -----------------------------
options = Options()
url = "https://www.dfimoveis.com.br/"
driver = webdriver.Chrome(options=options)
driver.get(url)
wait = WebDriverWait(driver, 20)

# -----------------------------
# APLICAÇÃO DOS FILTROS
# -----------------------------
# MODALIDADE
el = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'select2-selection--single')))
el.click()
el = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'select2-search__field')))
el.send_keys(MODALIDADE)
el.send_keys(Keys.ENTER)

# TIPO
el = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[1]/section/section[1]/div[2]/div/form/div[1]/div[2]/span/span[1]/span")))
el.click()
el = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "select2-search__field")))
el.send_keys(TIPO)
el.send_keys(Keys.ENTER)

# ESTADO
el = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[1]/section/section[1]/div[2]/div/form/div[1]/div[3]/span/span[1]/span/span[1]")))
el.click()
el = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "select2-search__field")))
el.send_keys(ESTADO)
el.send_keys(Keys.ENTER)

# CIDADE
el = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[1]/section/section[1]/div[2]/div/form/div[1]/div[4]/span")))
el.click()
el = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "select2-search__field")))
el.send_keys(CIDADE)
el.send_keys(Keys.ENTER)

# BAIRRO
el = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[1]/section/section[1]/div[2]/div/form/div[1]/div[5]/span')))
el.click()
el = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "select2-search__field")))
el.send_keys(BAIRRO)
el.send_keys(Keys.ENTER)

# QUARTOS
el = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[1]/section/section[1]/div[2]/div/form/div[1]/div[6]/div[1]/span")))
el.click()
option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{QUARTOS}')]")))
option.click()

# VALOR
el = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[1]/section/section[1]/div[2]/div/form/div[1]/div[6]/div[2]/input")))
el.send_keys(VALOR)

# ENDERECO
el = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[1]/section/section[1]/div[2]/div/form/div[1]/div[7]/input")))
el.send_keys(ENDERECO)

# CLICA EM BUSCAR
btn_busca = wait.until(EC.element_to_be_clickable((By.ID, "botaoDeBusca")))
btn_busca.click()

# -----------------------------
# COLETA DE LINKS DOS RESULTADOS
# -----------------------------
sleep(5)
xpath_resultados = "/html/body/main/div[1]/div[1]/div[2]/div[2]/div[2]"
resultados = wait.until(EC.presence_of_element_located((By.XPATH, xpath_resultados)))

links = []
for a in resultados.find_elements(By.TAG_NAME, "a"):
    href = a.get_attribute("href")
    if href and "imovel" in href:
        links.append(href)

print("Total de imóveis encontrados:", len(links))

# -----------------------------
# COLETA DE DADOS DOS IMÓVEIS
# -----------------------------
lst_imoveis = []

for link in links:
    driver.get(link)
    imovel = {"link": link}
    try:
        imovel["titulo"] = wait.until(EC.presence_of_element_located((By.XPATH, "//h1"))).text
        imovel["preco"] = wait.until(EC.presence_of_element_located((By.XPATH, "//h6/small"))).text
        imovel["metragem"] = wait.until(EC.presence_of_element_located((By.XPATH, "//div[5]/h6/small"))).text
        imovel["quartos"] = wait.until(EC.presence_of_element_located((By.XPATH, "//div[7]/div/div[3]/h6"))).text
        imovel["suites"] = wait.until(EC.presence_of_element_located((By.XPATH, "//div[7]/div/div[4]/h6"))).text
        imovel["descricao"] = wait.until(EC.presence_of_element_located((By.XPATH, "//div[6]/p"))).text
        lst_imoveis.append(imovel)
    except:
        print(f"[ERRO] Não foi possível coletar dados do link: {link}")
        continue

# Fecha o navegador
driver.quit()

# -----------------------------
# TRATAMENTO DOS DADOS
# -----------------------------
df = pd.DataFrame(lst_imoveis)
df['quartos'] = df['quartos'].str.replace('Quartos: ', '', regex=False)
df['suites'] = df['suites'].str.replace('Suítes: ', '', regex=False)
df['descricao'] = df['descricao'].str.slice(0, 255)
df['preco'] = df['preco'].str.replace(r'[^\d,]', '', regex=True).str.replace(',', '.').astype(float)

# -----------------------------
# INSERÇÃO NO BANCO DE DADOS
# -----------------------------
load_dotenv()
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database_name = os.getenv("DB_NAME")


DATABASE_URL = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}'
engine = create_engine(DATABASE_URL)

# Salvar no banco
df.to_sql('tb_imoveis', con=engine, if_exists='append', index=False)
print("Dados salvos no banco com sucesso!")
