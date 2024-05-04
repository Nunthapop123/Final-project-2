import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class SeasonalTrendModel:
    def __init__(self):
        self.df = pd.read_csv('shopping_trends_updated.csv')

    def get_columns(self):
        return list(self.df.columns)

    # def filter_season_data(self, season):
    #     season_data = self.df[self.df['Season'] == season].copy()
    #     return season_data

    def create_story_histogram(self, columns):
        ax = sns.histplot(data=self.df, x=columns, hue='Season', kde=True, multiple='stack')
        ax.set_title('Purchase Amount Distribution by Season')
        ax.set_xlabel('Purchase Amount (USD)')
        ax.set_ylabel('Frequency')
        return ax.figure

    def create_story_pie(self,season):
        season_data = self.df[self.df['Season'] == season]
        category_distribution = season_data['Category'].value_counts(normalize=True)
        plt.pie(category_distribution, labels=category_distribution.index, autopct='%1.1f%%', startangle=140)
        plt.title(f'Distribution of Items Purchased by Category for')
        plt.axis('equal')
        return plt.figure


if __name__ == '__main__':
    a = SeasonalTrendModel()
    print(a.get_columns())
