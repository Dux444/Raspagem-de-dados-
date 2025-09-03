import requests
from bs4 import BeautifulSoup
import csv

# Define a URL (endereço web) da página que queremos raspar.
url = "https://books.toscrape.com/index.html"

# Informa ao usuário que o processo de download vai começar.
print(f"Baixando a página: {url}")

# O bloco 'try...except' é usado para lidar com possíveis erros de conexão.
try:
    # Faz uma requisição GET para a URL. Isso baixa o conteúdo HTML da página.
    response = requests.get(url)
    # Lança um erro se a requisição não for bem-sucedida.
    response.raise_for_status()
# Se houver qualquer erro na requisição, ele será capturado aqui.
except requests.exceptions.RequestException as e:
    # Exibe a mensagem de erro e encerra o programa.
    print(f"Erro ao baixar a página: {e}")
    exit()

# Cria um objeto BeautifulSoup para analisar o HTML.
# 'response.text' contém o código-fonte da página como uma string.
# 'html.parser' é o analisador de HTML padrão do Python.
soup = BeautifulSoup(response.text, 'html.parser')

# Encontra todos os elementos HTML que representam um livro.
# Cada livro está contido em uma tag <article> com a classe 'product_pod'.
books = soup.find_all('article', class_='product_pod')

# Cria uma lista vazia para armazenar os dicionários de dados de cada livro.
book_data = []

# Informa quantos livros foram encontrados.
print(f"Extraindo dados de {len(books)} livros...")

# Inicia um loop para processar cada livro encontrado na lista 'books'.
for book in books:
    # Encontra a tag <a> dentro de <h3> e extrai o título do atributo 'title'.
    title_tag = book.find('h3').find('a')
    title = title_tag['title']

    # Encontra a tag <p> com a classe 'price_color' e extrai o texto do preço.
    price_tag = book.find('p', class_='price_color')
    price = price_tag.text.strip() # .strip() remove espaços em branco extras.

    # Encontra a tag <p> com a classe 'instock availability' e extrai o texto de disponibilidade.
    availability_tag = book.find('p', class_='instock availability')
    availability = availability_tag.text.strip()

    # Adiciona um dicionário com as informações do livro à lista 'book_data'.
    book_data.append({
        'title': title,
        'price': price,
        'availability': availability
    })

# Define o nome do arquivo CSV de saída.
csv_filename = "books.csv"
print(f"Salvando dados em {csv_filename}...")

# O bloco 'try...except' lida com erros de escrita de arquivo.
try:
    # Abre o arquivo CSV em modo de escrita ('w').
    # 'newline=''' evita linhas em branco extras no arquivo.
    # 'encoding='utf-8'' garante que caracteres especiais sejam salvos corretamente.
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Define os nomes das colunas do CSV (cabeçalho).
        fieldnames = ['title', 'price', 'availability']
        # Cria um objeto DictWriter para escrever os dados.
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Escreve a primeira linha do arquivo com os nomes das colunas.
        writer.writeheader()
        # Itera sobre a lista de dados e escreve cada linha no arquivo CSV.
        for data in book_data:
            writer.writerow(data)

    # Mensagem de sucesso ao finalizar a raspagem e o salvamento.
    print(f"Raspagem de dados concluída. Os dados foram salvos com sucesso em {csv_filename}.")
# Se houver erro ao salvar o arquivo (ex: permissões de escrita), ele será capturado aqui.
except IOError as e:
    print(f"Erro ao salvar o arquivo CSV: {e}")