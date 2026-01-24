<div align="center">
  <h1>CALIBRADOR 🦥</h1>
  <img src="Assets\flesh_completo.png" width="200" alt="Flash - O Mascote da Automação">
  <h3>"Deixe o robô trabalhar enquanto você toma um café."</h3>
</div>

![Python](https://img.shields.io/badge/Python-3.13-blue?style=flat&logo=python)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458?style=flat&logo=pandas)
![PowerBI](https://img.shields.io/badge/View-Power_BI-F2C811?style=flat&logo=powerbi)
![Status](https://img.shields.io/badge/Status-Em_Produção-green?style=flat)

> **Automação de Inteligência Logística & Pipeline de ETL**
## 💡 Contexto e Motivação
Como Assistente Logístico focado em expedição e armazenagem, identifiquei um gargalo crítico na rotina de **Calibração de Estoque**. O processo anterior era manual, fragmentado e ineficiente:

* **O Problema:** A geração de relatórios exigia extrair dados de múltiplas rotinas e consolidá-los via "copiar e colar" no Excel.
* **A Dor:** O processo levava de **1 a 2 horas diárias**. Além do tempo perdido, o volume de fórmulas pesadas travava as planilhas, gerando erros de cálculo, perda de dados e falta de confiabilidade.
* **A Solução:** Desenvolvi o **CALIBRADOR_V1**, uma aplicação que substitui o trabalho manual por um pipeline de dados automatizado.

> **Resultado:** O tempo de processamento caiu drasticamente, eliminando erros humanos e liberando tempo para atuar na análise estratégica e no acompanhamento físico do estoque.
---

## 🚀 O Que a Aplicação Faz
O sistema atua como um orquestrador de dados que conecta o operacional à gestão:

1.  **Extração (Extract):** Lê automaticamente arquivos de múltiplas fontes (TXT de sistemas legados e XLSX operacionais).
2.  **Processamento (Transform):** Utiliza **Python (Pandas)** para limpar dados, tratar erros de digitação e cruzar informações (merges).
3.  **Cálculo de KPI:** Aplica regras de negócio complexas (Giro, Ponto de Reposição, Capacidade) que o Excel não suportava com performance.
4.  **Visualização (Load):** Gera uma base consolidada auditável e alimenta um Dashboard no **Power BI**.
---
## 📊 Comparativo: Antes vs. Depois

| Cenário Antigo (Excel Manual) | Cenário Novo (Python Pipeline) |
| :--- | :--- |
| ⏳ 1h a 2h de trabalho manual | ⚡ Processamento em segundos |
| ❌ Travamentos e corrupção de arquivos | ✅ Estabilidade e integridade de dados |
| 📉 Fórmulas quebradas ("#REF!") | 📈 Lógica de cálculo blindada |
| 📋 Foco em *digitar* dados | 🎯 Foco em *analisar* o estoque |

---

## ⚙️ Funcionalidades Técnicas
* **Pipeline de ETL:** Ingestão de 12 fontes de dados simultâneas.
* **Sanitização:** Limpeza automática de *strings*, tratamento de valores nulos (`NaN`) e tipagem de dados.
* **Alertas de Estoque:**

## ⚙️ Engenharia de Dados e KPIs

O pipeline vai além de cálculos simples, aplicando algoritmos de otimização logística para reduzir movimentação desnecessária e prevenir rupturas no processo de expedição.

### 1. Colunas de Suporte (Enriquecimento)
Métricas base para entender a dimensão física do produto no armazém.

| Indicador | Lógica / Cálculo | O que revela? |
| :--- | :--- | :--- |
| **SUG_%** | `SUGESTAO / QTTOTPAL` | Proporção da compra sugerida em relação a um palete fechado. Define se a entrada será armazenada inteira ou fracionada. |
| **ATUAL_%** | `CAPACIDADE / QTTOTPAL` | Nível de ocupação física atual. Indica se o endereço está subutilizado ou superlotado em relação à norma técnica. |
| **FREQ_PROD** | `Count(PREDIO)` | "Vizinhos": Quantas vezes o produto aparece repetido na rua. Alta frequência indica fragmentação excessiva. |

### 2. KPIs de Ruptura e Abastecimento
Focados em garantir que o produto esteja disponível para o separador, prevenindo o *stockout* operacional.

* **⚠️ SIT_REPOS (Risco de Baixa):**
    * *Lógica:* `GIRO_DIA > PONTO_REPOSICAO`
    * *Problema:* O estoque de segurança não suporta a venda diária.
    * *Impacto:* Risco de falta na expedição devido ao *lead time* interno (tempo entre gerar a baixa, empilhadeira descer o aéreo e abastecedor encher o picking).

* **🚨 CRIT_CAP (Gargalo de Capacidade):**
    * *Lógica:* `GIRO_DIA >= CAPACIDADE`
    * *Problema:* A demanda do dia é maior que o tamanho do endereço.
    * *Ação:* Necessário aumentar o *frente* do picking ou alterar o layout ("Ajustar").

* **⚡ ALERTA_50 (Giro Acelerado):**
    * *Lógica:* `(GIRO_DIA / CAPACIDADE) > 0.5`
    * *Problema:* O produto consome mais de 50% do endereço em um único dia.
    * *Impacto:* Gera o "Picking Furado" (vazio constante), exigindo reabastecimentos frenéticos.

### 3. Inteligência de Movimentação (Travel Time)
Algoritmos que analisam se o produto está no local correto da rua para reduzir a caminhada do separador.

* **MED_ACESSO:** Compara os acessos do produto (`ACESSO`) com a média da rua (`MED_RUA`) para classificar como "ACIMA" ou "ABAIXO" da média.
* **📍 ALERTA_MOV (Otimização de Posição):**
    * **UP (Subir):** Produto de **alto giro** localizado no **final da rua**. *Prejuízo: O separador anda a rua toda desnecessariamente.*
    * **DOWN (Descer):** Produto de **baixo giro** no **começo da rua**. *Prejuízo: Ocupa espaço nobre de produtos curva A.*
    * **NORMAL:** Produto posicionado corretamente conforme sua curva ABC.

### 4. Classificação Estratégica (Output Final)

* **📦 STATUS_PROD:** Define a estratégia de armazenagem:
    * `INT` (Inteiro): Produto consolidado (Ocupa até 2 posições).
    * `DIV` (Dividido): Produto fragmentado (Candidato a unificação).
    * `VAL`: Exceção/Validar manualmente.

* **🎯 STATUS_FINAL:** O "Termômetro da Rua". Se *CRIT_CAP*, *SIT_REPOS* e *ALERTA_50* estiverem "NORMAL", a rua está saudável. Caso contrário, sinaliza "DIVERGENTE" para priorizar a atuação do analista.

## 🛠️ Stack Tecnológica

O projeto foi construído inteiramente em **Python 3.13**, utilizando uma arquitetura modular para garantir performance e facilidade de manutenção.

### 📚 Bibliotecas Principais

* **Pandas:** O motor central do ETL. Responsável pela extração, limpeza (sanitização), cruzamento de dados (*merges*) e geração do relatório final auditável.
* **Numpy:** Utilizado para performance matemática. Substitui fórmulas complexas do Excel por cálculos vetoriais e lógica condicional (`np.where`) para criar as colunas de KPI.
* **Tkinter & Messagebox:** Framework para construção da Interface Gráfica (GUI) nativa e sistema de notificações (Alertas de erro/conclusão) para o usuário.

### ⚙️ Engenharia de Software & Sistema

* **Threading:** Implementação de processamento em segundo plano. Garante que a interface **não congele** durante os cálculos pesados, mantendo a responsividade da aplicação.
* **OS:** Gerenciamento dinâmico de diretórios.
    * *Função:* Permite que o software encontre a pasta `base_dados` automaticamente em qualquer máquina, eliminando a necessidade de caminhos fixos (Hardcoded paths).
* **Datetime:** Automação temporal. Sugere automaticamente os intervalos de consulta (períodos de 30 e 90 dias) para facilitar a análise de giro.
* **Warnings:** Controle de logs para manter o console limpo durante a execução do ETL.

---

## 🔮 Roadmap (Próximos Passos)

Visando democratizar o acesso aos dados (já que nem todos os stakeholders possuem licença de **Power BI**), as próximas versões focarão em visualização nativa:

* [ ] **Dashboard Web Integrado:** Substituir a dependência do Power BI por uma interface web leve utilizando **Streamlit**.
* [ ] **Gráficos Interativos:** Implementação de bibliotecas como **Plotly Express** ou **Matplotlib** para gerar gráficos de calor e curvas ABC diretamente na aplicação.

---
## 📂 Estrutura do Projeto

```bash
/
├── assets/             # Recursos visuais (Ícones, Imagens)
├── base_dados/         # Diretório de ingestão (Arquivos .txt e .xlsx)
├── modulos/            # Código-fonte principal
│   ├── _settings.py    # Gerenciamento de diretórios (OS Paths)
│   ├── etl_engine.py   # Motor de processamento de dados (Pandas)
│   └── dashboard.py    # Módulo de visualização (Futuro)
├── main.py             # Orquestrador da aplicação
├──RETORNO.xlsx         # Relatório final consolidado (Output para o usuário)
```
Essa organização separa claramente **Dados**, **Lógica** e **Visual**, o que é essencial para a manutenção do código no futuro (Padrão MVC - Model, View, Controller). O que acha?

---
## 👤 Autor

**Wesley Henrique Ferreira de Oliveira**<br>
*Estudante de Engenharia de Software (Estácio) & Engenharia de dados*

Focado em transição de carreira para a área de Tecnologia, unindo minha experiência prática em resolução de problemas logísticos com o rigor técnico da Engenharia de Software e Dados.

**Áreas de Interesse:**
`Analista de Dados` `Engenharia de Dados` `Analista de Sistemas` `Engenharia de Software`

---
Conecte-se comigo ou entre em contato para dúvidas e sugestões:
<div align="center">
  <a href="https://www.linkedin.com/in/wesley-henrique22" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
  </a>
  <a href="mailto:wesleyhfo123@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>
  <a href="https://www.instagram.com/w25_oliveira/" target="_blank">
    <img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram">
  </a>
</div>

---

## 🚀 Como gerar o executável (.exe)

Para distribuir a aplicação, utilize o **PyInstaller**. Certifique-se de incluir as pastas de recursos corretamente para que o executável encontre as imagens e os módulos.

### Opção A: Pasta Única (Mais rápido para abrir)
```bash
pyinstaller --noconfirm --onedir --windowed --name "CALIBRADOR" --icon "assets/flesh_perfil.ico" --add-data "assets;assets" --add-data "base_dados;base_dados" --add-data "modulos;modulos" main.py
```

### Opção B: Arquivo Único (Recomendado para distribuição)
```bash
pyinstaller --noconfirm --onefile --windowed --name "CALIBRADOR" --icon "assets/flesh_perfil.ico" --add-data "assets;assets" --add-data "base_dados;base_dados" --add-data "modulos;modulos" main.py
```
---
