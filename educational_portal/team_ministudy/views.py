from django.shortcuts import render, redirect, get_object_or_404
from adminside.automate import *
from django.contrib import messages
from team_ministudy.models import *
from team_ministudy.forms import *
from datetime import timedelta
from django.utils.timezone import now
import pandas as pd
from django.core.paginator import Paginator


# Create your views here.


def paginatoorrr(queryset,request):
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return page_obj

def team_ministudy_home(request):
    return render(request, 'ministudy/ministudy_home.html')


def show_institute_function(request):
    institute_data = NewInstitution.objects.all()
    context = {'institute_data': institute_data}
    return render(request, 'ministudy/show_institute.html', context)


def insert_update_institute_function(request):
    if request.GET.get('pk'):
        pk = request.GET['pk']
        instance = get_object_or_404(NewInstitution, pk=pk)
        if request.method == "POST":
            form = Institute_Form(request.POST, instance = instance)
            if form.is_valid():
                form.save()
                return redirect('show_institute')
            else:
                return render(request, 'ministudy/insert_update_institute.html')
        else:
            return render(request, 'ministudy/insert_update_institute.html')

    if request.GET.get('update_id'):
        update_id = request.GET.get('update_id')
        update_data = get_object_or_404(NewInstitution, institute_id=update_id)
        context = {'update_data': update_data}
        return render(request, 'ministudy/insert_update_institute.html', context)
    
    if request.method == 'POST':
        institute_name = request.POST['institute_name']
        institute_email = request.POST['institute_email']
        institute_contact = request.POST['institute_contact']
        institute_domain = request.POST['institute_domain']
        institute_logo = request.FILES['institute_logo']

        NewInstitution.objects.create(institute_name = institute_name, institute_email = institute_email, institute_contact = institute_contact, institute_logo = institute_logo, institute_domain = institute_domain)
        creation(request, institute_domain, institute_email)
        return redirect('show_institute')
    return render(request, 'ministudy/insert_update_institute.html')

def show_ministudy_payment_function(request):
    ministudy_payment_data = MinistudyPayment.objects.all()
    context = {'ministudy_payment_data': ministudy_payment_data}
    return render(request, 'ministudy/show_ministudy_pay.html', context)

def insert_update_ministudy_payment_function(request):
    students_data = Students.objects.all()
    update_data = None
    if request.GET.get('pk'):
        instance = get_object_or_404(MinistudyPayment, pk=request.GET['pk'])
        if request.method == 'POST':
            form = Ministudy_Payment_Form(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('show_ministudy_payment')
            else:
                return render(request, 'ministudy/insert_update_ministudy_pay.html')

    if request.GET.get('update_id'):
        update_id = request.GET.get('update_id')
        update_data = MinistudyPayment.objects.get(ministudypay_id = update_id)
        return render(request, 'ministudy/insert_update_ministudy_pay.html', {'update_data': update_data, 'students_data': students_data})
    else:
        if request.method == 'POST':
            form = Ministudy_Payment_Form(request.POST)
            if form.is_valid():
                form.save()
                return redirect('show_ministudy_payment')
            else:
                return render(request, 'ministudy/insert_update_ministudy_pay.html')
    return render(request, 'ministudy/insert_update_ministudy_pay.html', {'students_data': students_data, 'update_data': update_data})



def institute_lock_function():
    unlocked_institutes = NewInstitution.objects.filter(institute_lock=False)
    for institute in unlocked_institutes:
        lock_date = institute.institute_joining_date + timedelta(days=15)
        
        if now() >= lock_date:
            institute.institute_lock = True
            institute.save()


def remove_institute_function(request):
    if request.GET.get('remove_id'):
        institute_id = request.GET.get('remove_id')
        remove_data = NewInstitution.objects.get(institute_id = institute_id)
        Boards.objects.filter(domain_name=remove_data.institute_domain).delete()
        AdminData.objects.filter(domain_name = remove_data.institute_domain).delete()
        Event.objects.filter(domain_name = remove_data.institute_domain).delete()
        Banks.objects.filter(domain_name = remove_data.institute_domain).delete()
        Notification.objects.filter(domain_name = remove_data.institute_domain).delete()
        Chatbox.objects.filter(domain_name = remove_data.institute_domain).delete()
        Expense.objects.filter(domain_name = remove_data.institute_domain).delete()
        Groups.objects.filter(domain_name = remove_data.institute_domain).delete()
        Faculties.objects.filter(domain_name = remove_data.institute_domain).delete()
        remove_data.delete()  
        messages.success(request, 'Institute deleted successfully!')
        return redirect('show_institute')
    return redirect('show_institute')


def bulk_upload_questions(request):
    if request.method == 'POST':
        qb_chapter_id = request.POST.get('tq_chapter')  # Corrected variable name
        qb_chapter = Chepter.objects.get(chep_id=qb_chapter_id)

        # Extract all question entries
        
        qb_subject = qb_chapter.chep_sub.sub_name
        qb_std = qb_chapter.chep_std.std_name
        questions_data = request.POST.getlist('question[]')
        q_types = request.POST.getlist('q_type[]')
        answers = request.POST.getlist('answer[]')
        weightages = request.POST.getlist('weightage[]')
        options_a = request.POST.getlist('option_a[]')
        options_b = request.POST.getlist('option_b[]')
        options_c = request.POST.getlist('option_c[]')
        options_d = request.POST.getlist('option_d[]')

        # Save each question entry
        for i in range(len(questions_data)):
            question_bank.objects.create(
                qb_chepter=qb_chapter,
                qb_subject=qb_subject,
                qb_std=qb_std,
                qb_q_type=q_types[i],
                qb_question=questions_data[i],
                qb_answer=answers[i],
                qb_weightage=weightages[i],
                qb_optiona=options_a[i] if q_types[i] == 'MCQ' else None,
                qb_optionb=options_b[i] if q_types[i] == 'MCQ' else None,
                qb_optionc=options_c[i] if q_types[i] == 'MCQ' else None,
                qb_optiond=options_d[i] if q_types[i] == 'MCQ' else None,
            )

        return redirect('show_question_bank')  # Redirect to the same page after submission
    chap_data = Chepter.objects.filter(chep_std__std_id = 13).values('chep_id','chep_name','chep_sub__sub_name','chep_sub__sub_std__std_name')
    que_type_choices = question_bank.que_type.choices
    context={'chap_data':chap_data,'que_type_choices':que_type_choices}
    return render(request, 'insert_update/bulk_upload_test_questions.html',context)



def show_question_bank(request):
    # excel_data = pd.read_excel('chepter_list.xlsx')
    # chapter_names = excel_data['Chapter Name'].tolist()
    # standard_names = excel_data['Chapter Standard'].tolist()
    # subject_names = excel_data['Chepter Subject'].tolist()
    # questions = question_bank.objects.values('qb_id', 'qb_chepter')
    # for i, question in enumerate(questions):
    #     if i < len(chapter_names):
    #         qb_id = question['qb_id']
    #         chapter_name = chapter_names[i]
    #         standard_name = standard_names[i]
    #         subject_name = subject_names[i]
    #         qb = question_bank.objects.get(qb_id = qb_id)
    #         qb.qb_chepter = chapter_name
    #         qb.qb_std = standard_name
    #         qb.qb_subject = subject_name
    #         qb.save()

    question_answers = question_bank.objects.values('qb_chepter','qb_std', 'qb_subject', 'qb_q_type', 'qb_question', 'qb_answer', 'qb_weightage','qb_optiona','qb_optionb','qb_optionc','qb_optiond')
    total_questions = question_bank.objects.all().count()

    # chepters_names_with_ids = question_bank.objects.values_list('qb_chepter', 'qb_std', 'qb_subject', 'qb_q_type','qb_question','qb_answer','qb_weightage','qb_optiona','qb_optionb','qb_optionc','qb_optiond')
    # chepter_list = [(chep_name, chep_std, che_sub, que_type, question, answer, weightage, q_optiona, q_optionb, q_optionc, q_optiond) for chep_name, chep_std, che_sub, que_type, question, answer, weightage, q_optiona, q_optionb, q_optionc, q_optiond in chepters_names_with_ids]
    # df = pd.DataFrame(chepter_list, columns=['Chapter Name', 'Chapter Standard', 'Chepter Subject', 'Question Type', 'Question', 'Answer', 'Weightage', 'Option A', 'Option B', 'Option C', 'Option D'])
    # df.to_excel('chepter_list.xlsx', index=False)
    

    questions = paginatoorrr(question_answers,request)
    return render(request, 'show_question_bank.html', {'questions': questions, 'total_questions':total_questions, 'question_answers': question_answers})


def edit_question_bankk(request):
    domain = request.get_host()
    # Fetch the specific question to edit
    updateid = request.GET.get('updateid')
    question = get_object_or_404(question_bank, qb_id=updateid)
    
    if request.method == 'POST':
        # Update the question details from form data
        chepter_object = Chepter.objects.get(chep_id=request.POST.get('gb_chepter'))
        question.qb_chepter = chepter_object.chep_name
        question.qb_subject = chepter_object.chep_sub.sub_name
        question.qb_std = chepter_object.chep_std.std_name
        question.qb_q_type = request.POST.get('qb_q_type')
        question.qb_question = request.POST.get('qb_question')
        question.qb_answer = request.POST.get('qb_answer')
        question.qb_weightage = request.POST.get('qb_weightage')
        
        # Update options based on question type
        if question.qb_q_type == 'MCQ':
            question.qb_optiona = request.POST.get('qb_optiona')
            question.qb_optionb = request.POST.get('qb_optionb')
            question.qb_optionc = request.POST.get('qb_optionc')
            question.qb_optiond = request.POST.get('qb_optiond')
        else:
            # Clear options if not MCQ
            question.qb_optiona = None
            question.qb_optionb = None
            question.qb_optionc = None
            question.qb_optiond = None
        
        # Save the updated question to the database
        question.save()
        return redirect('show_question_bank')  # Redirect back to the question list page

    # Render edit form with existing question data
    chap_data = Chepter.objects.filter(chep_sub__sub_std__std_id = 13, domain_name = domain).values('chep_id','chep_name','chep_sub__sub_name','chep_sub__sub_std__std_name')
    que_type_choices = question_bank.que_type.choices
    context = {
        'question': question,
        'chap_data': chap_data,
        'que_type_choices': que_type_choices,
    }
    return render(request, 'insert_update/edit_question_bank.html', context)


def delete_question_bank(request):
    qb_id = request.GET.get('qb_id')
    if qb_id:
        question = get_object_or_404(question_bank, qb_id=qb_id)
        question.delete()

    # Redirect back to the list of questions
    return redirect('show_question_bank')
