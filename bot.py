from publisher import MarketplacePublisher
from logger import logger


def main():

    logger.info("================================")
    logger.info("Bot iniciado")
    logger.info("================================")

    publisher = MarketplacePublisher()

    try:
        publisher.iniciar()
        publisher.abrir_facebook()

        input(
            "Facebook aberto. Pressione ENTER para fechar..."
        )

    except Exception:
        logger.exception("Erro durante execução.")

    finally:
        publisher.fechar()


if __name__ == "__main__":
    main()