from time import localtime, strftime, sleep
from colorama import init, Fore
import requests
import random
import string
import os

init(autoreset=True)

def generate_code(code_type):
    if code_type == "boost":
        return "".join(random.choices(string.ascii_letters + string.digits, k=24))
    else:
        return "".join(random.choices(string.ascii_letters + string.digits, k=16))

def print_welcome_message():
    print(Fore.WHITE + """
  NNN   NNN III  TTTTT  RRRRR   OOO
  NNNN  NNN  I     T    R   R  O   O
  NN NN NNN  I     T    RRRRR  O   O
  NN  NNNNN  I     T    R  R   O   O
  NN   NNNN  III    T    R   R   OOO
    """)
    print(Fore.WHITE + "\Vamos Gerar Mano.")

def verify_code(code, proxies=None):
    url = f"https://discordapp.com/api/entitlements/gift-codes/{code}"
    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        if response.status_code == 200:
            return "Código válido, como esperado.", Fore.GREEN
        elif response.status_code == 404:
            return "Código inválido. Não era de se esperar?", Fore.RED
        elif response.status_code == 429:
            return "Taxa limitada. Parece que você está tentando demais.", Fore.YELLOW
        else:
            return "Erro. Não é como se você soubesse o que fazer, certo?", Fore.WHITE
    except Exception as e:
        return f"Erro ao verificar o código. Não surpreende. {str(e)}", Fore.WHITE

def run_code_generator():
    while True:
        print_welcome_message()

        code_type = input(Fore.WHITE + "Qual tipo de código você quer gerar? (boost ou classic): ").strip().lower()
        if code_type not in ["boost", "classic"]:
            print(Fore.WHITE + "Você sabe o que está fazendo? Escolha 'boost' ou 'classic'. Não é tão difícil.")
            continue

        use_proxies = input(Fore.WHITE + "Vai usar proxies? (Sim / Não): ").strip().lower()
        proxies = None
        if use_proxies == "sim":
            proxies = input(Fore.WHITE + "Informe o proxy que você deseja usar: ").strip()
            if proxies:
                proxies = {"http": proxies}
            else:
                proxies = None

        try:
            num_codes = int(input(Fore.WHITE + "Quantos códigos você quer gerar? "))

            if num_codes <= 0:
                print(Fore.WHITE + "Você não quer gerar códigos? Que surpresa. Vamos lá, digite algo válido.")
                continue
        except ValueError:
            print(Fore.WHITE + "Você não sabe o que é um número? Digite algo válido.")
            continue

        print(Fore.WHITE + f"\nGerando {num_codes} códigos... Vamos ver o que sai.\n")
        for _ in range(num_codes):
            code = generate_code(code_type)
            status, color = verify_code(code, proxies)
            print(color + f"Código gerado: {code} | Status: {status}")
            if color == Fore.GREEN:
                with open("valid_codes.txt", "a") as valid_file:
                    valid_file.write(f"{code}\n")
                    print(Fore.GREEN + f"Ah, um código válido. Adicionado ao 'valid_codes.txt'. Não é difícil, né?")
            sleep(1)

        repeat = input(Fore.WHITE + "\nQuer gerar mais códigos? (Sim / Não): ").strip().lower()
        if repeat != "sim":
            print(Fore.WHITE + "Beleza, parece que você já cansou. Não sou de forçar nada. Até a próxima.")
            break

if __name__ == "__main__":
    run_code_generator()
