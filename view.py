import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from model import SeasonalTrendModel


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
        self.selected_graph = ctk.StringVar()
        self.selected_attribute = ctk.StringVar()
        self.create_layout()

    def create_layout(self):
        title = ctk.CTkLabel(self, text='Analyze Page', font=ctk.CTkFont(size=30, weight='bold'))
        title.grid(row=0, column=0, columnspan=3, padx=10, pady=15, stick='nw')

        self.grid_columnconfigure(2, weight=1)

        graph_type_label = ctk.CTkLabel(self, text='Graph Type', font=ctk.CTkFont(size=14, weight='bold'))
        graph_type_label.grid(row=1, column=0, padx=10, pady=2, sticky='w')

        self.graph_type = ctk.CTkComboBox(self, state='readonly',
                                          values=['Descriptive statistics', 'Correlation',
                                                  'Histogram', 'Bar graph', 'Pie graph'], variable=self.selected_graph)
        self.graph_type.grid(row=2, column=0, padx=10, pady=2, sticky='w')

        attribute_label = ctk.CTkLabel(self, text='Attribute', font=ctk.CTkFont(size=14, weight='bold'))
        attribute_label.grid(row=1, column=1, padx=5, pady=2, sticky='w')

        self.attribute = ctk.CTkComboBox(self, state='readonly', values=SeasonalTrendModel().get_columns(),
                                         variable=self.selected_attribute)
        self.attribute.grid(row=2, column=1, padx=5, pady=2)

        compute_button = ctk.CTkButton(self, text='Compute', font=ctk.CTkFont(size=14, weight='bold'),
                                       command=self.compute_graph_handler)
        compute_button.grid(row=2, column=2, padx=20, sticky='e')

        self.output_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.output_frame.grid(padx=15, pady=15, row=3, column=0, columnspan=3, sticky="nsew")
        self.grid_rowconfigure(3, weight=1)

    def create_histogram(self):
        selected_attribute = self.selected_attribute.get()
        for widget in self.output_frame.winfo_children():
            widget.destroy()
        data_model = SeasonalTrendModel()
        histogram_plot = data_model.create_story_histogram(selected_attribute)
        canvas = FigureCanvasTkAgg(histogram_plot, master=self.output_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)

    def compute_graph_handler(self):
        self.create_histogram()


class MoreinfoPage(BasePage):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        title = ctk.CTkLabel(self, text='Moreinfo Page', font=ctk.CTkFont(size=30, weight='bold'))
        title.grid(padx=10, pady=45)
        self.grid_columnconfigure(2, weight=1)


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
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0, fg_color="transparent")
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

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.mainloop()
