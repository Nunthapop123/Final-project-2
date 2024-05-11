import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from model import SeasonalTrendModel
import matplotlib.pyplot as plt


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
        self.selected_season = ctk.StringVar()
        self.selected_graph = ctk.StringVar()
        self.selected_attribute = ctk.StringVar()
        self.selected_category = ctk.StringVar()
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.create_layout()
        self.season_combobox = None
        self.category_combobox = None

    def create_layout(self):
        title = ctk.CTkLabel(self, text='Analyze Page', font=ctk.CTkFont(size=30, weight='bold'))
        title.grid(row=0, column=0, columnspan=3, padx=10, pady=(42, 0), stick='nw')

        graph_type_label = ctk.CTkLabel(self, text='Graph Type', font=ctk.CTkFont(size=14, weight='bold'))
        graph_type_label.grid(row=1, column=0, padx=10, pady=2, sticky='w')

        self.graph_type = ctk.CTkComboBox(self, state='readonly',
                                          values=['Descriptive statistics', 'Correlation',
                                                  'Histogram', 'Bar graph', 'Pie graph'],
                                          variable=self.selected_graph,
                                          command=self.update_attribute)
        self.graph_type.grid(row=2, column=0, padx=10, pady=2, sticky='w')

        attribute_label = ctk.CTkLabel(self, text='Attribute', font=ctk.CTkFont(size=14, weight='bold'))
        attribute_label.grid(row=1, column=1, padx=5, pady=2, sticky='w')

        self.attribute = ctk.CTkComboBox(self, state='readonly', values=SeasonalTrendModel().get_columns(),
                                         variable=self.selected_attribute)
        self.attribute.grid(row=2, column=1, padx=5, pady=2)

        self.compute_button = ctk.CTkButton(self, text='Compute', font=ctk.CTkFont(size=14, weight='bold'))
        self.compute_button.grid(row=2, column=3, padx=20, sticky='e')

        self.output_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.output_frame.grid(padx=15, pady=15, row=3, column=0, columnspan=4, sticky="nsew")

    def season_combobox_layout(self):
        if self.selected_graph.get() in ['Descriptive statistics', 'Correlation', 'Pie graph']:
            if self.season_combobox is None:
                self.season_label = ctk.CTkLabel(self, text='Season',
                                                 font=ctk.CTkFont(size=14, weight='bold'))
                self.season_label.grid(row=1, column=3, padx=10, pady=2, sticky='w')
                self.season_combobox = ctk.CTkComboBox(self, state='readonly',
                                                       values=['Spring', 'Summer', 'Fall', 'Winter'],
                                                       variable=self.selected_season)
                self.season_combobox.grid(row=2, column=3, padx=10, pady=2, sticky='w')
        elif self.selected_graph.get() in ['Bar graph']:
            if self.season_combobox is None and self.category_combobox is None:
                self.season_label = ctk.CTkLabel(self, text='Season',
                                                 font=ctk.CTkFont(size=14, weight='bold'))
                self.season_label.grid(row=1, column=3, padx=10, pady=2, sticky='w')
                self.season_combobox = ctk.CTkComboBox(self, state='readonly',
                                                       values=['Spring', 'Summer', 'Fall', 'Winter'],
                                                       variable=self.selected_season)
                self.season_combobox.grid(row=2, column=3, padx=10, pady=2, sticky='w')

                self.category_label = ctk.CTkLabel(self, text='Category',
                                                   font=ctk.CTkFont(size=14, weight='bold'))
                self.category_label.grid(row=1, column=3, padx=165, pady=2, sticky='w')
                self.category_combobox = ctk.CTkComboBox(self, state='readonly',
                                                         values=['Outerwear', 'Footwear', 'Clothing', 'Accessories'],
                                                         variable=self.selected_category)
                self.category_combobox.grid(row=2, column=3, padx=165, pady=2, sticky='w')
        else:
            self.clear_combo()

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
        plt.close(histogram_plot)

    def create_pie(self):
        selected_season = self.selected_season.get()
        for widget in self.output_frame.winfo_children():
            widget.destroy()
        data_model = SeasonalTrendModel()
        pie_plot = data_model.create_story_pie(selected_season)
        canvas = FigureCanvasTkAgg(pie_plot, master=self.output_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
        plt.close(pie_plot)

    def create_descriptive(self):
        selected_season = self.selected_season.get()
        for widget in self.output_frame.winfo_children():
            widget.destroy()
        data_model = SeasonalTrendModel()
        descriptive = data_model.create_descriptive(selected_season)
        label1 = ctk.CTkLabel(self.output_frame, text=descriptive, font=ctk.CTkFont(size=15, weight='bold'))
        label1.grid(row=0, column=1)

    def create_bar(self):
        selected_season = self.selected_season.get()
        selected_category = self.selected_category.get()
        for widget in self.output_frame.winfo_children():
            widget.destroy()
        data_model = SeasonalTrendModel()
        bar_plot = data_model.create_story_bar(selected_season, selected_category)
        canvas = FigureCanvasTkAgg(bar_plot, master=self.output_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
        plt.close(bar_plot)

    def compute_graph_handler(self):
        self.create_descriptive()

    def update_attribute(self, choice):
        graph = self.selected_graph.get()
        if graph == 'Descriptive statistics':
            self.clear_combo()
            self.season_combobox_layout()
            self.attribute.configure(values=['Purchase Amount (USD)'])
            self.compute_button.configure(command=self.create_descriptive)
        elif graph == 'Correlation':
            self.clear_combo()
            self.season_combobox_layout()
            self.attribute.configure(values=['Purchase Amount (USD)', 'Review Rating'])
        elif graph == 'Histogram':
            self.clear_combo()
            self.attribute.configure(values=['Purchase Amount (USD)'])
            self.compute_button.configure(command=self.create_histogram)
        elif graph == 'Bar graph':
            self.clear_combo()
            self.season_combobox_layout()
            self.attribute.configure(values=['Category'])
            self.compute_button.configure(command=self.create_bar)
        elif graph == 'Pie graph':
            self.clear_combo()
            self.season_combobox_layout()
            self.attribute.configure(values=['Category'])
            self.compute_button.configure(command=self.create_pie)

    def clear_combo(self):
        self.attribute.set('')
        if self.season_combobox is not None:
            self.selected_season.set('')
            self.season_label.grid_forget()
            self.season_combobox.grid_forget()
            self.season_label = None
            self.season_combobox = None

        if self.category_combobox is not None:
            self.selected_category.set('')
            self.category_label.grid_forget()
            self.category_combobox.grid_forget()
            self.category_label = None
            self.category_combobox = None


class MoreinfoPage(BasePage):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.textfile = 'description.txt'
        self.selected_item = ctk.StringVar()
        self.toplevel_window = None
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=3)
        self.page_layout()

    def page_layout(self):
        title = ctk.CTkLabel(self, text='Moreinfo Page', font=ctk.CTkFont(size=30, weight='bold'))
        title.grid(row=0, column=0, padx=10, pady=45, sticky='nw')
        about = ctk.CTkLabel(self, text='About Project', font=ctk.CTkFont(size=20, weight='bold'))
        about.grid(row=0, column=0, padx=10, pady=(90, 0), sticky='nw')
        self.upper_frame = ctk.CTkFrame(self)
        self.upper_frame.grid(row=1, padx=10, sticky='new')

        self.description = ctk.CTkTextbox(self.upper_frame, width=1000, height=90,
                                          font=ctk.CTkFont(size=15, weight='bold'))
        self.description.grid(row=0, column=0, pady=2, columnspan=3, sticky='new')
        self.description.insert('0.0', text=self.read_description(self.textfile))
        self.description.configure(state='disabled')

        graph_text = ctk.CTkLabel(self, text='The Default Graph', font=ctk.CTkFont(size=20, weight='bold'))
        graph_text.grid(row=2, column=0, padx=10, pady=10, sticky='nw')
        graph_info = ctk.CTkLabel(self, text='A bar graph shows the number of “Items” sold in a different season'
                                  , font=ctk.CTkFont(size=15, weight='bold'))
        graph_info.grid(row=2, column=0, padx=10, pady=35, sticky='nw')

        item = ctk.CTkLabel(self, text='Select item', font=ctk.CTkFont(size=12, weight='bold'))
        item.grid(row=2, column=2, padx=(0, 10), pady=2, sticky='ne')
        self.item_combobox = ctk.CTkComboBox(self, state='readonly',
                                             values=SeasonalTrendModel().get_items(),
                                             variable=self.selected_item, command=self.plot_graph)
        self.item_combobox.grid(row=2, column=2, padx=10, pady=35, sticky='ne')

        self.graph_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.graph_frame.grid(row=2, column=0, pady=70, columnspan=3, rowspan=3, sticky="nsew")

        self.grap_button = ctk.CTkButton(self, text='More graph',command=self.open_toplevel)
        self.grap_button.grid(row=3, column=0, sticky='nsew', pady=(0, 10), padx=10, columnspan=3)


    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = MoreGraph(self)
        else:
            self.toplevel_window.focus()

    def create_default_bar(self):
        selected_item = self.selected_item.get()
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        data_model = SeasonalTrendModel()
        bar_plot = data_model.create_more_info_bar(selected_item)
        canvas = FigureCanvasTkAgg(bar_plot, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
        plt.close(bar_plot)

    def plot_graph(self, event):
        self.create_default_bar()

    def read_description(self, text):
        with open(text) as t:
            read_text = t.read()
        return read_text

class MoreGraph(ctk.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.geometry("800x600")

        self.label = ctk.CTkLabel(self,text='Toplevel')
        self.label.pack(padx=20,pady=20)
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Seasonal Trends")
        self.geometry("1280x720")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("custom-theme.json")
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
        self.quit()

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
