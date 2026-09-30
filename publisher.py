import time
from playwright.sync_api import sync_playwright
from config import NAVEGADOR_HEADLESS, TIMEOUT
from logger import logger

class MarketplacePublisher:
    def __init__(self):
        self.playwright = None
        self.context = None
        self.page = None

    def iniciar(self):
        logger.info("Iniciando navegador...")
        self.playwright = sync_playwright().start()
        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir="perfil_facebook",
            headless=NAVEGADOR_HEADLESS,
            channel="chrome",
            viewport={"width": 1280, "height": 900},
        )
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        self.page.set_default_timeout(TIMEOUT)
        logger.info("Navegador iniciado.")

    def esta_logado(self):
        url_atual = self.page.url.lower()
        if any(p in url_atual for p in ["login", "two_step_verification", "checkpoint"]):
            return False
        try:
            perfil = self.page.locator('[aria-label*="Perfil"], [aria-label*="profile"], a[href*="/me/"], [aria-label*="Marketplace"]')
            return perfil.count() > 0
        except Exception:
            return False

    def abrir_facebook(self):
        logger.info("Abrindo Facebook...")
        self.page.goto("https://www.facebook.com/", wait_until="domcontentloaded")
        time.sleep(2)
        return self.esta_logado()

    def abrir_criacao_anuncio(self):
        logger.info("Acessando tela de criação de anúncio no Marketplace...")
        self.page.goto("https://www.facebook.com/marketplace/create/item", wait_until="domcontentloaded")
        logger.info("Aguardando formulário do Marketplace carregar...")
        time.sleep(4)

    def _preencher_texto(self, rotulos, valor, nome_campo, e_textarea=False):

        tag = "textarea" if e_textarea else "input"

        for rotulo in rotulos:
            try:
                campo = self.page.get_by_label(rotulo, exact=False)
                if campo.is_visible(timeout=1500):
                    campo.click()
                    time.sleep(0.2)
                    campo.fill(str(valor))
                    print(f"  [OK] {nome_campo} preenchido!")
                    return True
            except Exception:
                pass

            try:
                campo = self.page.locator("label").filter(has_text=rotulo).locator(tag).first
                if campo.is_visible(timeout=1500):
                    campo.click()
                    time.sleep(0.2)
                    campo.fill(str(valor))
                    print(f"  [OK] {nome_campo} preenchido!")
                    return True
            except Exception:
                pass

            try:
                campo = self.page.locator(f'{tag}[aria-label*="{rotulo}"]').first
                if campo.is_visible(timeout=1500):
                    campo.click()
                    time.sleep(0.2)
                    campo.fill(str(valor))
                    print(f"  [OK] {nome_campo} preenchido!")
                    return True
            except Exception:
                pass

        if e_textarea:
            try:
                campo = self.page.locator("textarea").first
                if campo.is_visible(timeout=1500):
                    campo.click()
                    time.sleep(0.2)
                    campo.fill(str(valor))
                    print(f"  [OK] {nome_campo} preenchido!")
                    return True
            except Exception:
                pass

        print(f"  [X] Falha ao preencher {nome_campo}")
        return False

    def _selecionar_categoria(self, categoria_nome):

        try:
            print(f"Selecionando Categoria: {categoria_nome}...")

            clicou = False
            for rotulo in ["Categoria", "Category"]:
                try:
                    el = self.page.get_by_label(rotulo, exact=False).first
                    if el.is_visible(timeout=1500):
                        el.click()
                        clicou = True
                        break
                except Exception:
                    pass

                if not clicou:
                    try:
                        el = self.page.locator("label").filter(has_text=rotulo).first
                        if el.is_visible(timeout=1500):
                            el.click()
                            clicou = True
                            break
                    except Exception:
                        pass

            if not clicou:
                print("  [X] Não foi possível abrir o menu de Categoria")
                return False

            time.sleep(1.5)

            try:
                input_busca = self.page.locator('div[role="dialog"] input, div[role="listbox"] input, input[placeholder*="Pesquisar"]').first
                if input_busca.is_visible(timeout=1000):
                    input_busca.fill(categoria_nome)
                    time.sleep(1)
            except Exception:
                pass

            containers_menu = [
                'div[role="dialog"]',
                'div[role="listbox"]',
                'div[role="menu"]',
                'div[tabindex="-1"]'
            ]

            for container_sel in containers_menu:
                try:
                    container = self.page.locator(container_sel).first
                    if container.is_visible(timeout=1000):
                        opcao = container.locator(f':not(a):has-text("{categoria_nome}")').first
                        if opcao.is_visible(timeout=1000):
                            opcao.click()
                            print(f"  [OK] Categoria '{categoria_nome}' selecionada!")
                            return True
                except Exception:
                    continue
            for role_opcao in ["option", "button"]:
                try:
                    opcao = self.page.get_by_role(role_opcao, name=categoria_nome, exact=False).first
                    if opcao.is_visible(timeout=1500):
                        opcao.click()
                        print(f"  [OK] Categoria '{categoria_nome}' selecionada!")
                        return True
                except Exception:
                    continue

        except Exception as e:
            print(f"  [X] Erro ao selecionar Categoria: {e}")

        print(f"  [X] Falha ao selecionar Categoria '{categoria_nome}'")
        return False

    def _selecionar_dropdown(self, rotulos, valor_opcao, nome_campo):
        for rotulo in rotulos:
            try:
                clicou = False
                try:
                    el = self.page.get_by_label(rotulo, exact=False)
                    if el.is_visible(timeout=1500):
                        el.click()
                        clicou = True
                except Exception:
                    pass

                if not clicou:
                    try:
                        el = self.page.locator("label").filter(has_text=rotulo).first
                        if el.is_visible(timeout=1500):
                            el.click()
                            clicou = True
                    except Exception:
                        pass

                if clicou:
                    time.sleep(1.5)

                    opcao = self.page.get_by_role("option", name=valor_opcao, exact=False).first
                    if opcao.is_visible(timeout=2000):
                        opcao.click()
                        print(f"  [OK] {nome_campo}: '{valor_opcao}' selecionado!")
                        return True

                    opcao_txt = self.page.get_by_text(valor_opcao, exact=False).first
                    if opcao_txt.is_visible(timeout=2000):
                        opcao_txt.click()
                        print(f"  [OK] {nome_campo}: '{valor_opcao}' selecionado!")
                        return True
            except Exception:
                continue

        print(f"  [X] Falha ao selecionar {nome_campo}")
        return False

    def _abrir_mais_detalhes(self):
        print("Buscando botão 'Mais detalhes'...")
        seletores = [
            'div[role="button"]:has-text("Mais detalhes")',
            'button:has-text("Mais detalhes")',
            '[aria-label*="Mais detalhes"]',
            'span:has-text("Mais detalhes")',
        ]
        for seletor in seletores:
            try:
                botao = self.page.locator(seletor).first
                if botao.is_visible(timeout=2000):
                    botao.click()
                    time.sleep(1.5)
                    print("  [OK] Botão 'Mais detalhes' clicado!")
                    return True
            except Exception:
                continue

        print("  [i] 'Mais detalhes' não foi necessário ou já está aberto.")
        return False

    def _preencher_localizacao(self, localizacao):
        try:
            campo_loc = self.page.get_by_label("Localização", exact=False)
            if not campo_loc.is_visible(timeout=1500):
                campo_loc = self.page.locator('label').filter(has_text="Localização").locator('input').first

            if campo_loc.is_visible(timeout=2000):
                campo_loc.click()
                self.page.keyboard.press("Control+A")
                self.page.keyboard.press("Backspace")
                time.sleep(0.3)
                campo_loc.fill(localizacao)
                time.sleep(2)

                self.page.keyboard.press("ArrowDown")
                time.sleep(0.5)
                self.page.keyboard.press("Enter")
                print(f"  [OK] Localização '{localizacao}' selecionada!")
                return True
        except Exception as e:
            print(f"  [X] Falha na Localização: {e}")
        return False

    def _preencher_etiquetas(self, etiquetas):
        if isinstance(etiquetas, str):
            etiquetas = [e.strip() for e in etiquetas.split(",") if e.strip()]

        try:
            campo_tags = self.page.get_by_label("Etiquetas", exact=False)
            if not campo_tags.is_visible(timeout=1500):
                campo_tags = self.page.locator('label').filter(has_text="Etiquetas").locator('textarea, input').first

            if campo_tags.is_visible(timeout=2000):
                campo_tags.click()
                for tag in etiquetas:
                    campo_tags.fill(tag)
                    self.page.keyboard.press("Enter")
                    time.sleep(0.3)
                print(f"  [OK] {len(etiquetas)} Etiqueta(s) adicionada(s)!")
                return True
        except Exception as e:
            print(f"  [X] Falha nas Etiquetas: {e}")
        return False

    def preencher_anuncio(self, dados_anuncio):
        logger.info("Iniciando preenchimento do formulário...")

        # 1. Anexar Fotos
        fotos = dados_anuncio.get("fotos", [])
        if fotos:
            print("Anexando fotos...")
            try:
                input_foto = self.page.locator('input[type="file"][accept*="image"]').first
                input_foto.set_input_files(fotos)
                print("  [OK] Fotos anexadas!")
                time.sleep(3)
            except Exception as e:
                print(f"  [X] Erro ao anexar fotos: {e}")

        # 2. Título
        if dados_anuncio.get("titulo"):
            print("Preenchendo Título...")
            self._preencher_texto(["Título", "Title"], dados_anuncio["titulo"], "Título")

        # 3. Preço
        if dados_anuncio.get("preco") is not None:
            print("Preenchendo Preço...")
            self._preencher_texto(["Preço", "Price"], dados_anuncio["preco"], "Preço")

        # 4. Categoria
        if dados_anuncio.get("categoria"):
            print("Selecionando Categoria...")
            self._selecionar_categoria(dados_anuncio["categoria"])

        # 5. Condição (Padrão: "Novo")
        condicao = dados_anuncio.get("condicao", "Novo")
        print("Selecionando Condição...")
        self._selecionar_dropdown(["Condição", "Condition"], condicao, "Condição")

        # 6. EXPANDIR SEÇÃO "MAIS DETALHES"
        self._abrir_mais_detalhes()

        # Rola a página para baixo
        self.page.mouse.wheel(0, 600)
        time.sleep(1.5)

        # 7. Descrição
        if dados_anuncio.get("descricao"):
            print("Preenchendo Descrição...")
            self._preencher_texto(["Descrição", "Description"], dados_anuncio["descricao"], "Descrição", e_textarea=True)

        # 8. Etiquetas / Tags
        etiquetas = dados_anuncio.get("etiquetas", dados_anuncio.get("tags", []))
        if etiquetas:
            print("Preenchendo Etiquetas...")
            self._preencher_etiquetas(etiquetas)

        # 9. Localização
        if dados_anuncio.get("localizacao"):
            print("Preenchendo Localização...")
            self._preencher_localizacao(dados_anuncio["localizacao"])

    def fechar(self):
        logger.info("Fechando navegador...")
        if self.context:
            self.context.close()
        if self.playwright:
            self.playwright.stop()