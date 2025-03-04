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
    print(Fore.WHITE + "\nVamos lá, não temos todo o tempo do mundo. Escolha o que você quer fazer.\n")

# Função para verificar o status do código
def verify_code(code, proxies=None):
    url = f"https://discordapp.com/api/entitlements/gift-codes/{code}"
    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        if response.status_code == 200:
            return "Código Válido. Surpreso?", Fore.GREEN
        elif response.status_code == 404:
            return "Inútil. Isso nunca vai funcionar.", Fore.RED
        elif response.status_code == 429:
            return "Taxa Limitada. Você já está tentando demais. Tente mais tarde.", Fore.YELLOW
        else:
            return "Erro. Não é como se você soubesse o que fazer, né?", Fore.WHITE
    except Exception as e:
        return f"Erro ao verificar o código. Surpreso? Não sou. {str(e)}", Fore.WHITE

# Função principal para gerenciar a entrada e exibição de códigos
def run_code_generator():
    while True:
        print_welcome_message()

        # Tipo de código
        code_type = input(Fore.WHITE + "Tipo de código? (Escolha 'boost' ou 'classic', se souber o que está fazendo): ").strip().lower()
        if code_type not in ["boost", "classic"]:
            print(Fore.WHITE + "Sério? É simples. Escolha 'boost' ou 'classic'. Vamos lá. 🤦‍♂️")
            continue

        # Usar proxies
        use_proxies = input(Fore.WHITE + "Vai usar proxies? (Sim / Não): ").strip().lower()
        proxies = None
        if use_proxies == "sim":
            proxies = input(Fore.WHITE + "Você realmente acha que sabe o que está fazendo com proxies? (Digite o proxy): ").strip()
            if proxies:
                proxies = {"http": proxies}
            else:
                proxies = None

        # Número de códigos
        try:
            num_codes = int(input(Fore.WHITE + "Quantos códigos você acha que vai conseguir gerar? (Digite um número): "))

            if num_codes <= 0:
                print(Fore.WHITE + "Sem códigos? Claro, sem problemas. Não vou me importar. 😒")
                continue
        except ValueError:
            print(Fore.WHITE + "Ei, você não sabe o que é um número? Digite um número válido. 😏")
            continue

        # Gerando e verificando os códigos
        print(Fore.WHITE + f"\nGerando {num_codes} códigos... Isso vai ser rápido, mas você pode se surpreender. 😏\n")
        for _ in range(num_codes):
            code = generate_code(code_type)
            status, color = verify_code(code, proxies)
            print(color + f"Código gerado: {code} | Status: {status}")
            if color == Fore.GREEN:
                with open("valid_codes.txt", "a") as valid_file:
                    valid_file.write(f"{code}\n")
                    print(Fore.GREEN + f"Uau, um código válido... O que mais você esperava? Adicionado ao 'valid_codes.txt'.\n")
            sleep(1)

        # Perguntar se o usuário quer gerar mais códigos
        repeat = input(Fore.WHITE + "\nQuer gerar mais códigos? (Sim / Não): ").strip().lower()
        if repeat != "sim":
            print(Fore.WHITE + "Então você já cansou, né? Tchau. 👋 Não vai fazer falta.")
            break

if __name__ == "__main__":
    run_code_generator()
