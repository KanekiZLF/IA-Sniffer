#  Capturador de Links de Vídeo v5.3 ✨

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Ativo-brightgreen.svg))

Um aplicativo de desktop robusto e intuitivo desenvolvido para automatizar a captura de links de streaming de vídeo a partir de diversas páginas de animes, doramas e séries.

<br>

![Screenshot da Aplicação](https://img001.prntscr.com/file/img001/w_Zlw1itT3mWwZRNW4-CBQ.png)

---

## 🚀 Principais Funcionalidades

-   **Interface Gráfica Moderna:** Desenvolvido com CustomTkinter para uma aparência agradável e moderna.
-   **Compatibilidade Multi-Site:** Não se limita a um único site! Utiliza uma lógica de busca heurística para encontrar listas de episódios em diferentes layouts de HTML.
-   **Captura de Rede:** Utiliza `selenium-wire` para inspecionar o tráfego de rede e capturar os links de vídeo `.m3u8`, `.mp4`, etc., que são carregados pelos players.
-   **Interface Responsiva:** O processo de captura roda em uma thread separada, garantindo que a interface do usuário nunca congele.
-   **Persistência de Tema:** Lembra sua preferência de tema (Claro ou Escuro) entre as sessões, salvando a escolha em um arquivo `config.json`.
-   **Diálogo "Sobre" Personalizado:** Uma janela de informações customizada com um link clicável.

---

## 🔧 Como Funciona

O aplicativo opera em um fluxo de trabalho de três etapas para extrair os links desejados:

### **Etapa 1: Análise da Página Principal**
Quando você insere uma URL e clica em "Iniciar", uma primeira instância do Selenium (em modo `headless`, sem interface) é iniciada. Ela carrega a página e entrega o código-fonte HTML para o BeautifulSoup.

### **Etapa 2: Busca Inteligente de Episódios**
Com o HTML da página em mãos, a função `find_episode_links_heuristic` entra em ação. Ela não procura por um padrão fixo, mas sim:
1.  Tenta identificar "contêineres" comuns de episódios (ex: `<div class="lista-episodios">`).
2.  Dentro dessa área, ela usa expressões regulares flexíveis para encontrar links que se pareçam com episódios (ex: "Episódio 01", "Ep 2", "Capítulo 5", etc.).
3.  Todos os links de episódios encontrados são coletados e organizados.

### **Etapa 3: Captura do Link de Vídeo**
Uma segunda instância do Selenium, desta vez com o `selenium-wire` ativado, é iniciada. Ela navega para cada um dos links de episódio encontrados na etapa anterior. Para cada página, o `selenium-wire` monitora as requisições de rede e espera por uma que corresponda a um formato de vídeo conhecido (`.m3u8`, `.mp4`, `videoplayback`). O primeiro link correspondente é capturado, exibido na tela e salvo no arquivo `links.txt`.

---

## 📚 Como Usar

Siga os passos abaixo para configurar e rodar o projeto em sua máquina.

### **Pré-requisitos**
-   [Python 3.9](https://www.python.org/downloads/) ou superior
-   Google Chrome instalado

### **Instalação**

1.  **Clone o repositório (ou baixe os arquivos):**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # No Windows
    # source venv/bin/activate  # No Linux/Mac
    ```

3.  **Instale as dependências:**
    Crie um arquivo `requirements.txt` com o conteúdo abaixo e execute o comando `pip install -r requirements.txt`.

    **requirements.txt:**
    ```
    customtkinter
    selenium-wire
    beautifulsoup4
    Pillow
    ```
    **Comando:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Baixe o ChromeDriver:**
    -   Verifique a versão do seu Google Chrome (em `Ajuda > Sobre o Google Chrome`).
    -   Acesse o [Dashboard do ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/).
    -   Baixe o `chromedriver.exe` correspondente à sua versão do Chrome.
    -   Extraia e coloque o arquivo `chromedriver.exe` **na mesma pasta** do script principal.

### **Execução**
Com o ambiente configurado, basta executar o script:
```bash
python nome_do_seu_script.py
```

---

## 📂 Estrutura dos Arquivos

```
seu-projeto/
│
├── nome_do_seu_script.py   # O script principal
├── chromedriver.exe        # O driver do Selenium
├── requirements.txt        # Lista de dependências
│
├── config.json             # Criado automaticamente para salvar o tema
└── links.txt               # Criado automaticamente para salvar os links
```

---

<br>

Criado por Luiz F. R. Pimentel
