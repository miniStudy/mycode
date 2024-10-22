English_5_CBSE = [
        'Chapter 1: The Magic Garden',
        'Chapter 2: The Friendly Mongoose',
        'Chapter 3: The Shepherd\'s Treasure',
        'Chapter 4: The Old-Clock Shop',
        'Chapter 5: Topsy-Turvy Land',
        'Chapter 6: The Wonder of Nature',
        'Chapter 7: A Busy Month',
        'Chapter 8: The Story of the Road',
        'Chapter 9: What Do We Do With a Tail Like This?',
        'Chapter 10: The Man Who Knew Too Much',
        'Chapter 11: A Different Kind of School',
        'Chapter 12: The Black Aeroplane',
        'Chapter 13: The Little Girl',
        'Chapter 14: The Treasure Within',
        'Chapter 15: When the Mountain Spoke',
        'Chapter 16: A Gift of Chappals',
        'Chapter 17: The Blue Sky',
        'Chapter 18: The Good and the Bad'
    ]

Maths_5_CBSE = [
        'Chapter 1: Shapes and Angles',
        'Chapter 2: Nets and 3D Shapes',
        'Chapter 3: Operations on Large Numbers',
        'Chapter 4: Basic Geometrical Ideas',
        'Chapter 5: Understanding Elementary Shapes',
        'Chapter 6: Fractions',
        'Chapter 7: Decimals',
        'Chapter 8: Data Handling',
        'Chapter 9: Patterns',
        'Chapter 10: Simple and Compound Interest',
        'Chapter 11: Algebra',
        'Chapter 12: Ratio and Proportion',
        'Chapter 13: Comparing Quantities',
        'Chapter 14: Geometry',
        'Chapter 15: Construction',
        'Chapter 16: Time',
        'Chapter 17: Money',
        'Chapter 18: Perimeter and Area',
        'Chapter 19: Volume and Capacity'
    ]





def chapter_list_func(chep_sub, chep_std):
    if chep_sub.sub_name == 'English' and chep_std.std_name == '5':
        return English_5_CBSE
    
    elif chep_sub.sub_name == 'Mathematics' and chep_std.std_name == '5':
        return Maths_5_CBSE
    
    else:
        return []

    
