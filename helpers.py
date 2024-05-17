import platform
import customtkinter as ctk



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
        
        

# Slide panel az animalt notikhoz
class SlidePanel(ctk.CTkFrame):
    def __init__(self, parent, start_pos, end_pos, background_color):
        super().__init__(parent, fg_color=background_color)

        # General attributes
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = abs(start_pos - end_pos)

        # Animation logic
        self.pos = self.start_pos
        self.in_start_pos = True  # Indicates, if the panel is in the starting position

        # Layout
        self.place(relx=self.start_pos, rely=0.9, relwidth=self.width, relheight=0.1)
    
    def animate(self):
        if self.in_start_pos:
            self.animate_forward()
        else:
            self.animate_backwards()

    def animate_forward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.01  # Setting the animation speed
            self.place(relx=self.pos, rely=0.9, relwidth=self.width, relheight=0.1)
            self.after(10, self.animate_forward)  # Delay for the animation
        else:
            self.in_start_pos = False
            self.after(1000, self.animate_backwards)  # Waiting to start the backward animation

    def animate_backwards(self):
        if self.pos < self.start_pos:
            self.pos += 0.01  # Setting the animation speed
            self.place(relx=self.pos, rely=0.9, relwidth=self.width, relheight=0.1)
            self.after(10, self.animate_backwards)  # Delay for the animation
        else:
            self.in_start_pos = True