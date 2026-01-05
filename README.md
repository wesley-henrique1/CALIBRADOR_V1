# CALIBRADOR_V1 🦥

Aplicação desktop voltada para a centralização, processamento e análise inteligente de dados logísticos. O sistema consolida fontes heterogêneas (Excel e TXT) para fornecer métricas críticas sobre ocupação e giro de estoque.

## 🚀 Como gerar o executável (.exe)

Para distribuir a aplicação, utilize o **PyInstaller**. Certifique-se de incluir as pastas de recursos.

### Opção A: Arquivo Único (Recomendado para distribuição)
```bash
python -m PyInstaller --onefile --windowed --name=CALIBRADOR_V1 --icon=style/flesh_perfil.ico --add-data "style;style" --add-data "base_dados;base_dados" main.py
```
###  Opção B: Pasta Única (Mais rápido para abrir)
```bash
PyInstaller --onedir --windowed --name=CALIBRADOR_V1 --icon=style/flesh_perfil.ico --add-data "style;style" --add-data "base_dados;base_dados" --add-data "fuctions;fuctions" main.py```

## 📂 Estrutura do Projeto
```bash
CALIBRADOR_V1/
├── main.py                 # Interface Gráfica (Tkinter) e gerenciamento de estados
├── base_dados/             # Fontes de dados (.xlsx, .txt) e mapeamento de caminhos
├── fuctions/
│    └── path_dados.py      # Configuração de caminhos dinâmicos
│    └── logica.py          # Pipeline de ETL e Processamento (Pandas/Numpy)
└── style/                  # Assets visuais (ícones e imagens de fundo)
```

## ⚙️ Regras de Negócio e Métricas
O sistema realiza o cálculo automático das colunas abaixo para subsidiar a tomada de decisão:
| Métrica | Cálculo / Lógica | Objetivo |
| :--- | :--- | :--- |
| **SUG_%** | `SUGESTAO / QTTOTPAL` | Percentual da sugestão de compra em relação à norma do palete. |
| **ATUAL_%** | `CAPACIDADE / QTTOTPAL` | Percentual de ocupação física atual em relação à norma técnica. |
| **SIT_REPOS** | `PONTOREPOSICAO < GIRO_DIA` | Alerta se o estoque de segurança é menor que o consumo diário. |
| **CRIT_CAP** | `GIRO_DIA >= CAPACIDADE` | Alerta de gargalo: a demanda diária supera a capacidade do endereço. |
| **ALERTA_50** | `(GIRO_DIA / CAPACIDADE) > 0.5` | Identifica produtos que consomem mais de 50% da ocupação em um único dia. |
| **FREQ_PROD** | `count(PREDIO)` | Totalizador de endereços/prédios físicos ocupados pelo produto. |


## 🏷️ Classificação de Status (STATUS_PROD)
Define a estratégia de armazenagem com base na frequência de ocupação e tipo de estrutura:

* INT (Inteiro):
    * Condição: Ocupa até 2 prédios (FREQ_PROD <= 2) em estruturas de paletização padrão.
    * Significado: Produto estocado de forma otimizada.

* DIV (Dividido):
    * Condição: Ocupa mais de 3 prédios (FREQ_PROD > 3).
    * Significado: Produto muito fragmentado no armazém; alta necessidade de consolidação.

* VAL (Validar):
    * Condição: Casos de exceção ou endereçamentos que fogem à regra padrão.

## 🛠️ Tecnologias Utilizadas
* Python 3.13

* Pandas & Numpy (Processamento de dados)

* Tkinter (Interface Gráfica)

* Pillow (Manipulação de imagens)

* Openpyxl & Xlrd (Motores de leitura de Excel)

---
## 👤 Desenvolvido por Wesley Oliveira
Conecte-se comigo ou entre em contato para dúvidas e sugestões:

* **LinkedIn:** [Wesley Oliveira](https://www.linkedin.com/in/wesley-henrique22)
* **Instagram:** [@w25_oliveira](https://www.instagram.com/w25_oliveira/)
* **E-mail:** [wesleyhfo123@gmail.com](mailto:wesleyhfo123@gmail.com)