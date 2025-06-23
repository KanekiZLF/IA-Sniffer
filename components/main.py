# =================================================================================
#  CAPTURA DE LINKS DE VÍDEO - v5.3 (Diálogo Clicável e Persistência de Tema)
#  Desenvolvido por Luiz. F. R. Pimentel e Gemini
# =================================================================================
import customtkinter as ctk
from customtkinter import CTkFont
import threading
import queue
import re
import os
import sys
import webbrowser
import time
import json
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
from urllib.parse import urljoin

# --- Configurações ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOME_ARQUIVO_SAIDA = os.path.join(BASE_DIR, "links.txt")
NOME_ARQUIVO_CONFIG = os.path.join(BASE_DIR, "config.json")
CHROME_DRIVER_PATH = os.path.join(BASE_DIR, "chromedriver.exe")
NOME_ARQUIVO_ICONE = os.path.join(BASE_DIR, "../assets/logo.jpg")


# =================================================================================
#  CLASSE DE DIÁLOGO PERSONALIZADO "SOBRE"
# =================================================================================
class AboutDialog(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Sobre")
        self.geometry("400x200")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        version = "5.3"
        github_url = "https://github.com/KanekiZLF"

        frame = ctk.CTkFrame(self)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        label_dev = ctk.CTkLabel(frame, text="Desenvolvido por Luiz. F. R. Pimentel e Gemini", wraplength=350)
        label_dev.pack(pady=(0, 10))

        label_version = ctk.CTkLabel(frame, text=f"Versão: {version}")
        label_version.pack(pady=5)
        
        link_frame = ctk.CTkFrame(frame, fg_color="transparent")
        link_frame.pack(pady=5)
        
        label_github_intro = ctk.CTkLabel(link_frame, text="GitHub: ")
        label_github_intro.pack(side="left")

        link_font = ctk.CTkFont(underline=True)
        label_link = ctk.CTkLabel(
            link_frame,
            text=github_url,
            font=link_font,
            text_color="#1E90FF"
        )
        label_link.pack(side="left")
        
        label_link.bind("<Button-1>", lambda e: self.open_link(github_url))
        label_link.bind("<Enter>", lambda e: label_link.configure(cursor="hand2"))
        label_link.bind("<Leave>", lambda e: label_link.configure(cursor=""))

        ok_button = ctk.CTkButton(frame, text="OK", command=self.destroy, width=100)
        ok_button.pack(pady=(20, 0))

    def open_link(self, url):
        try:
            webbrowser.open_new_tab(url)
        except Exception as e:
            print(f"Erro ao abrir link: {e}")


# =================================================================================
#  CLASSE PRINCIPAL DA APLICAÇÃO
# =================================================================================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.config = self.load_config()
        ctk.set_appearance_mode(self.config.get("theme", "Light"))

        self.title("Capturador de Links v5.3")
        self.geometry("500x600")
        self.resizable(False, False)
        
        ctk.set_default_color_theme("blue")

        try:
            if os.path.exists(NOME_ARQUIVO_ICONE):
                image = Image.open(NOME_ARQUIVO_ICONE)
                self.photo_image = ImageTk.PhotoImage(image)
                self.iconphoto(True, self.photo_image)
        except Exception as e:
            print(f"Aviso: Ícone não encontrado. Erro: {e}")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.update_queue = queue.Queue()
        self.cancel_event = threading.Event()
        self.create_widgets()
        self.process_queue()

    def load_config(self):
        if os.path.exists(NOME_ARQUIVO_CONFIG):
            try:
                with open(NOME_ARQUIVO_CONFIG, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {"theme": "Light"}
        return {"theme": "Light"}

    def save_config(self):
        try:
            with open(NOME_ARQUIVO_CONFIG, 'w') as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            print(f"Erro ao salvar configuração: {e}")

    def create_widgets(self):
        top_frame = ctk.CTkFrame(self)
        top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        top_frame.grid_columnconfigure(0, weight=1)

        self.url_label = ctk.CTkLabel(top_frame, text="URL da Página do Anime/Série:")
        self.url_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 0), sticky="w")
        self.url_entry = ctk.CTkEntry(top_frame, placeholder_text="Cole a URL da página principal aqui")
        self.url_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.start_button = ctk.CTkButton(top_frame, text="Iniciar", command=self.start_scraping_thread, width=80)
        self.start_button.grid(row=1, column=1, padx=(0, 5), pady=5)
        self.cancel_button = ctk.CTkButton(top_frame, text="Cancelar", command=self.cancel_scraping, state="disabled", fg_color="#D32F2F", hover_color="#B71C1C", width=80)
        self.cancel_button.grid(row=1, column=2, padx=(0, 10), pady=5)

        status_frame = ctk.CTkFrame(self)
        status_frame.grid(row=1, column=0, padx=10, pady=0, sticky="ew")
        status_frame.grid_columnconfigure(0, weight=1)
        self.status_label = ctk.CTkLabel(status_frame, text="Aguardando início...")
        self.status_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.progress_bar = ctk.CTkProgressBar(status_frame, orientation="horizontal")
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.links_textbox = ctk.CTkTextbox(self, state="disabled", wrap="none")
        self.links_textbox.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        bottom_frame.grid_columnconfigure(0, weight=1)

        self.theme_switch = ctk.CTkSwitch(bottom_frame, text="Tema Escuro", command=self.toggle_theme)
        self.theme_switch.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        if self.config.get("theme", "Light") == "Dark":
            self.theme_switch.select()
            self.theme_switch.configure(text="Tema Claro")

        self.open_file_button = ctk.CTkButton(bottom_frame, text="Abrir Arquivo (.txt)", command=self.open_output_file)
        self.open_file_button.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        
        self.about_button = ctk.CTkButton(bottom_frame, text="?", command=self.show_about_dialog, width=40)
        self.about_button.grid(row=0, column=2, padx=10, pady=5, sticky="e")

    def toggle_theme(self):
        is_dark = self.theme_switch.get() == 1
        new_theme = "Dark" if is_dark else "Light"
        ctk.set_appearance_mode(new_theme)
        self.theme_switch.configure(text="Tema Claro" if is_dark else "Tema Escuro")
        
        self.config["theme"] = new_theme
        self.save_config()
    
    def show_about_dialog(self):
        """Abre a janela de diálogo 'Sobre' personalizada."""
        about_dialog = AboutDialog(self)

    def start_scraping_thread(self):
        url = self.url_entry.get()
        if not url:
            self.status_label.configure(text="Erro: Por favor, insira uma URL.", text_color="orange")
            return

        self.cancel_event.clear()
        self.start_button.configure(state="disabled", text="Buscando...")
        self.cancel_button.configure(state="normal")
        self.status_label.configure(text="Iniciando processo...", text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        self.progress_bar.set(0)
        
        self.links_textbox.configure(state="normal")
        self.links_textbox.delete("1.0", "end")
        self.links_textbox.configure(state="disabled")
        
        thread = threading.Thread(target=self.scraping_worker, args=(url,), daemon=True)
        thread.start()

    def cancel_scraping(self):
        self.status_label.configure(text="Cancelando processo... Aguarde.", text_color="orange")
        self.cancel_event.set()
        self.cancel_button.configure(state="disabled")

    def process_queue(self):
        try:
            message_type, data = self.update_queue.get_nowait()
            
            if message_type == "status":
                self.status_label.configure(text=data, text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"])
            elif message_type == "link":
                self.links_textbox.configure(state="normal")
                self.links_textbox.insert("end", data + "\n")
                self.links_textbox.see("end")
                self.links_textbox.configure(state="disabled")
            elif message_type == "progress":
                current, total = data
                self.progress_bar.set(current / total)
            elif message_type == "finished":
                self.start_button.configure(state="normal", text="Iniciar")
                self.cancel_button.configure(state="disabled")
                self.status_label.configure(text=data, text_color="green" if "Concluído" in data else "orange")
                if "Concluído" in data: self.progress_bar.set(1)
        except queue.Empty:
            pass
        self.after(100, self.process_queue)

    def find_episode_links_heuristic(self, soup, base_url):
        links_encontrados = set()
        padrao_texto_ep = re.compile(
            r'(ep(is[oó]dio)?|cap(ítulo)?|parte|part|ova|ona|filme|movie|especial|special)\s*[\d.\-]+', 
            re.IGNORECASE
        )
        seletores_container = [
            '.episodes-list', '.lista-de-episodios', '.episode_list', '.episodios', 
            '#episode-list', '.video-list', 'ul[class*="episode"]', 'div[class*="episode"]'
        ]
        
        search_area = soup
        for seletor in seletores_container:
            container = soup.select_one(seletor)
            if container:
                search_area = container
                break
        
        todos_os_links = search_area.find_all('a', href=True)

        for link in todos_os_links:
            href = link['href']
            texto_link = link.get_text(strip=True)
            titulo_link = link.get('title', '')

            if padrao_texto_ep.search(texto_link) or padrao_texto_ep.search(titulo_link) or padrao_texto_ep.search(href):
                url_completo = urljoin(base_url, href)
                links_encontrados.add(url_completo)
        
        return sorted(list(links_encontrados))

    def scraping_worker(self, url):
        service = None
        driver = None
        serie_title = "Série"
        try:
            service = Service(executable_path=CHROME_DRIVER_PATH)
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--log-level=3")
            options.add_argument("--disable-gpu")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])

            self.update_queue.put(("status", "Parte 1: Analisando HTML da página principal..."))
            
            driver = webdriver.Chrome(service=service, options=options)
            driver.get(url)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            try:
                title_tag = soup.find(['h1', 'h2'], class_=['entry-title', 'post-title', 'title'])
                if not title_tag:
                    title_tag = soup.find('h1') # Fallback para qualquer h1
                
                if title_tag:
                    serie_title = title_tag.get_text(strip=True)
                elif soup.title:
                    serie_title = soup.title.string.strip()
            except AttributeError:
                print("Aviso: Título não encontrado, usando valor padrão.")

            display_title = serie_title[:35] + "..." if len(serie_title) > 35 else serie_title
            
            driver.quit()

            self.update_queue.put(("status", f"Procurando episódios para '{display_title}'..."))
            links_dos_episodios = self.find_episode_links_heuristic(soup, url)
            
            if not links_dos_episodios:
                self.update_queue.put(("finished", f"Erro: Nenhum episódio encontrado para '{display_title}'."))
                return

            self.update_queue.put(("status", f"Sucesso! {len(links_dos_episodios)} episódios encontrados."))
            
            header = f"\n\n------ Links de '{serie_title}' ({time.strftime('%Y-%m-%d %H:%M:%S')}) ------\nURL: {url}\n"
            with open(NOME_ARQUIVO_SAIDA, 'a', encoding='utf-8') as f:
                f.write(header)

            self.update_queue.put(("status", f"Parte 2: Inspecionando rede para '{display_title}'..."))
            
            wire_options = {'disable_capture': True}
            driver = webdriver.Chrome(service=service, seleniumwire_options=wire_options, options=options)
            
            for i, link_ep in enumerate(links_dos_episodios):
                if self.cancel_event.is_set():
                    self.update_queue.put(("finished", f"Cancelado: Processamento interrompido."))
                    break
                
                self.update_queue.put(("status", f"'{display_title}' - Processando Ep. {i+1}/{len(links_dos_episodios)}..."))
                self.update_queue.put(("progress", (i, len(links_dos_episodios))))
                
                driver.scopes = ['.*']
                driver.get(link_ep)
                
                try:
                    req = driver.wait_for_request(r'(\.m3u8|\.mp4|\.mkv|videoplayback)', timeout=25)
                    video_url = req.url
                    self.update_queue.put(("link", video_url))
                    with open(NOME_ARQUIVO_SAIDA, 'a', encoding='utf-8') as f: f.write(video_url + '\n')
                except Exception:
                    self.update_queue.put(("link", f"[AVISO] Link de vídeo não encontrado para o episódio {i+1}."))
                
                del driver.requests
            else:
                self.update_queue.put(("finished", f"Concluído: '{display_title}' - {len(links_dos_episodios)} links processados."))
        
        except Exception as e:
            self.update_queue.put(("finished", f"Ocorreu um erro crítico: {e}"))
        finally:
            if driver:
                driver.quit()

    def open_output_file(self):
        try:
            if not os.path.exists(NOME_ARQUIVO_SAIDA):
                with open(NOME_ARQUIVO_SAIDA, 'w', encoding='utf-8') as f:
                    f.write("# Nenhum link capturado ainda.")
            webbrowser.open(os.path.realpath(NOME_ARQUIVO_SAIDA))
        except Exception as e:
            self.status_label.configure(text=f"Erro ao abrir arquivo: {e}")


if __name__ == "__main__":
    if sys.platform == "win32":
        from multiprocessing import freeze_support
        freeze_support()
        
    app = App()
    app.mainloop()