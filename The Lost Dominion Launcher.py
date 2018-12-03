import tkinter
import os
import subprocess

class GUI:
    def __init__(self):
        self.main_window = tkinter.Tk()
        self.main_window.title ("The Lost Dominion Launcher")
        self.main_window.resizable(width = False, height = False)

        self.a_frame = tkinter.Frame(self.main_window)
        self.launch = "Launch The Lost Dominion"
        self.install = "Install Necessary Libraries"

        self.game_folder = os.path.dirname(__file__)
        self.img_folder = os.path.join(self.game_folder, 'img')
        self.img_file = os.path.join(self.img_folder, 'logo.png')

        self.logo = tkinter.PhotoImage(file = self.img_file)

        self.label = tkinter.Label(self.a_frame, image = self.logo, height = 150, width = 500)
        self.label.pack(side="left")

        self.b_frame = tkinter.Frame(self.main_window)
        self.launch_button = tkinter.Button(self.b_frame, text = self.launch, command = self.launch_game)

        self.c_frame = tkinter.Frame(self.main_window)
        self.install_button = tkinter.Button(self.c_frame, text = self.install, command = self.install_game)

        self.d_frame = tkinter.Frame(self.main_window)
        self.quit_button = tkinter.Button(self.d_frame, text = "Quit", command = self.quit_game)

        self.e_frame = tkinter.Frame(self.main_window)
        self.label = tkinter.Label(self.e_frame, text = " ", height = 5)
        self.label.pack(side="left")

        self.a_frame.pack()
        self.b_frame.pack()
        self.c_frame.pack()
        self.d_frame.pack()
        self.e_frame.pack()
        self.launch_button.pack(side="right")
        self.install_button.pack(side="right")
        self.quit_button.pack(side="right")

        tkinter.mainloop()

    def launch_game(self):
        subprocess.call("python3 main.py", shell = True)
        tkinter.mainloop()
        quit()

    def install_game(self):
        subprocess.call("pip install pygame", shell = True)
        subprocess.call("pip install pytmx", shell = True)

        tkinter.mainloop()

    def quit_game(self):
        quit()

        tkinter.mainloop()


def main():
    GUI()

main()
