import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.title("Seasonal Trends")
        self.geometry(f"{1100}x{580}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.setup_sidebar()

    def setup_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky='nsew')
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.project_name_label = ctk.CTkLabel(self.sidebar_frame, text="Hello world",
                                               font=ctk.CTkFont(size=35, weight='bold'))
        self.project_name_label.grid(row=0, column=0, padx=20, pady=40)

        self.analyze_page_button = ctk.CTkButton(self.sidebar_frame, text='Analyze')
        self.analyze_page_button.grid(row=1, column=0, padx=20, pady=30)

        self.moreinfo_page_button = ctk.CTkButton(self.sidebar_frame)
        self.moreinfo_page_button.grid(row=2, column=0, padx=20, pady=5)

        self.exit_button = ctk.CTkButton(self.sidebar_frame, text='Exit', command=self.exit_button_event)
        self.exit_button.grid(row=5, column=0, padx=20, pady=35)

    def exit_button_event(self):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
