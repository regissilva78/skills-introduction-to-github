# Arquivo: app.py
#
# =========================================================================
# == TUTORIAL PASSO A PASSO: O "MOTOR" DO JOGO (O Game Engine) ==
# =========================================================================
#
# Objetivo: Conter toda a "LÓGICA" do jogo.
# Matéria Aplicada: Controle de Fluxo (if/for) [cite: pdf 2 fluxo ddo código 47479430.pdf],
#                  Lógica de Pandas [cite: pdf 4 dataflame 47480719.pdf],
#                  Processamento de Fila/Pilha [cite: pdf 1. 27070497.pdf]
#
# Este arquivo "lê" o banco de dados (mundo_jogo.py) e toma decisões.
# =========================================================================

from flask import Flask, jsonify, render_template, request
import mundo_jogo # Importa nosso "Banco de Dados Central"
import pandas as pd
import dialogos # Importa os diálogos
import json # Para salvar/carregar

app = Flask(__name__)

# ---
# FUNÇÃO 1: Carregar o Jogo (O Palco) - (Sem mudanças)
# ---
@app.route('/')
def carregar_jogo():
    return render_template('index.html')


# ---
# FUNÇÃO 2: Pegar o Estado ATUAL do Jogo
# ---
@app.route('/get_estado_jogo', methods=['GET'])
def get_estado_jogo():
    """
    Envia o "estado" completo do mundo para o JavaScript desenhar.
    """
    
    # 1. Pega o local atual da Yumi
    local_id = mundo_jogo.estado_yumi['local_atual']
    
    # 2. Pega os dados deste local (Tabela Hash)
    dados_cenario_atual = mundo_jogo.db_cenarios[local_id]
    
    # 3. ACHAR NPCs NO LOCAL (Consulta no DataFrame)
    npcs_no_local = mundo_jogo.db_npcs[
        mundo_jogo.db_npcs['local_atual'] == local_id
    ]
    
    # 4. Envia tudo para o HTML
    return jsonify({
        'mundo': mundo_jogo.estado_mundo,
        'yumi_status': mundo_jogo.db_yumi_status.to_dict(),
        'yumi_estado': mundo_jogo.estado_yumi,
        'cenario_atual': dados_cenario_atual,
        'npcs_presentes': npcs_no_local.to_dict('index'),
        'eventos_na_fila': mundo_jogo.fila_eventos 
    })

# ---
# FUNÇÃO 3: O "CORAÇÃO" DO JOGO (Game Loop)
# ---
@app.route('/avancar_tempo', methods=['POST'])
def avancar_tempo():
    """
    Esta é a função MAIS IMPORTANTE. 
    É o "motor" que roda o jogo. Custa 30 min.
    """
    
    # 1. AVANÇAR O RELÓGIO (custa 30 min, como você pediu)
    mundo_jogo.estado_mundo['minuto'] += 30
    if mundo_jogo.estado_mundo['minuto'] >= 60:
        mundo_jogo.estado_mundo['minuto'] = 0
        mundo_jogo.estado_mundo['hora'] += 1
    
    if mundo_jogo.estado_mundo['hora'] >= 24:
        mundo_jogo.estado_mundo['hora'] = 0
        
        # Lógica para avançar o dia da semana
        dias_semana = ['segunda-feira', 'terca-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sabado', 'domingo']
        dia_atual = mundo_jogo.estado_mundo['dia_semana']
        
        # Encontra o índice do dia atual e calcula o próximo
        indice_atual = dias_semana.index(dia_atual)
        proximo_indice = (indice_atual + 1) % len(dias_semana) # O % garante o loop (domingo -> segunda)
        
        mundo_jogo.estado_mundo['dia_semana'] = dias_semana[proximo_indice]
        
    # 2. ATUALIZAR O PERÍODO do dia
    hora = mundo_jogo.estado_mundo['hora']
    if 6 <= hora < 12: mundo_jogo.estado_mundo['periodo'] = 'manha'
    elif 12 <= hora < 18: mundo_jogo.estado_mundo['periodo'] = 'tarde' # [cite: pdf 2 fluxo ddo código 47479430.pdf]
    elif 18 <= hora < 24: mundo_jogo.estado_mundo['periodo'] = 'noite'
    else: mundo_jogo.estado_mundo['periodo'] = 'madrugada'
    
    
    # 3. MOVER NPCs (Lógica de Agendas)
    # APLICAÇÃO: Iterar no DataFrame do Pandas e ler a Tabela Hash de agenda
    periodo_atual = mundo_jogo.estado_mundo['periodo']
    dia_atual = mundo_jogo.estado_mundo['dia_semana']
    
    for npc_id, npc_dados in mundo_jogo.db_npcs.iterrows():
        agenda_npc = npc_dados['agenda']
        # Verifica se existe uma entrada para o dia atual na agenda do NPC
        if dia_atual in agenda_npc:
            agenda_do_dia = agenda_npc[dia_atual]
            # Verifica se existe uma entrada para o período atual na agenda do dia
            if periodo_atual in agenda_do_dia:
                novo_local = agenda_do_dia[periodo_atual]
                mundo_jogo.db_npcs.loc[npc_id, 'local_atual'] = novo_local

    # 4. PROCESSAR "AÇÕES EM CADEIA" (IA e Eventos)
    # APLICAÇÃO: Lógica de Controle de Fluxo [cite: pdf 2 fluxo ddo código 47479430.pdf]
    
    # Regra 1: "Pegadinha dos Irmãos" (Sua ideia)
    # "SE Yumi está na sala_estar E Mike está na sala_estar E Julio está na sala_estar"
    yumi_local = mundo_jogo.estado_yumi['local_atual']
    mike_local = mundo_jogo.db_npcs.loc['mike', 'local_atual']
    julio_local = mundo_jogo.db_npcs.loc['julio', 'local_atual']
    
    if yumi_local == 'sala_estar' and mike_local == 'sala_estar' and julio_local == 'sala_estar':
        # "E SE o evento 'pegadinha_mike_1' AINDA NÃO aconteceu (não está na memória)"
        memoria_mike = mundo_jogo.db_memoria_npcs['mike']
        if not any(mem['id'] == 'pegadinha_mike_1' for mem in memoria_mike):
            
            # GATILHO! Dispara a "Ação em Cadeia"
            print("MOTOR: Gatilho da Pegadinha do Mike disparado!")
            
            # APLICAÇÃO (Fila): Adiciona os eventos na Fila de Eventos
            # [cite: pdf 1. 27070497.pdf]
            mundo_jogo.fila_eventos.append({
                'tipo': 'dialogo', 
                'npc_id': 'mike', 
                'dialogo': 'Mike: Ei Yumi, olha isso!'
            })
            mundo_jogo.fila_eventos.append({
                'tipo': 'cena', # Mostra a imagem/gif
                'midia_id': 'pegadinha_mike_1'
            })
            mundo_jogo.fila_eventos.append({
                'tipo': 'dialogo', 
                'npc_id': 'julio', 
                'dialogo': 'Julio: Hahaha! Você caiu direitinho!'
            })
            # APLICAÇÃO (Pilha): Força uma "Ação Autônoma" na Yumi
            # [cite: pdf 1. 27070497.pdf]
            mundo_jogo.fila_eventos.append({
                'tipo': 'acao_yumi',
                'acao': 'correr_para_quarto' # Isso será colocado na pilha da Yumi
            })
            
            # Salva na "Memória" que isso aconteceu
            mundo_jogo.db_memoria_npcs['mike'].append({'id': 'pegadinha_mike_1', 'dia': dia_atual})


    # 5. PROCESSAR A FILA DE EVENTOS E AÇÕES DA YUMI
    # APLICAÇÃO (Pilha): A Yumi "programável"
    # O Motor SEMPRE checa a pilha da Yumi primeiro.
    if mundo_jogo.estado_yumi['pilha_acoes']:
        # Pega a ação do topo da pilha
        acao_autonoma = mundo_jogo.estado_yumi['pilha_acoes'].pop(0) # Usando como Fila, na verdade
        
        if acao_autonoma == 'correr_para_quarto':
            mundo_jogo.estado_yumi['local_atual'] = 'quarto_yumi'
            mundo_jogo.db_yumi_status['trauma'] += 1 # Ação autônoma afeta status
            
            # Adiciona um evento de "feedback"
            mundo_jogo.fila_eventos.insert(0, {
                'tipo': 'notificacao',
                'texto': 'Você correu para o seu quarto, furiosa!'
            })
    
    
    # 6. Retorna o NOVO estado do jogo para o JavaScript
    # (O JS vai chamar 'get_estado_jogo' de novo para redesenhar tudo)
    return jsonify({'status': 'tempo_avancado'})


# ---
# FUNÇÃO 4: Mudar de Cenário (Controlado pelo Jogador)
# ---
@app.route('/mudar_cenario', methods=['POST'])
def mudar_cenario():
    novo_local_id = request.json['novo_local_id']

    # Não deixa o jogador se mover se ele tiver uma "Ação Autônoma" na pilha
    if mundo_jogo.estado_yumi['pilha_acoes']:
         return jsonify({'error': 'Yumi não está no controle agora!'}), 403
         
    # Custa 30 mins para se mover
    avancar_tempo() 
    
    mundo_jogo.estado_yumi['local_atual'] = novo_local_id
    print(f"Servidor: Yumi se moveu para '{novo_local_id}'.")
    
    # Retorna o estado completo após a mudança
    return get_estado_jogo()

# ---
# FUNÇÃO 5: Salvar e Carregar (Lógica será no JavaScript/Firestore)
# ---
# O Python não precisa de rotas de salvar/carregar
# O JavaScript vai fazer isso direto no Firestore.


# --- COMANDO PARA RODAR O SERVIDOR ---
if __name__ == '__main__':
    print("--- Servidor do Jogo TCC (Python) Iniciado ---")
    print("--- Acesse http://127.0.0.1:5000 no seu navegador ---")
    app.run(debug=True, port=5000)
