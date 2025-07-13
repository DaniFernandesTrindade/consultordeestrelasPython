# Medidor Estelar - Consulta de Estrelas com API SIMBAD

Este projeto é um aplicativo em Python para consultar dados de estrelas reais usando a API do banco astronômico SIMBAD e para acessar informações de estrelas famosas pré-definidas.

---

## Funcionalidades

- Pesquisa de estrelas por nome diretamente na API SIMBAD (do Observatório de Estrasburgo).
- Lista de 5 estrelas famosas com dados pré-definidos para consulta rápida.
- Armazenamento local das estrelas pesquisadas em arquivo JSON.
- Exibição formatada das informações da estrela: nome, luminosidade, distância, massa, temperatura e tipo espectral.
- Classificação estelar básica baseada na temperatura da estrela.
- Menu interativo para fácil uso no terminal.

---

## Tecnologias e Bibliotecas

- Python 3.x
- Biblioteca `requests` para chamadas HTTP
- Biblioteca `xml.etree.ElementTree` para parsing dos dados XML da API
- Manipulação de arquivos JSON para salvar e carregar dados localmente

---

## Como usar

1. Clone este repositório:

```bash
git clone https://github.com/seu_usuario/medidor-estelar.git
cd medidor-estelar
