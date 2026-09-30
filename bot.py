import os
from publisher import MarketplacePublisher
from logger import logger
import anuncio

def main():
    print("Bot iniciado...")
    publisher = MarketplacePublisher()

    try:
        publisher.iniciar()
        login_ok = publisher.abrir_facebook()

        if not login_ok:
            print("\nVocê não está totalmente logado!")
            input("Conclua o login/2FA e pressione ENTER...")

        print("\nAcessando Marketplace...")
        publisher.abrir_criacao_anuncio()

        dados_raw = getattr(anuncio, "ANUNCIO", {})

        imagens_brutas = dados_raw.get("imagens", dados_raw.get("fotos", []))
        fotos_absolutas = [os.path.abspath(img) for img in imagens_brutas]

        dados = {
            "titulo": dados_raw.get("titulo", ""),
            "preco": dados_raw.get("preco", "0"),
            "categoria": dados_raw.get("categoria", "Serviços"),
            "condicao": dados_raw.get("condicao", "Novo"),
            "descricao": dados_raw.get("descricao", ""),
            "localizacao": dados_raw.get("localizacao", ""),
            "etiquetas": dados_raw.get("etiquetas", dados_raw.get("tags", [])),
            "fotos": fotos_absolutas
        }

        print("\nPreenchendo o anúncio completo...")
        publisher.preencher_anuncio(dados)

        print("\nPreenchimento de todos os campos concluído!")
        input("Verifique o formulário no navegador e pressione ENTER para encerrar...")

    except Exception as e:
        print("\nERRO DURANTE A EXECUÇÃO:")
        print(e)
        logger.exception("Erro na execução.")
        input("\nPressione ENTER para sair...")

    finally:
        publisher.fechar()

if __name__ == "__main__":
    main()