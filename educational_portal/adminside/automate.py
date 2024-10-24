from adminside.models import *
from adminside.automation_list import *


def creation(request, institute_domain):
    domain_name = request.get_host()
    board_creation(request, domain_name)

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
    chepter_list = chapter_list_func(chep_sub, chep_std)
    for x in chepter_list:           
        chapter = Chepter.objects.create(
            chep_name = x,
            chep_sub = chep_sub,
            chep_std = chep_std,
            domain_name = institute_domain
        )

    
    