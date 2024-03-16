import pandas as pd
from datetime import datetime

def ler_planilha(caminho_arquivo, planilha_nome):
    try:
        df = pd.read_excel(caminho_arquivo, sheet_name=planilha_nome)
        df = df.drop(df.index[:7])
        return df
    except FileNotFoundError:
        print("O arquivo especificado não pôde ser encontrado.")
        return None

def extrair_colunas_interesse(df):
    contrato = df.iloc[:, 2]
    atividade = df.iloc[:, 8].str.lower()  # Convertendo todas as atividades para minúsculas
    data = pd.to_datetime(df.iloc[:, 14], errors='coerce')  # Convertendo para datetime e lidando com erros
    tecnico = df.iloc[:, 15]
    return contrato, atividade, data, tecnico

def gerar_dicionario_contrato_atividade_tecnico(contrato, atividade, data, tecnico, atividades_a_exibir):
    contrato_atividade_tecnico = {}
    for c, a, d, t in zip(contrato, atividade, data, tecnico):
        if pd.notna(c) and pd.notna(t) and not pd.isnull(d):  # Verifica se os dados não são nulos
            if c not in contrato_atividade_tecnico:
                contrato_atividade_tecnico[c] = {'atividades': [], 'tecnico': t, 'datas': []}
            if a in atividades_a_exibir:
                contrato_atividade_tecnico[c]['atividades'].append(a)
                contrato_atividade_tecnico[c]['datas'].append(d)
    return contrato_atividade_tecnico

def verificar_suporte_externo(contrato_atividade_tecnico):
    contratos_suporte_externo = {}
    for contrato, dados in contrato_atividade_tecnico.items():
        atividades = dados['atividades']
        datas = dados['datas']
        if 'suporte externo' in atividades and len(atividades) > 1:
            datas_ordenadas = sorted(datas)
            diferenca_datas = (datas_ordenadas[-1] - datas_ordenadas[0]).days
            if diferenca_datas <= 15:
                contratos_suporte_externo[contrato] = {'atividades': ['suporte externo'], 'quantidade': len(atividades), 'datas': datas_ordenadas, 'tecnico': dados['tecnico']}
    return contratos_suporte_externo

def gerar_relatorio_corretiva(contrato_atividade_tecnico):
    relatorio_corretiva = []
    for contrato, dados in contrato_atividade_tecnico.items():
        atividades = dados['atividades']
        tecnico = dados['tecnico']
        datas = dados['datas']
        for i in range(len(atividades)):
            if atividades[i] == 'corretiva':
                relatorio_corretiva.append({'contrato': contrato, 'atividade': atividades[i], 'tecnico': tecnico, 'data': datas[i]})
    return relatorio_corretiva

def gerar_relatorio(caminho):
    #caminho_arquivo = "/home/alex/Downloads/ordemservico-2024-03-07-230029.xlsx"
    caminho_arquivo = caminho
    planilha_nome = "Ordens de Serviço"
    tecnicos_a_evitar = ["tiago.peres", "eguinailson.nunes", "evandro.zuza", "geimerson.alves"]
    atividades_a_exibir = ["suporte externo", "corretiva"]

    df = ler_planilha(caminho_arquivo, planilha_nome)
    if df is not None:
        contrato, atividade, data, tecnico = extrair_colunas_interesse(df)
        
        # Remover valores "nan" da lista de técnicos
        tecnico = tecnico.dropna()
        
        # Remover técnicos que estão na lista de técnicos a evitar
        tecnico = tecnico[~tecnico.isin(tecnicos_a_evitar)]
        
        # Remover atividades que não estão na lista de atividades a exibir
        atividade = atividade[atividade.isin(atividades_a_exibir)]
        
        # Criar dicionário com contrato como chave e atividades, técnico e datas como valores
        contrato_atividade_tecnico = gerar_dicionario_contrato_atividade_tecnico(contrato, atividade, data, tecnico, atividades_a_exibir)
        
        # Verificar e gerar relatório para atividade 'suporte externo'
        relatorio_suporte_externo = verificar_suporte_externo(contrato_atividade_tecnico)
        
        # Gerar relatório para atividade 'corretiva'
        relatorio_corretiva = gerar_relatorio_corretiva(contrato_atividade_tecnico)
        
        # Salvar a saída em um arquivo de texto
        with open("relatório_reincidência.txt", "w") as file:
            file.write(f"---------------------------------------------------\n-------->  Relatório Suporte Externo: {len(relatorio_suporte_externo)}  <--------\n---------------------------------------------------\n")
            for contrato, dados in relatorio_suporte_externo.items():
                file.write(f'Contrato: {contrato}\n')
                file.write(f'Atividades: {dados["atividades"]}\n')
                file.write(f'Quantidade de Repetições: {dados["quantidade"]}\n')
                file.write(f'Técnico: {dados["tecnico"]}\n')
                file.write(f'Datas: {", ".join(map(str, dados["datas"]))}\n')
                file.write('\n')
            file.write("---------------------------------------------------")
            
            file.write(f"\n--------------------------------\n---> Relatório Corretiva: {len(relatorio_corretiva)} <---\n--------------------------------\n")
            for dados in relatorio_corretiva:
                file.write(f'Contrato: {dados["contrato"]}\n')
                file.write(f'Atividade: {dados["atividade"]}\n')
                file.write(f'Técnico: {dados["tecnico"]}\n')
                file.write(f'Data: {dados["data"]}\n')
                file.write('\n')


