import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class SeasonalTrendModel:
    """A class representing a model for analyzing seasonal shopping trends."""
    def __init__(self):
        """Initialize the SeasonalTrendModel."""
        self.df = pd.read_csv('shopping_trends_updated.csv')

    def get_columns(self):
        """Get the column names of the DataFrame.
        :return list: A list of column names."""
        return list(self.df.columns)

    def get_items(self):
        """Get the unique items purchased.
        :return list: A list of unique items purchased."""
        return list(self.df['Item Purchased'].unique())

    def filter_season_data(self, season):
        """Filter the data based on the specified season.
        :param season: The season to filter the data by.
        :return pd.DataFrame: The filtered DataFrame."""
        season_data = self.df[self.df['Season'] == season].copy()
        return season_data

    def create_story_histogram(self, columns):
        """Create a histogram of purchase amounts by season.
         :param columns: Column(s) to plot on the x-axis.
         :return Figure: The matplotlib figure object containing the histogram."""
        fig, ax = plt.subplots()
        ax = sns.histplot(data=self.df, x=columns, hue='Season', kde=True, multiple='stack')
        ax.set_title('Purchase Amount Distribution by Season')
        ax.set_xlabel('Purchase Amount (USD)')
        ax.set_ylabel('Frequency')
        return fig

    def create_story_pie(self, season):
        """Create a pie chart showing the distribution of items purchased by category for a given season.
        :param season: The season to analyze.
        :return Figure: The matplotlib figure object containing the pie chart."""
        season_data = self.df[self.df['Season'] == season]
        category_distribution = season_data['Category'].value_counts(normalize=True)
        fig, ax = plt.subplots()
        ax.pie(category_distribution, labels=category_distribution.index, autopct='%1.1f%%', startangle=140)
        ax.set_title(f'Distribution of Items Purchased by Category for {season}')
        ax.axis('equal')
        return fig

    def create_story_descriptive(self, season):
        """Generate descriptive statistics of purchase amounts for a given season.
        :param season: The season to analyze.
        :return Series: A pandas Series containing the descriptive statistics."""
        if season not in self.df['Season'].unique():
            print(f"Error: Season '{season}' not found in the data.")
            return None

        season_data = self.filter_season_data(season)
        data = season_data['Purchase Amount (USD)']
        descriptive = data.describe()
        return descriptive

    def crete_story_scatter(self, attribute1, attribute2, season):
        season_df = self.df[self.df['Season'] == season]
        fig, ax = plt.subplots()
        ax.scatter(season_df[attribute1], season_df[attribute2], alpha=0.5)
        ax.set_xlabel(f'{attribute1}')
        ax.set_ylabel(f'{attribute2}')
        ax.set_title(f'Scatter Plot of {attribute1} and {attribute2} ')
        return fig

    def create_story_bar(self, season, category):
        """Create a bar chart showing the sales of items in a specific category during a particular season.
        :param season: The season to analyze.
               category: The category of items to plot.
        :return Figure: The matplotlib figure object containing the bar chart."""
        category_data = self.df[(self.df['Category'] == category) & (self.df['Season'] == season)]
        category_item_sale = category_data.groupby('Item Purchased').size()
        fig, ax = plt.subplots()
        category_item_sale.plot(kind='bar', color='skyblue')
        ax.set_title(f'Sales of {category} Items in {season} Season')
        ax.set_xlabel(f'{category} Item')
        ax.set_ylabel('Number of Sales')
        for tick in ax.get_xticklabels():
            tick.set_rotation(45)
        return fig

    def create_more_info_bar(self, item):
        """Create a bar chart showing the number of a specific item sold in different seasons.
        :param item: The item to analyze.
        :return Figure: The matplotlib figure object containing the bar chart."""
        item_sales = self.df[self.df['Item Purchased'] == item]
        item_sales_season = item_sales.groupby('Season').size()
        fig, ax = plt.subplots()
        item_sales_season.plot(kind='bar', color='skyblue')
        ax.set_title(f'Number of {item} sold in Different Seasons')
        ax.set_xlabel(f'Season')
        ax.set_ylabel(f'Number of {item} Sold')
        for tick in ax.get_xticklabels():
            tick.set_rotation(0)
        return fig

    def descriptive_stats(self, attribute):
        """Generate descriptive statistics for a given attribute in the dataset.
        :param attribute: The attribute/column name for which descriptive statistics are calculated.
        :return Series: A pandas Series containing the descriptive statistics."""
        data = self.df[attribute]
        descriptive = data.describe()
        return descriptive

    def histogram_more_graph(self, attribute):
        """Create a histogram to visualize the distribution of a given attribute in the dataset.
        :param attribute: The attribute/column name to plot.
        :return Figure: The matplotlib figure object containing the histogram."""
        fig, ax = plt.subplots()
        self.df[attribute].plot(kind='hist', bins=20, color='green')
        ax.set_title(f'{attribute} Distribution')
        ax.set_xlabel(f'{attribute}')
        ax.set_ylabel(f'Frequency')
        return fig

    def bar_more_graph(self, attribute):
        """Create a bar chart to visualize the distribution of a given attribute in the dataset.
        :param attribute: The attribute/column name to plot.
        :return Figure: The matplotlib figure object containing the bar chart."""
        fig, ax = plt.subplots()
        self.df[attribute].value_counts().plot(kind='bar', color='skyblue')
        ax.set_title(f'{attribute} Distribution')
        ax.set_xlabel(f'{attribute}')
        ax.set_ylabel(f'Frequency')
        for tick in ax.get_xticklabels():
            tick.set_rotation(45)
        return fig

    def pie_more_graph(self, attribute):
        """Create a pie chart to visualize the distribution of a given attribute in the dataset.
           :param attribute: The attribute/column name to plot.
           :return Figure: The matplotlib figure object containing the pie chart."""
        fig, ax = plt.subplots()
        self.df[attribute].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90)

        ax.set_title(f'{attribute} Distribution')
        ax.axis('count')
        return fig

    def scatter_more_graph(self, attribute1, attribute2):
        """Create a scatter plot to visualize the relationship between two attributes in the dataset.
           :param attribute1: The first attribute/column name to plot on the x-axis.
                  attribute2: The second attribute/column name to plot on the y-axis.
           :return Figure: The matplotlib figure object containing the scatter plot."""
        fig, ax = plt.subplots()
        ax.scatter(self.df[attribute1], self.df[attribute2])
        ax.set_xlabel(f'{attribute1}')
        ax.set_ylabel(f'{attribute2}')
        ax.set_title(f'Scatter Plot of {attribute1} and {attribute2} ')
        return fig


if __name__ == '__main__':
    a = SeasonalTrendModel()
    print(a.get_columns())
    print(a.filter_season_data('Summer').head())
