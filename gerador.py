from time import localtime, strftime, sleep
from colorama import init, Fore
import requests
import random
import string
import os

# Inicializa o colorama
init(autoreset=True)

# Função para alternar as cores
def alternating_colors(text):
    color_sequence = [Fore.MAGENTA, Fore.BLACK, Fore.BLUE]  # Rosa, Preto, Azul
    result = ""
    for i, char in enumerate(text):
        result += color_sequence[i % len(color_sequence)] + char
    return result

# Adiciona a impressão do título no início do código
def print_title():
    title = """
   _____ ______ _____            _____   ____  _____      _   _ _____ _______ _____   ____  
  / ____|  ____|  __ \     /\   |  __ \ / __ \|  __ \    | \ | |_   _|__   __|  __ \ / __ \ 
 | |  __| |__  | |__) |   /  \  | |  | | |  | | |__) |   |  \| | | |    | |  | |__) | |  | |
 | | |_ |  __| |  _  /   / /\ \ | |  | | |  | |  _  /    | . ` | | |    | |  |  _  /| |  | |
 | |__| | |____| | \ \  / ____ \| |__| | |__| | | \ \    | |\  |_| |_   | |  | | \ \| |__| |
  \_____|______|_|  \_\/_/    \_\_____/ \____/|_|  \_\   |_| \_|_____|  |_|  |_|  \_\\____/ 
    """
    print(alternating_colors(title))

# Exibe o título ao iniciar o programa
print_title()

class SapphireGen:
    def __init__(this, code_type: str, prox=None, codes=None):
        this.type = code_type
        this.codes = codes
        this.proxies = prox
        this.session = requests.Session()
        this.prox_api = (
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        )

    def __proxies__(this):
        req = this.session.get(this.prox_api).text
        if req:
            open("./data/proxies.txt", "a+").truncate(0)
            for proxy in req.split("\n"):
                proxy = proxy.strip()
                proxy = f"https://{proxy}"
                open("./data/proxies.txt", "a").write(f"{proxy}\n")

    def generate(this, scrape=None):
        if scrape == "True":
            this.__proxies__()

        os.system("clear")
        for _ in range(int(this.codes)):
            try:
                if this.proxies == "True":
                    prox = {
                        "http": random.choice(
                            open("./data/proxies.txt", "r").read().splitlines()
                        )
                    }
                else:
                    prox = None

                if this.type == "boost":
                    code = "".join(
                        [
                            random.choice(string.ascii_letters + string.digits)
                            for i in range(24)
                        ]
                    )
                else:
                    code = "".join(
                        [
                            random.choice(string.ascii_letters + string.digits)
                            for i in range(16)
                        ]
                    )
                req = this.session.get(
                    f"https://discordapp.com/api/entitlements/gift-codes/{code}",
                    proxies=prox,
                    timeout=10,
                ).status_code
                if req == 200:
                    print(
                        alternating_colors(f"[{strftime('%H:%M', localtime())}] discord.gift/{code} | válido")
                    )
                    open("./data/valid.txt", "a").write(f"{code}\n")
                if req == 404:
                    print(
                        alternating_colors(f"[{strftime('%H:%M', localtime())}] discord.gift/{code} | inválido")
                    )
                if req == 429:
                    print(
                        alternating_colors(f"[{strftime('%H:%M', localtime())}] discord.gift/{code} | taxa limitada")
                    )
            except Exception as e:
                print(alternating_colors(f"[{strftime('%H:%M', localtime())}] {e}"))

        print(
            alternating_colors(f"[{strftime('%H:%M', localtime())}] Verificação concluída com sucesso: {this.codes} códigos.")
        )
        sleep(1.5)
        os.system("clear")

if __name__ == "__main__":
    while True:
        code_type = input(
            alternating_colors(f"[{strftime('%H:%M', localtime())}] Tipo de Código (boost, classic): ")
        )
        prox = input(
            alternating_colors(f"[{strftime('%H:%M', localtime())}] Usar proxies? (True, False): ")
        )
        if prox == "True":
            scrape_proxy = input(
                alternating_colors(f"[{strftime('%H:%M', localtime())}] Coletar proxies? (True, False): ")
            )
        else:
            scrape_proxy = False
        codes = input(
            alternating_colors(f"[{strftime('%H:%M', localtime())}] Número de códigos: ")
        )
        SapphireGen(code_type, prox, codes).generate(scrape=scrape_proxy)
