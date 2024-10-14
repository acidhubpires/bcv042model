import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv, find_dotenv
import os
import json

# Carrega variáveis de ambiente
_ = load_dotenv(find_dotenv())

# Chave da API protegida (pegando a chave do arquivo .env)
groq_api_key = os.getenv("GROQ_API_KEY")

# Inicializa o modelo llama3 com a chave API
chat = ChatGroq(temperature=0.7, model_name="llama-3.2-3b-preview", api_key=groq_api_key)

# Título do app
st.title("BCVM42Model by Geotoken")

# Estado de sessão para rastrear o nome do usuário e interações
if "name" not in st.session_state:
    st.session_state.name = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = 0

# Função para configurar o sistema de prompt com restrições de contexto para o modelo Verra VM0042
def get_system_prompt():
    return """
    Você é um especialista em modelagem matemática de projetos de créditos de carbono, especialmente seguindo a metodologia VM0042 da Verra.
    Sua função é auxiliar em questões técnicas relacionadas à geração de créditos de carbono no contexto do agronegócio, incluindo:
    - Cálculos de sequestro de carbono
    - Monitoramento, Relatório e Verificação (MRV) em projetos de carbono
    - Modelos de baseline para reduções de emissões
    - Certificação e verificação de créditos de carbono
    - Aplicações da metodologia VM0042 no setor agrícola e florestal

    Não responda perguntas que estejam fora do escopo de carbono, agricultura ou a metodologia Verra VM0042. Se o usuário fizer uma pergunta fora do contexto, gentilmente informe que só pode responder questões relacionadas a esses temas.
    """

# Fluxo inicial: Nome do usuário
if not st.session_state.name:
    st.session_state.name = st.text_input("Olá! Qual é o seu nome?", key="name_input")

# Exibe mensagem de boas-vindas e perguntas pré-definidas após inserir o nome
if st.session_state.name:
    st.write(f"Bem-vindo, {st.session_state.name}! Este assistente responde a perguntas relacionadas à metodologia VM0042 da Verra e créditos de carbono no agronegócio.")

    # Verificar se restam duas perguntas e mostrar um aviso
    if st.session_state.questions_asked == 8:
        st.warning("Atenção! Você tem apenas mais 2 perguntas antes de finalizar o acesso.")

    # Limita o número de perguntas para 10 por sessão
    if st.session_state.questions_asked < 10:
        # Opções de perguntas pré-definidas focadas em créditos de carbono e agronegócios
        questions = [
            "Como posso calcular o sequestro de carbono em um projeto agrícola?",
            "Quais são os principais componentes do MRV na metodologia VM0042?",
            "Como determinar o baseline para reduções de emissões em projetos de carbono?",
            "Quais são os critérios para certificação de créditos de carbono no setor agrícola?",
            "Como aplicar a metodologia VM0042 em projetos florestais?"
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
