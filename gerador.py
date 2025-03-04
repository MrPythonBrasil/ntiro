from time import localtime, strftime, sleep
from colorama import init, Fore
import requests
import random
import string
import os

# Inicializa o colorama
init(autoreset=True)

# Função para gerar um código aleatório baseado no tipo
def generate_code(code_type):
    if code_type == "boost":
        return "".join(random.choices(string.ascii_letters + string.digits, k=24))
    else:
        return "".join(random.choices(string.ascii_letters + string.digits, k=16))

# Função para exibir uma mensagem de boas-vindas com título "NITRO"
def print_welcome_message():
    print(Fore.WHITE + """
  NNN   NNN III  TTTTT  RRRRR   OOO
  NNNN  NNN  I     T    R   R  O   O
  NN NN NNN  I     T    RRRRR  O   O
  NN  NNNNN  I     T    R  R   O   O
  NN   NNNN  III    T    R   R   OOO
    """)
    print(Fore.WHITE + "\nBem-vindo ao gerador de códigos! Vamos tornar isso rápido e fácil para você. 😊\n")

# Função para verificar o status do código
def verify_code(code, proxies=None):
    url = f"https://discordapp.com/api/entitlements/gift-codes/{code}"
    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        if response.status_code == 200:
            return "Válido", Fore.GREEN
        elif response.status_code == 404:
            return "Inválido", Fore.RED
        elif response.status_code == 429:
            return "Taxa limitada. Oops, vamos dar uma pausa!", Fore.YELLOW
        else:
            return "Erro desconhecido, algo deu errado... 😕", Fore.WHITE
    except Exception as e:
        return f"Erro ao verificar código: {str(e)}. Tente novamente mais tarde!", Fore.WHITE

# Função principal para gerenciar a entrada e exibição de códigos
def run_code_generator():
    while True:
        print_welcome_message()

        # Tipo de código
        code_type = input(Fore.WHITE + "Escolha o tipo de código que você quer gerar (boost ou classic): ").strip().lower()
        if code_type not in ["boost", "classic"]:
            print(Fore.WHITE + "Ops! Parece que você digitou algo errado. Tente 'boost' ou 'classic'. 🤔")
            continue

        # Usar proxies
        use_proxies = input(Fore.WHITE + "Você gostaria de usar proxies para gerar os códigos? (Sim / Não): ").strip().lower()
        proxies = None
        if use_proxies == "sim":
            proxies = input(Fore.WHITE + "Digite o proxy que deseja usar (ou pressione Enter para não usar nenhum): ").strip()
            if proxies:
                proxies = {"http": proxies}
            else:
                proxies = None

        # Número de códigos
        try:
            num_codes = int(input(Fore.WHITE + "Quantos códigos você quer gerar? "))

            if num_codes <= 0:
                print(Fore.WHITE + "Hum, parece que você não quer gerar nenhum código... 😅")
                continue
        except ValueError:
            print(Fore.WHITE + "Ei, você precisa digitar um número válido. 😅")
            continue

        # Gerando e verificando os códigos
        print(Fore.WHITE + f"\nEstamos gerando {num_codes} códigos para você... Vamos lá! 💪\n")
        for _ in range(num_codes):
            code = generate_code(code_type)
            status, color = verify_code(code, proxies)
            print(color + f"Código gerado: {code} | Status: {status}")
            if color == Fore.GREEN:
                with open("valid_codes.txt", "a") as valid_file:
                    valid_file.write(f"{code}\n")
                    print(Fore.GREEN + f"🎉 Código válido! Adicionamos ao arquivo 'valid_codes.txt'.\n")
            sleep(1)

        # Perguntar se o usuário quer gerar mais códigos
        repeat = input(Fore.WHITE + "\nQuer gerar mais códigos? (Sim / Não): ").strip().lower()
        if repeat != "sim":
            print(Fore.WHITE + "Tudo bem! Obrigado por usar nosso gerador de códigos. Até a próxima! 👋")
            break

if __name__ == "__main__":
    run_code_generator()
