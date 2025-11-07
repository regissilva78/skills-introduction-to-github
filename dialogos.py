# Arquivo: dialogos.py
#
# =========================================================================
# == TUTORIAL PASSO A PASSO: O "ROTEIRO" (Banco de Dados de Diálogos) ==
# =========================================================================
#
# Objetivo: Guardar TODOS os diálogos do jogo.
# Matéria Aplicada: Grafos e Tabelas Hash
#
# COMO FUNCIONA:
# 1. 'GRAFOS_DE_DIALOGO' é uma Tabela Hash (Dicionário). A 'chave' é o ID do NPC.
# 2. O 'valor' é outro Dicionário, que contém o GRAFO de diálogo daquele NPC.
# 3. Cada 'chave' no grafo (ex: 'inicio') é um "Vértice" (um ponto na conversa).
# 4. As 'opcoes' são as "Arestas" (as linhas) que levam a outros vértices.
# 5. O 'app.py' (o Motor) vai ler este arquivo para criar as conversas.
#
# =========================================================================

# Para "facilitar a inserção", copie e cole um bloco de NPC e edite.
GRAFOS_DE_DIALOGO = {
    
    # -------------------------------------------------------------------------
    # NPC: 'mae' (Seu pedido: Diálogo simples e amoroso)
    # -------------------------------------------------------------------------
    'mae': {
        'caracteristica': 'protetora',
        'grafo': {
            
            # --- Vértice Condicional (Amizade Alta) ---
            'inicio_amizade_alta': {
                'dialogo_npc': "Minha estrela! Vendo você, meu dia já fica mais brilhante. Precisa de alguma coisa?",
                'opcoes': [
                    {'texto': "Só queria ver você, mãe. Te amo!", 'leva_para': 'conversa_amigavel'},
                    {'texto': "Na verdade, eu queria um dinheiro...", 'leva_para': 'pedir_dinheiro_sucesso'}
                ]
            },
            
            # --- Vértice 'inicio' ---
            'inicio': {
                'dialogo_npc': "Oi, minha filha. Como você está se sentindo?",
                # 'opcoes' são as Arestas do Grafo. Elas levam para outros Vértices.
                'opcoes': [
                    {'texto': "Estou bem, mãe. Só um pouco cansada.", 'leva_para': 'conversa_amigavel'},
                    {'texto': "Podia estar melhor...", 'leva_para': 'conversa_preocupada'},
                    {'texto': "Mãe... posso sair com minhas amigas hoje à noite?", 'leva_para': 'pedir_para_sair'}
                ]
            },
            
            # --- Vértice 'conversa_amigavel' ---
            'conversa_amigavel': {
                'dialogo_npc': "Entendo, querida. Lembre-se de descansar, sim? Eu te amo.",
                'opcoes': [
                    {'texto': "Também te amo, mãe.", 'leva_para': 'fim_conversa'}
                ]
                # Efeitos para este nó podem ser adicionados aqui se forem gerais ao entrar no nó
            },
            
            # --- Vértice 'conversa_preocupada' ---
            'conversa_preocupada': {
                'dialogo_npc': "Oh, meu bem... Aconteceu alguma coisa na escola? Você sabe que pode me contar tudo.",
                'opcoes': [
                    {'texto': "Não foi nada, é sério. Só drama de adolescente.", 'leva_para': 'fim_conversa', 'efeitos': {'npc_estado_emocional': 'preocupada'}},
                ],
            },

            # --- Vértice de "Gatilho de Roupa" (Sua ideia) ---
            'reacao_roupa_vulgar': {
                # O 'app.py' (Motor) vai forçar a conversa a vir para cá
                # se a Yumi falar com a mãe usando roupa Categoria E.
                'dialogo_npc': "Yumi! O que é isso que você está vestindo dentro de casa? É completamente inapropriado! Vá se trocar!",
                'opcoes': [
                    {'texto': "Ah, mãe, é só uma roupa...", 'leva_para': 'fim_conversa'},
                    {'texto': "(Ignorar e sair)", 'leva_para': 'fim_conversa', 'efeitos': {'npc_amizade_yumi': -15}}
                ],
                'efeitos': {'npc_amizade_yumi': -15} # Perde 15 pontos de amizade
            },
            
            # --- Vértice de Resposta ao Pedido de Dinheiro ---
            'pedir_dinheiro_sucesso': {
                'dialogo_npc': "Claro, meu amor. Pegue, mas use com sabedoria, viu?",
                'opcoes': [
                    {'texto': "Obrigada, mãe! Você é a melhor!", 'leva_para': 'fim_conversa', 'efeitos': {'yumi_dinheiro': 50}}
                ]
            },
            
            # --- INÍCIO DA NOVA ÁRVORE DE DIÁLOGO ---
            
            # --- Vértice: O Pedido ---
            'pedir_para_sair': {
                'dialogo_npc': "Sair? Aonde você está pensando em ir e com quem?",
                'opcoes': [
                    # Opção 1: Honesta (leva para o ramo positivo)
                    {'texto': "Vamos ao shopping, com a galera da escola. Prometo não voltar tarde.", 'leva_para': 'resposta_positiva_sair'},
                    # Opção 2: Vaga (leva para o ramo negativo)
                    {'texto': "Ah, por aí. Não sei direito ainda.", 'leva_para': 'resposta_negativa_sair'},
                    # Opção 3: Mentira (leva para o ramo suspeito)
                    {'texto': "Na verdade, vamos para a biblioteca estudar para a prova.", 'leva_para': 'resposta_suspeita_sair'}
                ]
            },
            
            # --- Ramo 1: Resposta Positiva ---
            'resposta_positiva_sair': {
                'dialogo_npc': "Shopping? Tudo bem, minha filha. Confio em você. Mas juízo, e me ligue se precisar de algo!",
                'opcoes': [
                    {'texto': "Obrigada, mãe! Você é a melhor!", 'leva_para': 'fim_conversa', 'efeitos': {'npc_amizade_yumi': 5}}
                ]
            },
            
            # --- Ramo 2: Resposta Negativa ---
            'resposta_negativa_sair': {
                'dialogo_npc': "'Por aí' não é um lugar, Yumi. Se você não pode me dizer onde vai, a resposta é não. Fim de papo.",
                'opcoes': [
                    {'texto': "(Suspira) Tudo bem...", 'leva_para': 'fim_conversa', 'efeitos': {'npc_amizade_yumi': -10, 'npc_estado_emocional': 'irritada'}}
                ]
            },
            
            # --- Ramo 3: Resposta Suspeita ---
            'resposta_suspeita_sair': {
                'dialogo_npc': "Estudar? À noite? ...Certo. Pode ir, mas eu quero você em casa até as 22h em ponto. Entendido?",
                'opcoes': [
                    {'texto': "Entendido. Obrigada, mãe.", 'leva_para': 'fim_conversa'}
                ]
            },
            
            # --- Vértice Final ---
            'fim_conversa': {
                'fim_conversa': True # Sinaliza ao Motor que o diálogo acabou
            }
        }
    },
    
    # -------------------------------------------------------------------------
    # NPC: 'pai' (Seu pedido: Diálogo simples e amoroso)
    # -------------------------------------------------------------------------
    'pai': {
        'caracteristica': 'ocupado',
        'grafo': {
            'inicio': {
                'dialogo_npc': "Oi, princesa. Desculpe a correria, o trabalho está uma loucura. Tudo bem com você?",
                'opcoes': [
                    {'texto': "Tudo bem, pai.", 'leva_para': 'fim_conversa'}
                ]
                # Efeitos para este nó podem ser adicionados aqui
            },
            'fim_conversa': {
                'fim_conversa': True
            }
        }
    },

    # -------------------------------------------------------------------------
    # NPC: 'mike' (Seu pedido: Irmão "Pedra no Sapato" com Julio)
    # -------------------------------------------------------------------------
    'mike': {
        'caracteristica': 'pentelho',
        'grafo': {
            'inicio': {
                'dialogo_npc': "E aí, maninha. Quer ver a gente detonar no videogame?",
                'opcoes': [
                    {'texto': "Sim, eu quero jogar!", 'leva_para': 'pedir_pra_jogar'},
                    {'texto': "Não, vocês são muito barulhentos.", 'leva_para': 'fim_conversa'}
                ]
            },
            
            'pedir_pra_jogar': {
                'dialogo_npc': "Heh. O Julio tá aqui. Você vai ter que provar que é boa. Que tal uma aposta?",
                'opcoes': [
                    {'texto': "Apostado! O que eu ganho?", 'leva_para': 'fim_conversa'},
                    {'texto': "Não quero apostar, só jogar.", 'leva_para': 'fim_conversa'}
                ]
            },
            
            'fim_conversa': {
                'fim_conversa': True
            }
        },
        # APLICAÇÃO: Lógica Condicional no Grafo
        # O Motor vai checar estas regras ANTES de usar o 'inicio' padrão.
        'nos_condicionais': [
            {
                # CONDIÇÃO: Se a amizade com a mãe for maior ou igual a 80...
                'condicao': {'amizade_yumi': '<= 10'},
                # ...então a conversa deve começar pelo nó 'inicio_amizade_alta'.
                'leva_para': 'inicio_amizade_baixa' # Exemplo de um novo nó que você pode criar
            }
        ]
    }
    
    # É FÁCIL ATUALIZAR:
    # Para adicionar o 'julio' ou 'jack', copie o bloco do 'mike' e cole aqui.
}