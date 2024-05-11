import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class SeasonalTrendModel:
    def __init__(self):
        self.df = pd.read_csv('shopping_trends_updated.csv')

    def get_columns(self):
        return list(self.df.columns)

    def filter_season_data(self, season):
        season_data = self.df[self.df['Season'] == season].copy()
        return season_data

    def create_story_histogram(self, columns):
        fig, ax = plt.subplots()
        ax = sns.histplot(data=self.df, x=columns, hue='Season', kde=True, multiple='stack')
        ax.set_title('Purchase Amount Distribution by Season')
        ax.set_xlabel('Purchase Amount (USD)')
        ax.set_ylabel('Frequency')
        return fig

    def create_story_pie(self, season):
        season_data = self.df[self.df['Season'] == season]
        category_distribution = season_data['Category'].value_counts(normalize=True)
        fig, ax = plt.subplots()
        ax.pie(category_distribution, labels=category_distribution.index, autopct='%1.1f%%', startangle=140)
        ax.set_title(f'Distribution of Items Purchased by Category for {season}')
        ax.axis('equal')
        return fig

    def create_descriptive(self, season):
        if season not in self.df['Season'].unique():
            print(f"Error: Season '{season}' not found in the data.")
            return None

        season_data = self.filter_season_data(season)
        data = season_data['Purchase Amount (USD)']
        descriptive = data.describe()
        return descriptive

    def create_story_bar(self, season, category):
        category_data = self.df[(self.df['Category'] == category) & (self.df['Season'] == season)]
        category_item_sale = category_data.groupby('Item Purchased').size()
        fig, ax = plt.subplots()
        category_item_sale.plot(kind='bar',color='skyblue')
        ax.set_title(f'Sales of {category} Items in {season} Season')
        ax.set_xlabel(f'{category} Item')
        ax.set_ylabel('Number of Sales')
        # ax.xticks(rotation=45)
        # ax.tight_layout()
        return fig


if __name__ == '__main__':
    a = SeasonalTrendModel()
    print(a.get_columns())
    print(a.filter_season_data('Summer').head())
