k_to_eval = [2, 6, 10, 16, 20, 30, 40, 50, 60]

metrics = {
    "query": [],
    "k": [],
    "max_k": [],
    "precision": [],
    "recall": [],
    "results": [],
    "source": [],
}

experiments = [
        "puma t-shirt men",
        "nike t-shirt men",
        "jeans men",
        "jeans women",
        "watch men",
        "watch women",
        "girl kids",
        "boy kids",
        "casual t-shirts men",
        "casual t-shirts women",
        "summer t-shirts men",
        "fall t-shirts women"
    ]

# Filters
puma_filters = [
    ('productDisplayName', 'puma', 'contains'),
    ('gender', 'Men', 'equals'),
    ('productDisplayName', 't-shirt', 'contains'),
    ('productDisplayName', 'tshirt', 'or_contains')
]

nike_filters = [
    ('productDisplayName', 'nike', 'contains'),
    ('gender', 'Men', 'equals'),
    ('productDisplayName', 't-shirt', 'contains'),
    ('productDisplayName', 'tshirt', 'or_contains')
]

jeans_men_filter = [
    ('gender', 'Men', 'equals'),
    ('articleType', 'Jeans', 'equals'),
    ('productDisplayName', 'jeans', 'or_contains')
]

jeans_women_filter = [
    ('gender', 'Women', 'equals'),
    ('gender', 'Girls', 'or_contains'),
    ('articleType', 'Jeans', 'equals'),
    ('productDisplayName', 'jeans', 'or_contains')
]

watch_men_filter = [
    ('gender', 'Men', 'equals'),
    ('productDisplayName', 'watch', 'contains'),
]

watch_women_filter = [
    ('gender', 'Women', 'equals'),
    ('productDisplayName', 'watch', 'contains'),
]

kids_girl_filter = [
    ('productDisplayName', 'girl', 'contains'),
    ('gender', 'Women', 'or_equals'),
    ('gender', 'Girl', 'or_equals'),
    ('gender', 'Girls', 'or_equals'),
    ('productDisplayName', 'kid', 'or_contains'),
]

kids_boy_filter = [
    ('productDisplayName', 'boy', 'contains'),
    ('gender', 'Men', 'equals'),
    ('gender', 'Boy', 'or_equals'),
    ('gender', 'Boys', 'or_equals'),
    ('productDisplayName', 'kid', 'or_contains'),
]

casual_t_shirts_men_filter = [
    ('gender', 'Men', 'equals'),
    ('gender', 'Boy', 'or_equals'),
    ('usage', 'Casual', 'equals'),
    ('productDisplayName', 't-shirt', 'contains'),
    ('productDisplayName', 'tshirt', 'or_contains')
]

casual_t_shirts_women_filter = [
    ('gender', 'Women', 'equals'),
    ('gender', 'Girl', 'or_equals'),
    ('usage', 'Casual', 'equals'),
    ('productDisplayName', 't-shirt', 'contains'),
    ('productDisplayName', 'tshirt', 'or_contains')

]

summer_t_shirts_men_filter = [
    ('gender', 'Men', 'equals'),
    ('gender', 'Boy', 'or_equals'),
    ('season', 'Summer', 'equals'),
    ('productDisplayName', 't-shirt', 'contains'),
    ('productDisplayName', 'tshirt', 'or_contains')
]

fall_t_shirts_women_filter = [
    ('gender', 'Women', 'equals'),
    ('gender', 'Girl', 'or_equals'),
    ('season', 'Fall', 'equals'),
    ('productDisplayName', 't-shirt', 'contains'),
    ('productDisplayName', 'tshirt', 'or_contains')

]