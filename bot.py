from publisher import MarketplacePublisher
from logger import logger


def main():

    print("Bot iniciado...")

    logger.info("================================")
    logger.info("Bot iniciado")
    logger.info("================================")

    publisher = MarketplacePublisher()

    try:
        print("Iniciando navegador...")

        publisher.iniciar()

        print("Abrindo Facebook...")

        login_ok = publisher.abrir_facebook()

        if not login_ok:
            print("Aguardando login...")

            input(
                "Faça o login no Facebook e pressione ENTER..."
            )

        print("Login concluído.")
        print("Automação pronta.")

    except Exception as e:
        print("\nERRO:")
        print(e)

        logger.exception("Erro durante execução.")

        input("\nPressione ENTER para fechar...")

    finally:
        publisher.fechar()


if __name__ == "__main__":
    main()