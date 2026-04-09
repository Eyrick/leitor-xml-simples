import os

# Recebe uma linha de texto (ex: 'Valor Total: R$ 3.500,00') 
# e retorna apenas o número como float (ex: 3500.00).
def extrair_valor_numerico(linha):
	if not linha:
		return None
	
	numeros_brutos = ""
	for caractere in linha:		
		if caractere.isdigit() or caractere in ['.', ',']:
			numeros_brutos += caractere

	if not numeros_brutos:
		return None

# 2. Transforma formato brasileiro (1.000,00) em formato de cálculo (1000.00)
	if '.' in numeros_brutos and ',' in numeros_brutos:
			numeros_brutos = numeros_brutos.replace('.', '')
			numeros_brutos = numeros_brutos.replace(',', '.')
	elif ',' in numeros_brutos:
			numeros_brutos = numeros_brutos.replace(',', '.')
    
	try:
		return float(numeros_brutos)
	except ValueError:
		return None

# Abre um arquivo .txt, lê linha por linha e procura por palavras-chave
# que indiquem valores monetários (ex: 'Valor', 'Total', 'R$').
def procurar_valor_no_arquivo(caminho_arquivo):
	# Lista palavras que queremos encontrar
	palavras_chave = ["valor", "total", "r$"]

	try:
		with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
			linhas = arquivo.readlines()
	  
		for linha in linhas:
			linha_lower = linha.lower() # Converte para minúsculas para facilitar a busca
			for chave in palavras_chave:
				if chave in linha_lower:
					linha_limpa = linha.strip()
					valor_num = extrair_valor_numerico(linha_limpa)
					return linha_limpa, valor_num
		# Se não encontrou nada
		return None, None
	
	except Exception as e:
		print(f"⚠️ Erro ao ler {caminho_arquivo}: {e}")
		return None

    
# Função principal: lista arquivos .txt, abre cada um e exibe o valor encontrado.
def listar_e_analisar_arquivos():
	print(60*"=")
	print("🔍 LEITOR DE ARQUIVOS - VERSÃO 0.3")
	print(60*"=")
	
	# Pega a lista de tudo que está na pasta atual
	pasta_atual = os.getcwd()
	print(f"\n📂 Pasta atual: {pasta_atual}\n")

	# Lista os itens da pasta e Filtra apenas os arquivos .txt
	arquivos_txt = [a for a in os.listdir('.') if a.endswith(".txt")]

	# Mostra o resultado
	quant_itens_txt = len(arquivos_txt)
	if not arquivos_txt:
		print(40*"-")
		print("⚠️ Nenhum arquivo .txt encontrado.")
		print(40*"-")
		print("\n")
		return

	print(f"\n📄 {len(arquivos_txt)} arquivo(s) .txt encontrado(s).")
	print("-" * 60)

	# Para cada arquivo, tenta extrair a informação de valor
	resultado = []
	soma_total = 0.0

	for arquivo in arquivos_txt:
		linha_original, valor_float = procurar_valor_no_arquivo(arquivo)

		if valor_float is not None:
			resultado.append((arquivo, linha_original, valor_float))
			soma_total += valor_float
			print(f"✅ {arquivo}")
			print(f"   └─ Texto: {linha_original}")
			print(f"   └─ Valor: R$ {valor_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
		
		else:
			print(f"❌ {arquivo}")
			print(f"   └─ Nenhuma informação de valor encontrada.")		

	# Resumo final
	print("=" * 60)
	print(f"📊 RESUMO: {len(resultado)} de {len(arquivos_txt)} arquivos com valores identificados.")
	
	# Opcional: Exibir apenas os valores encontrados de forma limpa
	if resultado:
		print(f"💰 SOMA TOTAL DOS VALORES: R$ {soma_total:,.2f}\n".replace(',', 'X').replace('.', ',').replace('X', '.'))

if __name__ == "__main__":
	listar_e_analisar_arquivos()