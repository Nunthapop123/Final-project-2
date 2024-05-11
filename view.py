import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from model import SeasonalTrendModel
import matplotlib.pyplot as plt


class BasePage(ctk.CTkFrame):
    """A base class representing a page in the application."""

    def __init__(self, parent, *args, **kwargs):
        """Initialize the BasePage"""
        super().__init__(parent, *args, **kwargs)

    def show(self):
        """Display the page."""
        self.grid(row=0, column=1, rowspan=4, sticky="nsew")

    def hide(self):
        """Hide the page."""
        self.grid_forget()


class AnalyzePage(BasePage):
    """A class representing the Analyze Page in the application."""

    def __init__(self, parent, *args, **kwargs):
        """Initialize the AnalyzePage."""
        super().__init__(parent, *args, **kwargs)
        self.configure(fg_color='#424769')
        self.selected_season = ctk.StringVar()
        self.selected_graph = ctk.StringVar()
        self.selected_attribute = ctk.StringVar()
        self.selected_attribute2 = ctk.StringVar()
        self.selected_category = ctk.StringVar()
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.create_layout()
        self.season_combobox = None
        self.category_combobox = None
        self.attribute2 = None

    def create_layout(self):
        """Create the layout for the Analyze Page."""
        title = ctk.CTkLabel(self, text='Storytelling Page', font=ctk.CTkFont(size=30, weight='bold'))
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
        """Dynamically adjust the season combobox based on the selected graph type."""
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

    def correlation_combobox_layout(self):
        """Dynamically adjust the attribute2 combobox for correlation graph."""
        if self.attribute2 is None:
            self.attribute2_label = ctk.CTkLabel(self, text='Attribute2',
                                                 font=ctk.CTkFont(size=14, weight='bold'))
            self.attribute2_label.grid(row=1, column=3, padx=165, pady=2, sticky='w')
            self.attribute2 = ctk.CTkComboBox(self, state='readonly',
                                              values=['Age', 'Purchase Amount (USD)',
                                                      'Review Rating', 'Previous Purchases'],
                                              variable=self.selected_attribute2)
            self.attribute2.grid(row=2, column=3, padx=165, pady=2, sticky='w')

    def create_histogram(self):
        """Create a histogram based on selected attribute."""
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
        """Create a pie chart based on selected season."""
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
        """Create descriptive statistics based on selected season."""
        selected_season = self.selected_season.get()
        for widget in self.output_frame.winfo_children():
            widget.destroy()
        data_model = SeasonalTrendModel()
        descriptive = data_model.create_story_descriptive(selected_season)
        label1 = ctk.CTkLabel(self.output_frame, text=descriptive, font=ctk.CTkFont(size=15, weight='bold'))
        label1.grid(row=0, column=1)

    def create_bar(self):
        """Create a bar graph based on selected season and category."""
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

    def create_correlation(self):
        """Create a correlation scatter plot based on selected attributes and season."""
        selected_attribute = self.selected_attribute.get()
        selected_attribute2 = self.selected_attribute2.get()
        selected_season = self.selected_season.get()
        for widget in self.output_frame.winfo_children():
            widget.destroy()
        data_model = SeasonalTrendModel()
        scatter_plot = data_model.crete_story_scatter(selected_attribute, selected_attribute2, selected_season)
        canvas = FigureCanvasTkAgg(scatter_plot, master=self.output_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
        plt.close(scatter_plot)

    def update_attribute(self, choice):
        """Update the available attributes based on the selected graph type."""
        graph = self.selected_graph.get()
        if graph == 'Descriptive statistics':
            self.clear_combo()
            self.season_combobox_layout()
            self.attribute.configure(values=['Purchase Amount (USD)'])
            self.compute_button.configure(command=self.create_descriptive)
        elif graph == 'Correlation':
            self.clear_combo()
            self.season_combobox_layout()
            self.correlation_combobox_layout()
            self.attribute.configure(values=['Age', 'Purchase Amount (USD)',
                                             'Review Rating', 'Previous Purchases'])
            self.compute_button.configure(command=self.create_correlation)
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
        """Clear combo boxes."""
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
    """A class representing the Moreinfo Page in the application."""

    def __init__(self, parent, *args, **kwargs):
        """Initialize the MoreinfoPage."""
        super().__init__(parent, *args, **kwargs)
        self.configure(fg_color='#424769')
        self.textfile = 'description.txt'
        self.selected_item = ctk.StringVar()
        self.toplevel_window = None
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=3)
        self.page_layout()

    def page_layout(self):
        """Create the layout for the Moreinfo Page."""
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

        self.grap_button = ctk.CTkButton(self, text='More graph', command=self.open_toplevel)
        self.grap_button.grid(row=3, column=0, sticky='nsew', pady=(0, 10), padx=10, columnspan=3)

    def open_toplevel(self):
        """Open a new top-level window for additional graphs."""
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = MoreGraph(self)
        else:
            self.toplevel_window.focus()

    def create_default_bar(self):
        """Create a default bar graph based on selected item."""
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
        """Plot graph based on selected item."""
        self.create_default_bar()

    def read_description(self, text):
        """Read description from file.
        :param text: The file path of the description text file.
        :Returns str: The content of the description text file."""
        with open(text) as t:
            read_text = t.read()
        return read_text


class MoreGraph(ctk.CTkToplevel):
    """A class representing the MoreGraph Window in the application."""

    def __init__(self, parent, *args, **kwargs):
        """Initialize the MoreGraph window."""
        super().__init__(parent, *args, **kwargs)
        self.title('MoreGraphWindow')
        self.geometry("1024x768")
        self.configure(fg_color='#424769')
        self.selected_season = ctk.StringVar()
        self.selected_graph = ctk.StringVar()
        self.selected_attribute = ctk.StringVar()
        self.selected_attribute2 = ctk.StringVar()
        self.selected_category = ctk.StringVar()
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.create_layout_more_graph()
        self.season_combobox = None
        self.category_combobox = None
        self.attribute2 = None

    def create_layout_more_graph(self):
        """Create the layout for the MoreGraph window."""
        title = ctk.CTkLabel(self, text='More Graph', font=ctk.CTkFont(size=30, weight='bold'))
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

        self.exit_button = ctk.CTkButton(self, text='Exit', command=self.exit_button_event)
        self.exit_button.grid(row=3, column=0, padx=20, pady=35, sticky='s')

    def season_combobox_layout(self):
        """Dynamically adjust the season combobox based on the selected graph type."""
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

    def correlation_combobox_layout(self):
        """Dynamically adjust the attribute2 combobox for correlation graph."""
        if self.attribute2 is None:
            self.attribute2_label = ctk.CTkLabel(self, text='Attribute2',
                                                 font=ctk.CTkFont(size=14, weight='bold'))
            self.attribute2_label.grid(row=1, column=3, padx=10, pady=2, sticky='w')
            self.attribute2 = ctk.CTkComboBox(self, state='readonly',
                                              values=['Age', 'Purchase Amount (USD)',
                                                      'Review Rating', 'Previous Purchases'],
                                              variable=self.selected_attribute2)
            self.attribute2.grid(row=2, column=3, padx=10, pady=2, sticky='w')

    def create_histogram_more_graph(self):
        """Create a histogram based on selected attribute."""
        selected_attribute = self.selected_attribute.get()
        for widget in self.output_frame.winfo_children():
            widget.destroy()
        data_model = SeasonalTrendModel()
        histogram_plot = data_model.histogram_more_graph(selected_attribute)
        canvas = FigureCanvasTkAgg(histogram_plot, master=self.output_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
        plt.close(histogram_plot)

    def create_correlation_more_graph(self):
        """Create a correlation scatter plot based on selected attributes."""
        selected_attribute = self.selected_attribute.get()
        selected_attribute2 = self.selected_attribute2.get()
        for widget in self.output_frame.winfo_children():
            widget.destroy()
        data_model = SeasonalTrendModel()
        scatter_plot = data_model.scatter_more_graph(selected_attribute, selected_attribute2)
        canvas = FigureCanvasTkAgg(scatter_plot, master=self.output_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
        plt.close(scatter_plot)

    def create_pie_more_graph(self):
        """Create a pie chart based on selected attribute."""
        selected_attribute = self.selected_attribute.get()
        for widget in self.output_frame.winfo_children():
            widget.destroy()
        data_model = SeasonalTrendModel()
        pie_plot = data_model.pie_more_graph(selected_attribute)
        canvas = FigureCanvasTkAgg(pie_plot, master=self.output_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
        plt.close(pie_plot)

    def create_descriptive_more_graph(self):
        """Display descriptive statistics based on selected attribute."""
        selected_attribute = self.selected_attribute.get()
        for widget in self.output_frame.winfo_children():
            widget.destroy()
        data_model = SeasonalTrendModel()
        descriptive = data_model.descriptive_stats(selected_attribute)
        label1 = ctk.CTkLabel(self.output_frame, text=descriptive, font=ctk.CTkFont(size=15, weight='bold'))
        label1.grid(row=0, column=1)

    def create_bar_more_graph(self):
        """Create a bar graph based on selected attribute."""
        selected_attribute = self.selected_attribute.get()
        for widget in self.output_frame.winfo_children():
            widget.destroy()
        data_model = SeasonalTrendModel()
        bar_plot = data_model.bar_more_graph(selected_attribute)
        canvas = FigureCanvasTkAgg(bar_plot, master=self.output_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
        plt.close(bar_plot)

    def update_attribute(self, choice):
        """Update the available attributes based on the selected graph type."""
        graph = self.selected_graph.get()
        if graph == 'Descriptive statistics':
            self.clear_combo()
            self.season_combobox_layout()
            self.attribute.configure(values=['Age', 'Purchase Amount (USD)', 'Review Rating', 'Previous Purchases'])
            self.compute_button.configure(command=self.create_descriptive_more_graph)
        elif graph == 'Correlation':
            self.clear_combo()
            self.correlation_combobox_layout()
            self.attribute.configure(values=['Age', 'Purchase Amount (USD)', 'Review Rating', 'Previous Purchases'])
            self.compute_button.configure(command=self.create_correlation_more_graph)
        elif graph == 'Histogram':
            self.clear_combo()
            self.attribute.configure(values=['Purchase Amount (USD)', 'Review Rating', 'Previous Purchases'])
            self.compute_button.configure(command=self.create_histogram_more_graph)
        elif graph == 'Bar graph':
            self.clear_combo()
            self.season_combobox_layout()
            self.attribute.configure(values=['Gender', 'Category', 'Season', 'Subscription Status', 'Payment Method',
                                             'Frequency of Purchases'])
            self.compute_button.configure(command=self.create_bar_more_graph)
        elif graph == 'Pie graph':
            self.clear_combo()
            self.season_combobox_layout()
            self.attribute.configure(values=['Gender', 'Subscription Status', 'Discount Applied', 'Promo Code Used'])
            self.compute_button.configure(command=self.create_pie_more_graph)

    def clear_combo(self):
        """Clear combo boxes."""
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

    def exit_button_event(self):
        """Event handler for the exit button.Destroys the application window."""
        self.destroy()


class App(ctk.CTk):
    """A class representing the main application."""

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
        """Setup the sidebar with buttons."""
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0, fg_color="#2D3250")
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Seasonal Trends",
                                       font=ctk.CTkFont(size=35, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=40)

        self.pages = {}

        self.analyze_page_button = ctk.CTkButton(self.sidebar_frame, text="Storytelling",
                                                 font=ctk.CTkFont(weight='bold'),
                                                 command=lambda p=AnalyzePage: self.show_page(p))
        self.analyze_page_button.grid(row=1, column=0, padx=20, pady=30, ipadx=80)

        self.moreinfo_page_button = ctk.CTkButton(self.sidebar_frame, text="Moreinfo",
                                                  font=ctk.CTkFont(weight='bold'),
                                                  command=lambda p=MoreinfoPage: self.show_page(p))
        self.moreinfo_page_button.grid(row=2, column=0, padx=20, pady=5, ipadx=80)

        self.exit_button = ctk.CTkButton(self.sidebar_frame, text='Exit', command=self.exit_button_event)
        self.exit_button.grid(row=5, column=0, padx=20, pady=35)

        self.current_page = None
        self.show_page(AnalyzePage)

    def exit_button_event(self):
        """Event handler for the exit button.Quits the application."""
        self.quit()

    def show_page(self, page_class):
        """Show the specified page.
        :param page_class: The class of the page to be displayed."""
        if self.current_page:
            self.current_page.hide()
        self.current_page = page_class(self)
        self.current_page.show()

    def run(self):
        """Run the application."""
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.mainloop()
