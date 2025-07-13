import requests
import xml.etree.ElementTree as ET
import json
import os

ARQUIVO_ESTRELAS = "estrelas_pesquisadas.json"

class MedidorEstelar:
    def __init__(self, nome, luminosidade=None, distancia=None, massa=None, temperatura=None, tipo_espectral=None):
        self.nome = nome
        self.luminosidade = luminosidade
        self.distancia = distancia
        self.massa = massa
        self.temperatura = temperatura
        self.tipo_espectral = tipo_espectral

    def exibir_dados(self):
        print(f"\n🔭 Dados da Estrela: {self.nome}")
        print(f"Luminosidade: {self.luminosidade if self.luminosidade is not None else 'N/D'} L☉")
        print(f"Distância: {self.distancia if self.distancia is not None else 'N/D'} anos-luz")
        print(f"Massa: {self.massa if self.massa is not None else 'N/D'} M☉")
        print(f"Temperatura: {self.temperatura if self.temperatura is not None else 'N/D'} K")
        print(f"Tipo espectral: {self.tipo_espectral if self.tipo_espectral else 'N/D'}")
        print(f"Classificação estelar: {self.classificar_estrelas()}")

    def classificar_estrelas(self):
        if self.temperatura is None:
            return "N/D"
        if self.temperatura >= 30000:
            return "Tipo O (azul)"
        elif self.temperatura >= 10000:
            return "Tipo B (azul-branca)"
        elif self.temperatura >= 7500:
            return "Tipo A (branca)"
        elif self.temperatura >= 6000:
            return "Tipo F (branco-amarelada)"
        elif self.temperatura >= 5200:
            return "Tipo G (amarela - como o Sol)"
        elif self.temperatura >= 3700:
            return "Tipo K (laranja)"
        else:
            return "Tipo M (vermelha)"

def carregar_estrelas():
    if os.path.exists(ARQUIVO_ESTRELAS):
        with open(ARQUIVO_ESTRELAS, "r") as f:
            return json.load(f)
    return []

def salvar_estrelas(estrelas):
    with open(ARQUIVO_ESTRELAS, "w") as f:
        json.dump(estrelas, f, indent=4, ensure_ascii=False)

def buscar_estrela_simbad(nome_estrela):
    url = "http://simbad.u-strasbg.fr/simbad/sim-id"
    params = {
        "output.format": "VOTable",
        "Ident": nome_estrela
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(" Erro ao acessar a API:", e)
        return None

    try:
        root = ET.fromstring(response.text)
        ns = {'v': 'http://www.ivoa.net/xml/VOTable/v1.1'}

        rows = root.findall('.//v:TABLEDATA/v:TR', ns)
        if not rows:
            return None

        row = rows[0]
        dados = [td.text for td in row.findall('v:TD', ns)]

        tipo_espectral = dados[8] if len(dados) > 8 else None
        nome = dados[0] if len(dados) > 0 else nome_estrela

        parallax_str = dados[14] if len(dados) > 14 else None
        distancia_ly = None
        if parallax_str and parallax_str != '':
            try:
                parallax = float(parallax_str)
                if parallax > 0:
                    distancia_pc = 1 / parallax
                    distancia_ly = round(distancia_pc * 3.26156, 2)
            except:
                pass

        estrela = MedidorEstelar(nome=nome, distancia=distancia_ly, tipo_espectral=tipo_espectral)
        return estrela

    except ET.ParseError:
        return None

def listar_estrelas_registradas(estrelas):
    if not estrelas:
        print("\n Nenhuma estrela registrada ainda.")
        return

    print("\n Estrelas registradas:")
    for i, e in enumerate(estrelas, 1):
        print(f"{i}. Nome: {e.get('nome','N/D')}")
        print(f"    Distância: {e.get('distancia','N/D')} anos-luz")
        print(f"    Tipo espectral: {e.get('tipo_espectral','N/D')}")
        print(f"    Luminosidade: {e.get('luminosidade','N/D')} L☉")
        print(f"    Massa: {e.get('massa','N/D')} M☉")
        print(f"    Temperatura: {e.get('temperatura','N/D')} K\n")

def escolher_estrela_pre_definida():
   
    estrelas_famosas = [
        MedidorEstelar("Sirius", luminosidade=25.4, distancia=8.6, massa=2.1, temperatura=9940, tipo_espectral="A1V"),
        MedidorEstelar("Betelgeuse", luminosidade=126000, distancia=642.5, massa=20, temperatura=3500, tipo_espectral="M1-2Ia-ab"),
        MedidorEstelar("Rigel", luminosidade=120000, distancia=860, massa=21, temperatura=11000, tipo_espectral="B8Ia"),
        MedidorEstelar("Proxima Centauri", luminosidade=0.0017, distancia=4.24, massa=0.12, temperatura=3042, tipo_espectral="M5.5Ve"),
        MedidorEstelar("Vega", luminosidade=40.12, distancia=25.04, massa=2.1, temperatura=9602, tipo_espectral="A0V"),
    ]

    print("\n✨ Escolha uma estrela famosa para consultar:")
    for i, estrela in enumerate(estrelas_famosas, 1):
        print(f"{i} - {estrela.nome}")

    escolha = input("Digite o número da estrela (ou 0 para cancelar): ").strip()
    if escolha.isdigit():
        escolha_num = int(escolha)
        if 1 <= escolha_num <= len(estrelas_famosas):
            return estrelas_famosas[escolha_num - 1]
    print("Opção inválida ou cancelada.")
    return None

def menu():
    estrelas_pesquisadas = carregar_estrelas()

    while True:
        print("\n MENU")
        print("1 - Pesquisar estrela na SIMBAD")
        print("2 - Escolher estrela famosa para consultar")
        print("3 - Listar estrelas registradas")
        print("4 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input(" Digite o nome da estrela: ").strip()
            estrela = buscar_estrela_simbad(nome)
            if estrela:
                estrela.exibir_dados()
                estrelas_pesquisadas.append({
                    "nome": estrela.nome,
                    "distancia": estrela.distancia,
                    "tipo_espectral": estrela.tipo_espectral,
                    "luminosidade": estrela.luminosidade,
                    "massa": estrela.massa,
                    "temperatura": estrela.temperatura
                })
                salvar_estrelas(estrelas_pesquisadas)
            else:
                print(" Nenhum dado encontrado para essa estrela na SIMBAD.")
        elif opcao == "2":
            estrela = escolher_estrela_pre_definida()
            if estrela:
                estrela.exibir_dados()
                estrelas_pesquisadas.append({
                    "nome": estrela.nome,
                    "distancia": estrela.distancia,
                    "tipo_espectral": estrela.tipo_espectral,
                    "luminosidade": estrela.luminosidade,
                    "massa": estrela.massa,
                    "temperatura": estrela.temperatura
                })
                salvar_estrelas(estrelas_pesquisadas)
        elif opcao == "3":
            listar_estrelas_registradas(estrelas_pesquisadas)
        elif opcao == "4":
            print(" Encerrando programa. Até logo!")
            break
        else:
            print(" Opção inválida. Tente novamente.")
if __name__ == "__main__":
    menu()

