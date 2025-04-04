# 🏠 Web Scraping de Imóveis - DFImóveis

Projeto de scraping que coleta automaticamente dados de imóveis anunciados no site [dfimoveis.com.br](https://www.dfimoveis.com.br/), com filtros customizáveis pelo usuário via terminal. Os dados são armazenados em um banco de dados MySQL para futura análise e visualização com Streamlit.

---

## 📦 Tecnologias Utilizadas

- [Python 3.10+](https://www.python.org/)
- [Selenium](https://www.selenium.dev/)
- [Pandas](https://pandas.pydata.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [MySQL](https://www.mysql.com/)
- [dotenv](https://pypi.org/project/python-dotenv/)
- [Streamlit](https://streamlit.io/) *(futuro painel de visualização)*

---

## 🚀 Funcionalidades

- Entrada de filtros via terminal (tipo, cidade, bairro, quartos, valor máximo, etc.)
- Extração automática de dados com Selenium
- Coleta de:
  - Título do imóvel
  - Preço
  - Metragem
  - Número de quartos e suítes
  - Descrição
  - Link direto do anúncio
- Armazenamento estruturado em banco de dados MySQL
- Pronto para visualização futura com Streamlit

---

## 🛠️ Como Usar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/web-scraping-imoveis.git
cd web-scraping-imoveis

# Criando e ativando o venv
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

## Configure o arquivo .env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=db_imoveis


## Lembre-se de utilizar o google chrome e utilizar o MySql WorkBench para realizar as ações dentro do banco de dados

## 👨‍💻 Sobre o Autor

Olá! Meu nome é Pedro, sou estudante de Ciência de Dados no IBMEC e apaixonado por automação, dados e desenvolvimento de soluções inteligentes. Este projeto surgiu como uma forma de aplicar técnicas de scraping e armazenamento de dados estruturados para análises futuras no mercado imobiliário do Distrito Federal.

Você pode me encontrar por aqui:

- 💻 [GitHub][(https://github.com/seu-usuario)](https://github.com/pedrocadaluz)  
- ✉️ Email: pedrocadaluz@gmail.com

Se quiser trocar uma ideia, colaborar ou tiver alguma sugestão, fique à vontade pra chamar!
