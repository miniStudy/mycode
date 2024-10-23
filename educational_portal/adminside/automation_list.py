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

EVS_5_CBSE = [
        'Chapter 1: Super Senses',
        'Chapter 2: A Snake Charmer\'s Story',
        'Chapter 3: From Tasting to Digesting',
        'Chapter 4: Mangoes Round the Year',
        'Chapter 5: Seeds and Seeds',
        'Chapter 6: Every Drop Counts',
        'Chapter 7: Experiments with Water',
        'Chapter 8: A Treat for Mosquitoes',
        'Chapter 9: Up You Go!',
        'Chapter 10: Walls Tell Stories',
        'Chapter 11: Sunita in Space',
        'Chapter 12: What if it Finishes ...?',
        'Chapter 13: A Shelter so High!',
        'Chapter 14: When the Earth Shook!',
        'Chapter 15: Blow Hot, Blow Cold',
        'Chapter 16: Who will do this Work?',
        'Chapter 17: Across the Wall',
        'Chapter 18: No Place for Us?',
        'Chapter 19: A Seed tells a Farmer\'s Story',
        'Chapter 20: Whose Forests?',
        'Chapter 21: Like Father, Like Daughter',
        'Chapter 22: On the Move Again'
    ]

Hindi_5_CBSE = [
        'Chapter 1: राख की रस्सी',
        'Chapter 2: फसलों के त्योहार',
        'Chapter 3: खिलौनेवाला',
        'Chapter 4: नन्हा फनकार',
        'Chapter 5: जहाँ चाह वहाँ राह',
        'Chapter 6: चिट्ठी का सफ़र',
        'Chapter 7: डाकिए की कहानी, कुँवरसिंह की ज़ुबानी',
        'Chapter 8: वे दिन भी क्या दिन थे',
        'Chapter 9: एक माँ की बेबसी',
        'Chapter 10: एक दिन की बादशाहत',
        'Chapter 11: चावल की रोटियाँ',
        'Chapter 12: गुरु और चेला',
        'Chapter 13: स्वामी की दादी',
        'Chapter 14: बाघ आया उस रात'
    ]





def chapter_list_func(chep_sub, chep_std):
    if chep_sub.sub_name == 'English' and chep_std.std_name == '5':
        return English_5_CBSE
    
    elif chep_sub.sub_name == 'Mathematics' and chep_std.std_name == '5':
        return Maths_5_CBSE
    
    else:
        return []

    
