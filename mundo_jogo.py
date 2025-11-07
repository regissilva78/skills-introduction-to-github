# Arquivo: mundo_jogo.py
#
# =========================================================================
# == TUTORIAL PASSO A PASSO: O BANCO DE DADOS CENTRAL (O "Universo") ==
# =========================================================================
#
# Objetivo: Definir o "Estado Inicial" de TUDO no jogo.
# Matéria Aplicada: Pandas [cite: pdf 4 dataflame 47480719.pdf], 
#                  Tabelas Hash (Dicionários) [cite: pdf 4 26481138.pdf],
#                  Listas Lineares [cite: pdf 1. 27070497.pdf]
#
# Para "facilitar a inserção", você só precisa adicionar
# entradas nestes dicionários e DataFrames. O "Motor" (app.py)
# foi programado para ler e entender esta estrutura.
# =========================================================================

import pandas as pd

# -------------------------------------------------------------------------
# BLOCO 1: O "Relógio Mestre" e o "Mundo"
# -------------------------------------------------------------------------
# APLICAÇÃO (Tabela Hash): Um dicionário para guardar o estado global.
estado_mundo = {
    'dia_semana': 'segunda-feira', # segunda-feira, terça-feira, etc.
    'periodo': 'manha',      # manha, tarde, noite, madrugada
    'hora': 6,               # Hora (0-23)
    'minuto': 0,             # Minuto (0-59)
    'dinheiro_yumi': 50.00
}

# -------------------------------------------------------------------------
# BLOCO 2: A PERSONAGEM (YUMI)
# -------------------------------------------------------------------------
# APLICAÇÃO (Pandas Series): Os status base da Yumi.
db_yumi_status = pd.Series(
    [0, 10, 50, 20, 10], 
    index=['depravacao', 'inteligencia', 'amizade', 'beleza', 'sensual']
    # Nota: O 'max' de depravacao (500) será controlado no app.py
)
# APLICAÇÃO (Tabela Hash): O estado dinâmico da Yumi.
estado_yumi = {
    'local_atual': 'quarto_yumi', 
    'roupa_atual': 'pijama',
    # APLICAÇÃO (Pilha/Stack): A "Pilha de Ações" da Yumi.
    # É o que a torna "programável" e permite "ações autônomas".
    # [cite: pdf 1. 27070497.pdf]
    'pilha_acoes': [] # Ex: ['ir_para_quarto', 'chorar']
}

# -------------------------------------------------------------------------
# BLOCO 3: O "ELENCO" (Banco de Dados de NPCs)
# -------------------------------------------------------------------------
# APLICAÇÃO (Pandas DataFrame): A "Lista de NPCs" completa.
# [cite: pdf 4 dataflame 47480719.pdf]
# Adicionamos os 5 familiares + Julio.
dados_iniciais_npcs = {
    # 'nome_exibicao': O nome que aparece no jogo.
    'nome_exibicao': ['Mãe (Teruma)', 'Pai (Kazuki)', 'Irmão (Mike)', 'Irmão (Jack)', 'Amigo (Carlos)', 'Amigo (Julio)'],
    
    # 'local_atual': Onde o NPC está AGORA.
    'local_atual': ['cozinha', 'quarto_casal', 'quarto_irmaos', 'quarto_irmaos', 'escola', 'rua'],
    
    # 'estado_emocional': O "humor" atual.
    'estado_emocional': ['preocupada', 'cansado', 'entediado', 'focado', 'neutro', 'atrevido'],
    
    # 'amizade_yumi': Status de relacionamento com a Yumi.
    'amizade_yumi': [70, 50, 20, 25, 40, 5],
    
    # 'agenda': O que o NPC faz. O "Motor" vai ler isso.
    # APLICAÇÃO (Tabela Hash Aninhada): Um dicionário de dicionários.
    # Estrutura: { dia: { periodo: local } }
    'agenda': [
        # Agenda da Mãe
        {'segunda-feira': {'manha': 'cozinha', 'tarde': 'trabalho', 'noite': 'sala_estar'},
         'terca-feira': {'manha': 'cozinha', 'tarde': 'trabalho', 'noite': 'sala_estar'},
         'sabado': {'manha': 'quarto_casal', 'tarde': 'shopping', 'noite': 'sala_estar'}},
        # Agenda do Pai
        {'segunda-feira': {'manha': 'trabalho', 'tarde': 'trabalho', 'noite': 'sala_estar'},
         'terca-feira': {'manha': 'trabalho', 'tarde': 'trabalho', 'noite': 'quarto_casal'},
         'sabado': {'manha': 'sala_estar', 'tarde': 'sala_estar', 'noite': 'sala_estar'}},
        # Agenda do Mike
        {'segunda-feira': {'manha': 'escola', 'tarde': 'sala_estar', 'noite': 'quarto_irmaos'},
         'terca-feira': {'manha': 'escola', 'tarde': 'lanchonete', 'noite': 'quarto_irmaos'},
         'sabado': {'manha': 'quarto_irmaos', 'tarde': 'rua', 'noite': 'rua'}},
        # Agenda do Jack
        {'segunda-feira': {'manha': 'home_office', 'tarde': 'home_office', 'noite': 'quarto_irmaos'},
         'terca-feira': {'manha': 'home_office', 'tarde': 'home_office', 'noite': 'quarto_irmaos'},
         'sabado': {'manha': 'quarto_irmaos', 'tarde': 'cinema', 'noite': 'quarto_irmaos'}},
        # Agenda do Carlos
        {'segunda-feira': {'manha': 'escola', 'tarde': 'lanchonete', 'noite': 'rua'},
         'terca-feira': {'manha': 'escola', 'tarde': 'lanchonete', 'noite': 'rua'},
         'sabado': {'manha': 'rua', 'tarde': 'shopping', 'noite': 'rua'}},
        # Agenda do Julio
        {'segunda-feira': {'manha': 'escola', 'tarde': 'sala_estar', 'noite': 'sala_estar'},
         'terca-feira': {'manha': 'escola', 'tarde': 'lanchonete', 'noite': 'sala_estar'},
         'sabado': {'manha': 'rua', 'tarde': 'rua', 'noite': 'rua'}},
    ]
}
db_npcs = pd.DataFrame(dados_iniciais_npcs, index=['mae', 'pai', 'mike', 'jack', 'carlos', 'julio'])


# -------------------------------------------------------------------------
# BLOCO 4: A "MEMÓRIA" DOS NPCs
# -------------------------------------------------------------------------
# APLICAÇÃO (Tabela Hash de Listas): [cite: pdf 4 26481138.pdf], [cite: pdf 1. 27070497.pdf]
# 'Chave' = ID do NPC, 'Valor' = Lista de memórias.
db_memoria_npcs = {
    'mae': [], 'pai': [], 'mike': [], 'jack': [], 'carlos': [], 'julio': []
}

# -------------------------------------------------------------------------
# BLOCO 5: O "PALCO" (Cenários)
# -------------------------------------------------------------------------
# APLICAÇÃO (Tabela Hash): A "Lista de Cenários".
# [cite: pdf 4 26481138.pdf]
# Adicionamos todos os 6 cenários da casa + 5 locais externos.
db_cenarios = {
    # --- Casa (6 Cenários) ---
    'quarto_yumi': {
        'nome_exibicao': 'Quarto da Yumi',
        'descricao': 'Seu quarto. Um lugar seguro.',
        'passagens': {'corredor_casa': 'Sair para o Corredor'},
        'eventos_locais': ['ler_livro_escrivaninha'] # Gatilhos de eventos
    },
    'corredor_casa': {
        'nome_exibicao': 'Corredor',
        'descricao': 'O corredor principal da casa.',
        'passagens': {
            'quarto_yumi': 'Entrar no seu Quarto',
            'quarto_irmaos': 'Entrar no Quarto dos Irmãos',
            'quarto_casal': 'Entrar no Quarto dos Pais',
            'banheiro': 'Entrar no Banheiro',
            'cozinha': 'Ir para a Cozinha',
            'sala_estar': 'Ir para a Sala de Estar',
            'rua': 'Sair de Casa' # CORREÇÃO: Sair de casa leva diretamente para a 'rua'.
        },
        'eventos_locais': ['espiar_porta_pais']
    },
    'quarto_irmaos': {
        'nome_exibicao': 'Quarto de Mike e Jack',
        'descricao': 'Uma bagunça de videogames e roupas. Mike e Jack estão aqui.',
        'passagens': {'corredor_casa': 'Voltar para o Corredor'},
        'eventos_locais': ['pedir_para_jogar_videogame']
    },
     'quarto_casal': {
        'nome_exibicao': 'Quarto dos Pais',
        'descricao': 'O quarto de seus pais. Está muito arrumado.',
        'passagens': {'corredor_casa': 'Voltar para o Corredor'},
        'eventos_locais': []
    },
    'cozinha': {
        'nome_exibicao': 'Cozinha',
        'descricao': 'O cheiro de café é forte.',
        'passagens': {'corredor_casa': 'Voltar para o Corredor', 'sala_estar': 'Ir para a Sala'},
        'eventos_locais': ['tomar_cafe']
    },
    'sala_estar': {
        'nome_exibicao': 'Sala de Estar',
        'descricao': 'A TV está ligada em um jogo de futebol.',
        'passagens': {'corredor_casa': 'Voltar para o Corredor', 'cozinha': 'Ir para a Cozinha'},
        'eventos_locais': []
    },
    'banheiro': {
        'nome_exibicao': 'Banheiro',
        'descricao': 'O espelho está um pouco manchado.',
        'passagens': {'corredor_casa': 'Sair para o Corredor'},
        'eventos_locais': ['tomar_banho', 'se_maquiar']
    },
    
    # --- Externo (5 Cenários) ---
    'rua': {
        'nome_exibicao': 'Rua',
        'descricao': 'A rua da sua casa.',
        'passagens': {
            'corredor_casa': 'Entrar em Casa', # CORREÇÃO: Entrar em casa leva para o 'corredor_casa'.
            'escola': 'Ir para a Escola',
            'lanchonete': 'Ir para a Lanchonete',
            'shopping': 'Ir para o Shopping'
        },
        'eventos_locais': []
    },
    'escola': { 'nome_exibicao': 'Escola', 'descricao': 'Colégio...','passagens': {'rua': 'Sair'}, 'eventos_locais': []},
    'lanchonete': { 'nome_exibicao': 'Lanchonete/Bar', 'descricao': 'O cheiro de fritura é forte.','passagens': {'rua': 'Sair'}, 'eventos_locais': ['pedir_emprego']},
    'shopping': { 'nome_exibicao': 'Shopping', 'descricao': 'Muitas lojas.','passagens': {'rua': 'Sair'}, 'eventos_locais': ['comprar_roupa']},
    'praia': { 'nome_exibicao': 'Praia', 'descricao': 'O som do mar.','passagens': {'rua': 'Sair'}, 'eventos_locais': []},
    'cinema': { 'nome_exibicao': 'Cinema', 'descricao': 'Escuro e com cheiro de pipoca.','passagens': {'rua': 'Sair'}, 'eventos_locais': []},
    # Local "falso" para onde os NPCs vão quando não estão no mapa
    'trabalho': { 'nome_exibicao': 'Trabalho', 'descricao': 'Fora do mapa','passagens': {}, 'eventos_locais': []},
}

# -------------------------------------------------------------------------
# BLOCO 6: A "FILA DE EVENTOS"
# -------------------------------------------------------------------------
# APLICAÇÃO (Lista Linear / Fila): [cite: pdf 1. 27070497.pdf]
# Este é o "coração" das suas "ações em cadeia".
# O jogo lê o primeiro item, executa, e o remove.
# Eventos podem adicionar mais eventos a esta fila.
fila_eventos = [
    # Ex: {'tipo': 'dialogo', 'npc_id': 'mae', 'no_dialogo': 'inicio'}
    # Ex: {'tipo': 'cena', 'midia_id': 'foto_irmaos_pegadinha'}
    # Ex: {'tipo': 'acao_yumi', 'acao': 'correr_para_quarto'}
]

# -------------------------------------------------------------------------
# BLOCO 7: A "Biblioteca de Mídia" (Imagens, GIFs, Vídeos)
# -------------------------------------------------------------------------
# APLICAÇÃO (Tabela Hash): [cite: pdf 4 26481138.pdf]
# "Fácil de inserir": Só adicionar uma nova 'chave' e 'valor' aqui.
db_midia = {
    'pegadinha_mike_1': {
        'tipo': 'gif',
        'url': 'https://placehold.co/600x400/000000/FFFFFF?text=GIF+da+Pegadinha+do+Mike'
    },
    'foto_julio_atrevido': {
        'tipo': 'imagem',
        'url': 'https://placehold.co/600x400/333333/FFFFFF?text=Foto+do+Julio+sendo+Atrevido'
    }
}
