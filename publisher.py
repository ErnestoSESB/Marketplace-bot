from playwright.sync_api import sync_playwright

from config import NAVEGADOR_HEADLESS, TIMEOUT
from logger import logger


class MarketplacePublisher:

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    def iniciar(self):
        logger.info("Iniciando navegador...")

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=NAVEGADOR_HEADLESS,
            channel="chrome"
        )

        self.page = self.browser.new_page()

        self.page.set_default_timeout(TIMEOUT)

        logger.info("Navegador iniciado.")

    def abrir_facebook(self):
        logger.info("Abrindo Facebook...")

        self.page.goto(
            "https://www.facebook.com/",
            wait_until="domcontentloaded"
        )

    def fechar(self):
        logger.info("Fechando navegador...")

        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()