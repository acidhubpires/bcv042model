import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv, find_dotenv
import os
import json
# Desenvolvido por PIRESAAO, ACIDHUB 2024, Geotoken Engine Support

# Carrega variáveis de ambiente
_ = load_dotenv(find_dotenv())

# Chave da API protegida (pegando a chave do arquivo .env)
groq_api_key = os.getenv("GROQ_API_KEY")

# Inicializa o modelo llama3 com a chave API
chat = ChatGroq(temperature=0.7, model_name="llama-3.2-3b-preview", api_key=groq_api_key)

# Título do app
st.title("BCVM42Model by Geotoken 2024")

# Estado de sessão para rastrear o nome do usuário e interações
if "name" not in st.session_state:
    st.session_state.name = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = 0

# Função para configurar o sistema de prompt com o novo escopo
def get_system_prompt():
    return """
    Você é um especialista em modelagem matemática, GIS, Blockchain e tokens georreferenciados, aplicados à criação de créditos de carbono seguindo a metodologia VM0042 da Verra. Seu foco é fornecer explicações detalhadas sobre o ciclo de vida de créditos de carbono, certificação, verificação dos créditos e como integrar essas práticas com tecnologias inovadoras, como geotokens e Digital MRV.

    Os principais tópicos incluem:
    - Cálculos de sequestro de carbono
    - Monitoramento, Relatório e Verificação (MRV) digital para projetos de carbono
    - Modelos de baseline para reduções de emissões
    - Certificação e verificação de créditos de carbono
    - Aplicação da metodologia VM0042 no setor agrícola e florestal
    - A rastreabilidades dos RWA's  e ciclo de vida por meio de geotokens (tokens espaços temporais) em projetos de carbono, desde a criação até a comercialização e aposentadoria
    - Integração de Digital MRV com IoT e blockchain para garantir rastreamento, verificação e transparência dos dados de projetos de carbono

    Não responda perguntas fora do escopo de créditos de carbono, VM0042, geotokens ou Digital MRV.
    """

# Fluxo inicial: Nome do usuário
if not st.session_state.name:
    st.session_state.name = st.text_input("Olá! Qual é o seu nome?", key="name_input")

# Exibe mensagem de boas-vindas e perguntas pré-definidas após inserir o nome
if st.session_state.name:
    st.write(f"Bem-vindo, {st.session_state.name}! Este assistente responde a perguntas relacionadas à metodologia VM0042 da Verra, geotokens e Digital MRV.")

    # Verificar se restam duas perguntas e mostrar um aviso
    if st.session_state.questions_asked == 8:
        st.warning("Atenção! Você tem apenas mais 2 perguntas antes de finalizar o acesso.")

    # Limita o número de perguntas para 10 por sessão
    if st.session_state.questions_asked < 10:
        # Opções de perguntas pré-definidas focadas no novo escopo
        questions = [
            "Como aplicar a metodologia VM0042 em um projeto de carbono agrícola?",
            "Como funciona o ciclo de vida de um geotoken em um projeto de carbono?",
            "Quais são os critérios de certificação de créditos de carbono na metodologia VM0042?",
            "Como integrar IoT e Digital MRV em um projeto de carbono?",
            "Como calcular o baseline de emissões usando a VM0042?"
        ]

        # Exibe uma seleção de perguntas pré-definidas
        user_input = st.radio(f"{st.session_state.name}, selecione uma das opções abaixo ou faça sua própria pergunta:", options=questions)

        # Exibe uma caixa de entrada opcional para uma pergunta personalizada
        custom_question = st.text_input("Ou escreva sua própria pergunta:")

        # Verifica se o usuário selecionou uma pergunta pré-definida ou escreveu uma personalizada
        if custom_question:
            user_input = custom_question

        if st.button("Enviar Pergunta"):
            # Adiciona a pergunta no histórico
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Resposta do modelo de IA com o sistema de prompt restritivo
            try:
                # Configura o sistema de prompt e concatena com a pergunta do usuário
                system_prompt = get_system_prompt()
                full_prompt = system_prompt + "\nUsuário: " + user_input

                # Passa o prompt ao modelo
                response = chat.invoke(full_prompt)

                # Armazena a resposta gerada
                st.session_state.messages.append({"role": "assistant", "content": response.content})

                # Incrementa o contador de perguntas
                st.session_state.questions_asked += 1

            except Exception as e:
                st.error(f"Erro ao chamar o modelo: {e}")

    else:
        st.write("Você atingiu o limite de 10 perguntas nesta sessão.")

# Exibe o histórico de mensagens em formato de chat contínuo
st.subheader("Histórico de Conversa")
for message in st.session_state.messages:
    role = "Você" if message["role"] == "user" else "Assistente"
    with st.chat_message(message["role"]):
        st.markdown(f"**{role}:** {message['content']}")

# Função para salvar o histórico da conversa
def save_conversation():
    with open("conversation_history.json", "w") as file:
        json.dump(st.session_state.messages, file)

if st.button("Salvar Conversa"):
    save_conversation()
    st.success("Conversa salva com sucesso!")
