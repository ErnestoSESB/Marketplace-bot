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
            chromium_sandbox=True,
            viewport={"width": 1280, "height": 900},
        )

        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()

        self.page.set_default_timeout(TIMEOUT)

        logger.info("Navegador iniciado.")

    def abrir_facebook(self):
        logger.info("Abrindo Facebook...")

        self.page.goto(
            "https://www.facebook.com/",
            wait_until="domcontentloaded"
        )

        logger.info("Verificando login...")

        try:
            self.page.wait_for_url(
                lambda url: "login" not in url.lower(),
                timeout=120000
            )

            logger.info("Facebook carregado.")
            return True

        except Exception:
            logger.warning("Login ainda não foi detectado.")
            return False

    def fechar(self):
        logger.info("Fechando navegador...")

        if self.context:
            self.context.close()

        if self.playwright:
            self.playwright.stop()