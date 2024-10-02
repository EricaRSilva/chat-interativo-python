#Título: Chat
# Botão: iniciar chat
# Alerta (popup)
    # Título: Bem vindo ao Chat
    # Campo de texto: Escreva seu nome no chat
    # Botão: Entrar no chat
        # Sumir com o título e o botão inical
        # Fechar o alerta
        # Criar o chat (com a mensagem de "nome do usuario entrou o chat")
            # Embaixo do chat:
            # Campo de texto: Digite sua mensagem
            # Botão Enviar 
                # Vai aparecer a mensagem no chat com o nome do usuario


import flet as ft

# Definindo a classe ChatMessage
class ChatMessage(ft.Row):
    def __init__(self, user_name: str, text: str):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START # alinhamento
        self.spacing = 10 # espaçamento entre o avatar e a mensagem
       
        # Definir avatar e nome do usuário com mensagem
        self.controls=[
                ft.CircleAvatar(
                    content=ft.Text(self.get_initials(user_name), color=ft.colors.WHITE),
                    color=ft.colors.WHITE,
                    radius=20, # tamanho do avatar
                    bgcolor=self.get_avatar_color(user_name),
                ),
                ft.Column(
                    [
                        ft.Text(user_name, weight="bold"),  # nome usuário
                        ft.Text(text, selectable=True),
                    ],
                    spacing=5,
                ),
            ]

    def get_initials(self, user_name: str):
        # retorna a primeira letra do nome como inicial
        return user_name[:1].capitalize()

    def get_avatar_color(self, user_name: str):
        # escolher uma cor baseada no nome do usuário
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


# Função principal do sistema
def main(pagina):
    texto = ft.Text("Chat Interativo", size=24, weight="bold")

    chat = ft.Column(scroll="auto", expand=True)

    nome_usuario = ft.TextField(label="Escreva seu nome", autofocus=True)


    # socket (tunel de comunicação entre vários usuários)  
    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]
          # adicionar a mensagem no chat
            chat.controls.append(ft.Text(f"{usuario_mensagem}: {texto_mensagem}"))   
        else:
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{usuario_mensagem} entrou no chat", 
                                         size=12, italic=True, color=ft.colors.WHITE))
        pagina.update()

    pagina.pubsub.subscribe(enviar_mensagem_tunel) 

# Função para enviar uma nova mensagem ao apertar o botão ou "Enter"
    def enviar_mensagem(evento):
         # enviar mensagem no tunel
        pagina.pubsub.send_all({"texto": campo_mensagem.value, "usuario": nome_usuario.value,
                                "tipo":"mensagem"})
        # limpar o campo de mensagem
        campo_mensagem.value = ""
        pagina.update()

    campo_mensagem = ft.TextField(label="Digite sua mensagem", on_submit=enviar_mensagem)
    botao_enviar_mensagem = ft.ElevatedButton("Enviar", on_click=enviar_mensagem)

    def entrar_popup(evento):
        pagina.pubsub.send_all({"usuario": nome_usuario.value, "tipo": "entrada"})
        # criar o chat
        pagina.add(chat)
        # fechar o popup
        popup.open = False
        # remover o botão iniciar chat
        pagina.remove(botao_iniciar)
        pagina.remove(texto)
        # criar o campo de mensagem do usuario
        # criar o botao de enviar mensagem do usuario
        pagina.add(ft.Row(
            [campo_mensagem, botao_enviar_mensagem]
        ))
        pagina.update()
        
    #arquivo = ft.FilePicker() # enviar arquivos no chat
        
    # Configuração do popup de entrada
    popup = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text("Bem vindo ao Chat Interativo"),
        content=nome_usuario,
        actions=[ft.ElevatedButton("Entrar",on_click=entrar_popup)],
        )

    pagina.bgcolor = "#ff6f91" #cor fundo da página

     # Função que exibe o popup para inserir o nome do usuário
    def entrar_chat(evento):
        pagina.dialog = popup
        popup.open = True
        pagina.update()

    botao_iniciar = ft.ElevatedButton("Iniciar chat", on_click=entrar_chat)

    pagina.add(texto)
    pagina.add(botao_iniciar)


# deploy
ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8000)
