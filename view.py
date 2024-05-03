import customtkinter as ctk


class BasePage(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def show(self):
        self.grid(row=0, column=1, rowspan=4, sticky="nsew")

    def hide(self):
        self.grid_forget()


class AnalyzePage(BasePage):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        label = ctk.CTkLabel(self, text="Analyze Page",font=ctk.CTkFont(size=20,weight='bold'))
        label.pack(pady=20,anchor='nw')


class MoreinfoPage(BasePage):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        label = ctk.CTkLabel(self, text="Moreinfo Page", font=ctk.CTkFont(size=20,weight='bold'))
        label.pack(pady=20,anchor='nw')


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Seasonal Trends")
        self.geometry(f"{1100}x{580}")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.setup_sidebar()

    def setup_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Seasonal Trends",
                                       font=ctk.CTkFont(size=35, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=40)

        self.pages = {}

        self.analyze_page_button = ctk.CTkButton(self.sidebar_frame, text="Analyze",
                                                 command=lambda p=AnalyzePage: self.show_page(p))
        self.analyze_page_button.grid(row=1, column=0, padx=20, pady=30)

        self.moreinfo_page_button = ctk.CTkButton(self.sidebar_frame, text="Moreinfo",
                                                  command=lambda p=MoreinfoPage: self.show_page(p))
        self.moreinfo_page_button.grid(row=2, column=0, padx=20, pady=5)

        self.exit_button = ctk.CTkButton(self.sidebar_frame, text='Exit', command=self.exit_button_event)
        self.exit_button.grid(row=5, column=0, padx=20, pady=35)

        self.current_page = None
        self.show_page(AnalyzePage)

    def exit_button_event(self):
        self.destroy()

    def show_page(self, page_class):
        if self.current_page:
            self.current_page.hide()
        self.current_page = page_class(self)
        self.current_page.show()


if __name__ == "__main__":
    app = App()
    app.mainloop()
