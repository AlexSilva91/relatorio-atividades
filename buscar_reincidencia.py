import pandas as pd
from datetime import datetime, timedelta

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
    atividade = df.iloc[:, 8].str.lower()
    data = pd.to_datetime(df.iloc[:, 14], errors='coerce')
    tecnico = df.iloc[:, 15]
    return tecnico, contrato, atividade, data

def gerar_dicionario(tecnico, contrato, atividade, data):
    dados_contratos = {}
    for cont, atv, dt, tec in zip(contrato, atividade, data, tecnico):
        if isinstance(tec, str) and tec.strip() != '':  
            if cont not in dados_contratos:
                dados_contratos[cont] = []
            dados_contratos[cont].append({'atividade': atv, 'data': dt, 'tecnico': tec})
    return dados_contratos

def filtrar_atividades(dados_contratos, atividades_a_exibir):
    dados_filtrados = {}
    for contrato, atividades in dados_contratos.items():
        atividades_filtradas = []
        for atividade in atividades:
            if atividade['atividade'].lower() in atividades_a_exibir:
                atividades_filtradas.append(atividade)
        if atividades_filtradas:
            dados_filtrados[contrato] = atividades_filtradas
    return dados_filtrados

def consolidar_contratos_funcao(dados_filtrados, atividades_a_exibir):
    contratos_consolidados = {}
    for contrato, atividades in dados_filtrados.items():
        atividades_filtradas = []
        for atividade in atividades:
            if atividade['atividade'].lower() in atividades_a_exibir or atividade['atividade'].lower() == 'corretiva':
                atividades_filtradas.append(atividade)
        if len(atividades_filtradas) > 1 or any(atividade['atividade'].lower() == 'corretiva' for atividade in atividades_filtradas):
            contratos_consolidados[contrato] = {'atividades': atividades_filtradas}
    return contratos_consolidados

def filtrar_contratos(contratos_consolidados, atividades_a_exibir):
    contratos_filtrados = {}
    for contrato, info in contratos_consolidados.items():
        if len(info['atividades']) > 1 or any(atividade['atividade'].lower() == 'corretiva' for atividade in info['atividades']):
            atividades_filtradas = []
            for atividade in info['atividades']:
                if atividade['atividade'].lower() in atividades_a_exibir:
                    atividades_filtradas.append(atividade)
            if atividades_filtradas:
                contratos_filtrados[contrato] = {'atividades': atividades_filtradas}
    return contratos_filtrados

def verificar_e_salvar_contratos(contratos_filtrados):
    contratos_salvos = {}
    for contrato, info in contratos_filtrados.items():
        if any(atividade['atividade'].lower() == 'corretiva' for atividade in info['atividades']):
            contratos_salvos[contrato] = info
        else:
            datas_servico = [servico['data'] for servico in info['atividades']]
            menor_data_servico = min(datas_servico)
            salvar_contrato = True
            for data_servico in datas_servico:
                if (data_servico - menor_data_servico).days > 30:
                    salvar_contrato = False
                    break
            if salvar_contrato:
                contratos_salvos[contrato] = info
    return contratos_salvos

def salvar_contratos_em_txt(contratos_salvos, nome_arquivo):
    try:
        total_contratos_impressos = 0
        with open(nome_arquivo, 'w') as arquivo:
            for contrato, info in contratos_salvos.items():
                if len(info['atividades']) > 1 or any(atividade['atividade'].lower() == 'corretiva' for atividade in info['atividades']):
                    arquivo.write(f"Contrato: {contrato}\n")
                    arquivo.write("Atividades:\n")
                    for atividade in info['atividades']:
                        arquivo.write(f"Atividade: {atividade['atividade']}, Data: {atividade['data']}, Técnico: {atividade['tecnico']}\n")
                    arquivo.write("\n")
                    total_contratos_impressos += 1
            arquivo.write(f"---------------------------------------\nTotal de contratos impressos: {total_contratos_impressos}\n---------------------------------------")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar as informações dos contratos no arquivo: {e}")

def buscar_reinicidencia(caminho_arq):
    caminho_arquivo = caminho_arq
    planilha_nome = "Ordens de Serviço"
    atividades_a_exibir = ["suporte externo", "corretiva"]

    df = ler_planilha(caminho_arquivo, planilha_nome)
    tecnico, contrato, atividade, data = extrair_colunas_interesse(df)
    dados_contratos = gerar_dicionario(tecnico, contrato, atividade, data)
    dados_filtrados = filtrar_atividades(dados_contratos, atividades_a_exibir)
    consolidar_contratos_variavel = consolidar_contratos_funcao(dados_filtrados, atividades_a_exibir) # Renomeada a variável
    contratos_filtrados = filtrar_contratos(consolidar_contratos_variavel, atividades_a_exibir)

    #contratos_salvos = verificar_e_salvar_contratos(contratos_filtrados)

    resultado_apos_filtro = verificar_e_salvar_contratos(contratos_filtrados)

    salvar_contratos_em_txt(resultado_apos_filtro, "reincidência.txt")

