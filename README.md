# Capturador de Links de Vídeo v5.3 ✨

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Ativo-brightgreen.svg)

Um aplicativo de desktop robusto e intuitivo desenvolvido para automatizar a captura de links de streaming de vídeo a partir de diversas páginas de animes, doramas e séries.

<br>

![Screenshot da Aplicação](https://img001.prntscr.com/file/img001/w_Zlw1itT3mWwZRNW4-CBQ.png)

---

## 💻 Download (Versão Executável .exe)

Para usuários que não desejam instalar Python e as dependências, uma versão executável (`.exe`) para Windows está disponível. Basta baixar o arquivo `.zip`, descompactar e rodar o programa.

⚠️ **Aviso:** Devido à natureza complexa dos sites de streaming (com CAPTCHAs e anúncios), o programa pode não funcionar perfeitamente em 100% dos sites ou pode exigir interação manual para fechar pop-ups ou resolver verificações de segurança.

<div align="center">

[**➡️ Baixar Capturador de Links v5.3 (Google Drive)**](https://drive.google.com/file/d/1jTbAuktbS4imdiKXJtWvNXy1Zh0ikWax/view?usp=sharing)

</div>

---

## 🚀 Principais Funcionalidades

- **Interface Gráfica Moderna:** Desenvolvido com CustomTkinter para uma aparência agradável e moderna.
- **Compatibilidade Multi-Site:** Não se limita a um único site! Utiliza uma lógica de busca heurística para encontrar listas de episódios em diferentes layouts de HTML.
- **Gerenciamento Automático de Driver:** Utiliza o Selenium Manager para baixar e gerenciar automaticamente o `chromedriver` necessário, garantindo compatibilidade com a versão do Chrome do usuário.
- **Captura de Rede:** Usa `selenium-wire` para inspecionar o tráfego de rede e capturar os links de vídeo `.m3u8`, `.mp4`, etc.
- **Interface Responsiva:** O processo de captura roda em uma thread separada, garantindo que a interface do usuário nunca congele.
- **Persistência de Tema:** Lembra sua preferência de tema (Claro ou Escuro) entre as sessões.
- **Diálogo "Sobre" Personalizado:** Uma janela de informações customizada com um link clicável.

---

## 🔧 Como Funciona

O aplicativo opera em um fluxo de trabalho de três etapas para extrair os links desejados:

### **Etapa 1: Análise da Página Principal**

Quando você insere uma URL e clica em "Iniciar", uma instância do Selenium (em modo `headless`) é iniciada para carregar a página e entregar o código-fonte HTML para o BeautifulSoup.

### **Etapa 2: Busca Inteligente de Episódios**

A função `find_episode_links_heuristic` analisa o HTML e, usando padrões flexíveis, identifica e coleta os links de todos os episódios listados na página.

### **Etapa 3: Captura do Link de Vídeo**

Uma segunda instância do `selenium-wire` navega para cada página de episódio. Ele monitora as requisições de rede, esperando por uma que corresponda a um formato de vídeo conhecido. O primeiro link correspondente é capturado, exibido na tela e salvo no arquivo `links.txt`.

---

## 📚 Para Desenvolvedores: Rodando a Partir do Código-Fonte

Siga os passos abaixo para configurar e rodar o projeto em sua máquina.

### **Pré-requisitos**

- [Python 3.9](https://www.python.org/downloads/) ou superior
- Google Chrome instalado

### **Instalação**

1.  **Clone o repositório:**

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

### **Execução**

Com o ambiente configurado, basta executar o script. O `chromedriver` será gerenciado automaticamente.

```bash
python nome_do_seu_script.py
```

---

## 📂 Estrutura dos Arquivos

```
seu-projeto/
│
├── nome_do_seu_script.py   # O script principal
├── requirements.txt        # Lista de dependências
│
├── config.json             # Criado automaticamente para salvar o tema
└── links.txt               # Criado automaticamente para salvar os links
```

---

<br>

Criado por Luiz F. R. Pimentel
