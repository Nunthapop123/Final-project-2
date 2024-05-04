import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class SeasonalTrendModel:
    def __init__(self):
        self.df = pd.read_csv('shopping_trends_updated.csv')

    def get_columns(self):
        return list(self.df.columns)

    def create_story_histogram(self, columns):
        ax = sns.histplot(data=self.df, x=columns, hue='Season', kde=True, multiple='stack')
        ax.set_title('Purchase Amount Distribution by Season')
        ax.set_xlabel('Purchase Amount (USD)')
        ax.set_ylabel('Frequency')
        return ax.figure


if __name__ == '__main__':
    a = SeasonalTrendModel()
    print(a.get_columns())
