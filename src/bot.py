import telebot
CHVE_API = '5057104135:AAFgQkI4cxDZufLWm7RdUfspaBmJcd0lTrw'

bot = telebot.TeleBot(CHVE_API)

@bot.message_handler(commands=["opcao1"])
def opcao1(mensagem):
    pass

@bot.message_handler(commands=["opcao2"])
def opcao2(mensagem):
    pass
@bot.message_handler(commands=["opcao3"])
def opcao3(mensagem):
    pass

def verificar(mensagem):
    return True

@bot.message_handler(fuc=verificar)
def responder(mensagem):
    texto = """
    Escolha uma opção para continuar (Clique no item):
    /opcao1 Fazer um pedido
    /opcao2 Reclamar de um pedido
    /opcao3 Mandar um abraço pro Bot
    Responder qualque outra coisa não vai funcionar, clique em uma das opções"""
    
    bot.reply_to(mensagem,texto)

bot.polling()

