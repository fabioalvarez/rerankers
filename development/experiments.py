import pandas as pd

from development import enums


class Products:
    def __init__(self, documents, filters):
        self.df: pd.DataFrame = documents
        self.conditions = []
        self.filtered_ids = self.filter_products(filters)

    def add_contains_filter(self, column, value):
        self.conditions.append(self.df[column].str.contains(value, case=False, na=False))

    def add_not_contains_filter(self, column, value):
        self.conditions.append(~self.df[column].str.contains(value, case=False, na=False))

    def add_equals_filter(self, column, value):
        self.conditions.append(self.df[column] == value)

    def add_or_contains_filter(self, column, value):
        if self.conditions:
            self.conditions[-1] = self.conditions[-1] | self.df[column].str.contains(value, case=False, na=False)
        else:
            raise ValueError("No previous condition to combine with")

    def add_or_equals_filter(self, column, value):
        if self.conditions:
            self.conditions[-1] = self.conditions[-1] | self.df[column].str.contains(value, case=False, na=False)
        else:
            raise ValueError("No previous condition to combine with")

    def format_filters(self, filters):
        for column, value, condition_type in filters:
            match condition_type:
                case 'contains':
                    self.add_contains_filter(column, value)
                case 'not_contains':
                    self.add_not_contains_filter(column, value)
                case 'or_contains':
                    self.add_or_contains_filter(column, value)
                case 'equals':
                    self.add_equals_filter(column, value)
                case 'or_equals':
                    self.add_or_equals_filter(column, value)
                case _:
                    raise ValueError(f"Unknown condition type: {condition_type}")

    def filter_products(self, filters):
        self.format_filters(filters)

        if self.conditions:
            combined_condition = self.conditions[0]

            for condition in self.conditions[1:]:
                combined_condition &= condition

            return self.df[combined_condition]["id"].tolist()


def experiments_factory(df, experiment):
    filters = []

    match experiment:
        case 'puma t-shirt men':
            filters = enums.puma_filters
        case 'nike t-shirt men':
            filters = enums.nike_filters
        case 'jeans men':
            filters = enums.jeans_men_filter
        case 'jeans women':
            filters = enums.jeans_women_filter
        case 'watch men':
            filters = enums.watch_men_filter
        case 'watch women':
            filters = enums.watch_women_filter
        case 'girl kids':
            filters = enums.kids_girl_filter
        case 'boy kids':
            filters = enums.kids_boy_filter
        case 'casual t-shirts men':
            filters = enums.casual_t_shirts_men_filter
        case 'casual t-shirts women':
            filters = enums.casual_t_shirts_women_filter
        case 'summer t-shirts men':
            filters = enums.summer_t_shirts_men_filter
        case 'fall t-shirts women':
            filters = enums.fall_t_shirts_women_filter
        case _:
            raise ValueError(f"Unknown experiment: {experiment}")

    return Products(df, filters).filtered_ids

if __name__ == "__main__":
    df = pd.read_csv("../dataset/products.csv")
    results = len(experiments_factory(df, 'puma t-shirt'))
    print(results)
