import platform



# Operacios rendszer megvizsgalasa, hogy eldontsuk melyik icon file nevet fogjuk hasznalni
def decide_logo_by_system():
    # operacios rendszer lekerdezese
    platform_system = platform.system()

    match platform_system:

        # Windows
        case  'Windows':
            return 'assets/beerpong.ico'
        
        # MacOS
        case 'Darwin':
            return 'assets/beer-pong.icns'