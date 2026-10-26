from controllers.main_controller import MainController


if __name__ == "__main__":
    try:
        MainController().ejecutar()
    except KeyboardInterrupt:
        print("\nPrograma finalizado.")
