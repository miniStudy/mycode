from adminside.models import *
from adminside.automation_list import *
from django.db import connection




def creation(request, institute_domain, institute_email):
    board_creation(request, institute_domain)
    admin_creation(request, institute_domain, institute_email)

def board_creation(request, institute_domain):
    board = Boards.objects.create(
        brd_name="CBSE",
        domain_name=institute_domain
    )
    board.save()
    std_creation(institute_domain, board)

def std_creation(institute_domain, board):
    std = Std.objects.create(
        std_name = "5",
        std_board = board,
        domain_name = institute_domain
    )
    subject_creation(institute_domain, std, 'English')
    subject_creation(institute_domain, std, 'Mathematics')
    subject_creation(institute_domain, std, 'Environmental Studies')
    subject_creation(institute_domain, std, 'Hindi')
    
    std = Std.objects.create(
        std_name = "6",
        std_board = board,
        domain_name = institute_domain
    )
    subject_creation(institute_domain, std, 'English')
    subject_creation(institute_domain, std, 'Mathematics')
    subject_creation(institute_domain, std, 'Science')
    subject_creation(institute_domain, std, 'Social Science')
    subject_creation(institute_domain, std, 'Hindi')
    subject_creation(institute_domain, std, 'Sanskrit')
    subject_creation(institute_domain, std, 'Computer Science')

    std = Std.objects.create(
        std_name = "7",
        std_board = board,
        domain_name = institute_domain
    )
    subject_creation(institute_domain, std, 'English')
    subject_creation(institute_domain, std, 'Mathematics')
    subject_creation(institute_domain, std, 'Science')
    subject_creation(institute_domain, std, 'Social Science')
    subject_creation(institute_domain, std, 'Hindi')
    subject_creation(institute_domain, std, 'Sanskrit') 
    subject_creation(institute_domain, std, 'Computer Science')

    std = Std.objects.create(
        std_name = "8",
        std_board = board,
        domain_name = institute_domain
    )
    subject_creation(institute_domain, std, 'English')
    subject_creation(institute_domain, std, 'Mathematics')
    subject_creation(institute_domain, std, 'Science')
    subject_creation(institute_domain, std, 'Social Science')
    subject_creation(institute_domain, std, 'Hindi')
    subject_creation(institute_domain, std, 'Sanskrit')  # Optional Language
    subject_creation(institute_domain, std, 'Computer Science')

    std = Std.objects.create(
        std_name = "9",
        std_board = board,
        domain_name = institute_domain
    )
    subject_creation(institute_domain, std, 'English')
    subject_creation(institute_domain, std, 'Mathematics')
    subject_creation(institute_domain, std, 'Science')
    subject_creation(institute_domain, std, 'Social Science')
    subject_creation(institute_domain, std, 'Hindi')  # Optional language
    subject_creation(institute_domain, std, 'Sanskrit')  # Optional language
    subject_creation(institute_domain, std, 'Computer Science')  # Optional

    std = Std.objects.create(
        std_name = "10",
        std_board = board,
        domain_name = institute_domain
    )
    subject_creation(institute_domain, std, 'English')
    subject_creation(institute_domain, std, 'Mathematics')
    subject_creation(institute_domain, std, 'Science')
    subject_creation(institute_domain, std, 'Social Science')
    subject_creation(institute_domain, std, 'Hindi')  # Optional language
    subject_creation(institute_domain, std, 'Sanskrit')  # Optional language
    subject_creation(institute_domain, std, 'Computer Science')  # Optional

    

def subject_creation(institute_domain, std, subject_name):
    subject = Subject.objects.create(
        sub_name = subject_name,
        sub_std = std,
        domain_name = institute_domain
    )
    std = Std.objects.get(std_id = subject.sub_std.std_id)
    chapter_creation(institute_domain, English_5_CBSE, subject, std)


def chapter_creation(institute_domain, chep_name, chep_sub, chep_std):
    return_list = chapter_list_func(chep_sub, chep_std)
    counter = 0
    if len(return_list[0]) !=0:
        for x in return_list[0]:           
            chapter = Chepter.objects.create(
                chep_name = x,
                chep_sub = chep_sub,
                chep_std = chep_std,
                domain_name = institute_domain
            )
            lenth = len(return_list[1])
            if counter < lenth:
                path =  "MiniSudy-Materials/{}".format(return_list[1][counter])
                # insert_chapterwise_material(chapter.chep_id, chapter.chep_name, path, domain_name=institute_domain)
            counter += 1

    # chepter_list = chapter_list_func(chep_sub, chep_std)
    # for x in chepter_list:           
    #     chapter = Chepter.objects.create(
    #         chep_name = x,
    #         chep_sub = chep_sub,
    #         chep_std = chep_std,
    #         domain_name = institute_domain
    #     )

    
    
def insert_chapterwise_material(cm_chepter_id, cm_filename, cm_file, cm_file_icon=None, domain_name=None):
    with connection.cursor() as cursor:
        # Create the SQL insert query
        query = """
            INSERT INTO Chepterwise_Material (cm_chepter_id, cm_filename, cm_file, cm_file_icon, domain_name)
            VALUES (%s, %s, %s, %s, %s)
        """
        # Execute the query with the provided data
        cursor.execute(query, [cm_chepter_id, cm_filename, cm_file, cm_file_icon, domain_name])

from django.contrib.auth.hashers import make_password
def admin_creation(request, institute_domain, institute_email):
    admin = AdminData.objects.create(
            admin_name = 'admin',
            admin_pass = '12345678',
            admin_email = institute_email,
            domain_name = institute_domain
        )
    admin.admin_pass = make_password('12345678')
    admin.save()