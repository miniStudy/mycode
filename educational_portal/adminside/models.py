from django.db import models
from datetime import timedelta
from django_summernote.fields import SummernoteTextField
import random

class AdminData(models.Model):
    admin_id = models.BigAutoField(primary_key=True)
    admin_name = models.CharField(max_length=20)
    admin_pass = models.CharField(max_length=100)
    admin_email = models.EmailField(unique=True)
    admin_otp = models.IntegerField(blank=True,null=True)
    domain_name = models.CharField(blank=True,null=True,max_length=100)
    admin_onesignal_player_id = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.admin_email}"
    
    class Meta:
        db_table = 'AdminData'


class Boards(models.Model):
    brd_id = models.BigAutoField(primary_key=True)
    brd_name = models.CharField(max_length=20)
    domain_name = models.CharField(blank=True,null=True,max_length=100)
    
    def __str__(self):
        return f"{self.brd_name}"
    
    class Meta:
        db_table = 'Boards'

class Std(models.Model):
    std_id = models.BigAutoField(primary_key=True)
    std_name = models.CharField(max_length=10)
    std_board = models.ForeignKey(Boards, on_delete=models.CASCADE)
    domain_name = models.CharField(blank=True,null=True,max_length=100)    

    def __str__(self):
        return f"{self.std_name} - {self.std_board}"
    
    class Meta:
        db_table = 'std'



class Subject(models.Model):
    sub_id = models.BigAutoField(primary_key=True)
    sub_name = models.CharField(max_length=50)
    sub_std = models.ForeignKey(Std, on_delete=models.CASCADE)
    domain_name = models.CharField(blank=True,null=True,max_length=100)    

    def __str__(self):
        return f"{self.sub_name} - {self.sub_std.std_name} | {self.sub_std.std_board.brd_name}"
    
    class Meta:
        db_table = 'subject'

class Chepter(models.Model):
    chep_id = models.BigAutoField(primary_key=True)
    chep_name = models.CharField(max_length=100)
    chep_sub = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    chep_sem = models.CharField(max_length=20,blank=True)
    chep_std = models.ForeignKey(Std,on_delete=models.CASCADE)
    chep_icon = models.ImageField(upload_to='uploads/')
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.chep_name} - {self.chep_sem} {self.chep_std}"
    
    class Meta:
        db_table = 'chepter'

class Chepterwise_material(models.Model):
    cm_id = models.BigAutoField(primary_key=True)
    cm_chepter = models.ForeignKey(Chepter,on_delete=models.CASCADE)
    cm_filename = models.CharField(max_length=100)
    cm_file = models.FileField(upload_to ='uploads/')
    cm_file_icon = models.ImageField(upload_to='file_icons/', null=True,blank=True)
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.cm_filename} - {self.cm_chepter}"
        
    class Meta:
        db_table = 'Chepterwise_Material'


class Batches(models.Model):
    batch_id = models.BigAutoField(primary_key=True)
    batch_name = models.CharField(max_length=50)
    batch_std = models.ForeignKey(Std,on_delete=models.CASCADE)
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.batch_name} - {self.batch_std.std_name} | {self.batch_std.std_board.brd_name}"
    
    class Meta:
        db_table = 'batches'


class Packs(models.Model):
    pack_id = models.BigAutoField(primary_key=True)
    pack_name = models.CharField(max_length=50)
    pack_std = models.ForeignKey(Std,on_delete=models.CASCADE)
    pack_subjects = models.ManyToManyField(Subject, blank=True, related_name='pack_subject')
    pack_fees = models.IntegerField()
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.pack_name} - {self.pack_std.std_name} | {self.pack_std.std_board.brd_name}"
    
    class Meta:
        db_table = 'packages'     

class Syllabus(models.Model):
    syllabus_id = models.BigAutoField(primary_key=True)
    syllabus_status = models.BooleanField(blank=True, null=True, default=0)
    syllabus_chapter = models.ForeignKey(Chepter, on_delete=models.CASCADE)
    syllabus_date = models.DateTimeField(auto_now_add=True)
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.syllabus_status} - {self.syllabus_chapter}"
    
    class Meta:
        db_table = 'Syllabus'
    
class Announcements(models.Model):
    announce_id = models.BigAutoField(primary_key=True)
    announce_title = models.CharField(max_length=100)
    announce_msg = models.TextField()
    announce_std = models.ForeignKey(Std,on_delete=models.CASCADE, blank=True,null=True)
    announce_batch = models.ForeignKey(Batches, on_delete=models.CASCADE,null=True, blank=True)
    announce_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    domain_name = models.CharField(blank=True,null=True,max_length=100)
    def __str__(self):
        return f"{self.announce_title}"
    
    class Meta:
        db_table = 'Announcement'


class Students(models.Model):
    class Gender(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'
        OTHER = 'Other', 'Other'
    stud_id = models.BigAutoField(primary_key=True)
    stud_name = models.CharField(max_length=200)
    stud_lastname = models.CharField(max_length=200)
    stud_contact = models.CharField(max_length=20)
    stud_username = models.CharField(max_length=40,null=True,blank=True)
    stud_email = models.EmailField(max_length=100)
    stud_dob = models.DateField()
    stud_gender = models.CharField(max_length=10,choices=Gender.choices,default=Gender.MALE)
    stud_nationality = models.CharField(null=True, blank=True, max_length=255, default='India')
    stud_profile = models.ImageField(blank=True, null=True, upload_to='uploads/',default='uploads/default_profile.jpg')
    stud_admission_no = models.IntegerField(blank=True, null=True)
    stud_roll_no = models.IntegerField(blank=True, null=True)
    stud_enrollment_no = models.IntegerField(blank=True, null=True)
    stud_guardian_name = models.CharField(max_length=200)
    stud_guardian_email = models.EmailField(max_length=200)
    stud_guardian_number = models.CharField(max_length=20)
    stud_guardian_profession = models.CharField(max_length=50,null=True,blank=True)
    stud_guardian_password = models.CharField(max_length=100, null=True, blank=True, default='123456')
    stud_guardian_otp = models.CharField(blank=True,null=True,max_length=10)
    guardian_onesignal_player_id = models.CharField(max_length=200, null=True, blank=True)
    stud_address = models.TextField(blank=True, null=True)
    stud_std = models.ForeignKey(Std, on_delete = models.CASCADE)
    stud_batch = models.ForeignKey(Batches, on_delete = models.CASCADE)
    stud_pack = models.ForeignKey(Packs, on_delete = models.CASCADE, related_name='packages')
    stud_pass = models.TextField(null=True, blank=True,default='12345678')
    stud_otp = models.CharField(blank=True,null=True,max_length=10)
    stud_telegram_studentchat_id = models.CharField(blank=True,null=True,max_length=20)
    stud_telegram_parentschat_id = models.CharField(blank=True,null=True,max_length=20)
    unique_code = models.CharField(max_length=20, editable=False, blank=True)
    domain_name = models.CharField(blank=True,null=True,max_length=100)
    stud_onesignal_player_id = models.TextField(max_length=200, null=True, blank=True)
    stud_lock = models.BooleanField(default=False)
    stud_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def generate_unique_code(self):
        """Generate a 20-digit random unique code."""
        while True:
            code = str(random.randint(10**19, 10**20 - 1))
            return code

    def __str__(self):
        return f"{self.stud_name} {self.stud_lastname}"
    
    class Meta:
        db_table = 'student'  

class Faculties(models.Model):
    fac_id = models.BigAutoField(primary_key=True)
    fac_name = models.CharField(max_length=100)
    fac_number = models.CharField(max_length=20)
    fac_email = models.EmailField(unique=True,default='abc@gmail.com')
    fac_address = models.TextField()
    fac_profile = models.ImageField(blank=True, null=True, upload_to='uploads/',default='uploads/default_profile.jpg')
    Subjects = models.CharField(max_length=100)
    fac_password = models.CharField(max_length=100,null=True, blank=True,default='12345678')
    fac_otp = models.IntegerField(blank=True,null=True)
    domain_name = models.CharField(blank=True,null=True,max_length=100)
    fac_onesignal_player_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.fac_name}"
    
    class Meta:
        db_table = 'faculty'


class Timetable(models.Model):
    class DaysChoice(models.TextChoices):
        SUNDAY = 'SUNDAY', 'Sunday'
        MONDAY = 'MONDAY', 'Monday'
        TUESDAY = 'TUESDAY', 'Tuesday'
        WEDNESDAY = 'WEDNESDAY', 'Wednesday'
        THURSDAY = 'THURSDAY', 'Thursday'
        FRIDAY = 'FRIDAY', 'Friday'
        SATURDAY = 'SATURDAY', 'Saturday'

    tt_id = models.BigAutoField(primary_key=True)
    tt_day = models.CharField(max_length=100, choices=DaysChoice.choices)
    tt_batch = models.ForeignKey('Batches', on_delete=models.CASCADE)
    tt_subject1 = models.ForeignKey('Subject', on_delete=models.CASCADE)
    tt_time1 = models.TimeField()
    tt_tutor1 = models.ForeignKey('Faculties', on_delete=models.CASCADE)
    domain_name = models.CharField(blank=True,null=True,max_length=100)
    
    def __str__(self):
        return f"{self.tt_batch} - {self.tt_day} | {self.tt_time1}"
    
    class Meta:
        db_table = 'timetable'
   
class Attendance(models.Model):
    atten_id = models.BigAutoField(primary_key=True)
    atten_student = models.ForeignKey(Students,on_delete=models.CASCADE)
    atten_timetable = models.ForeignKey(Timetable,on_delete=models.CASCADE)
    atten_date = models.DateTimeField(auto_now_add=True)
    atten_present = models.BooleanField(default=0)
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.atten_student} - {self.atten_timetable}"
    
    class Meta:
        db_table = 'attendence'

class Event(models.Model):
    event_id = models.BigAutoField(primary_key=True)
    event_name = models.CharField(max_length=500)
    event_date = models.DateField()
    event_desc = models.CharField(max_length=1000, null=True, blank=True)
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.event_name}"
    
    class Meta:
        db_table = 'event'

class Event_Image(models.Model):
    event_img_id = models.BigAutoField(primary_key=True)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    event_img = models.ImageField()
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.event_img}"
    
    class Meta:
        db_table = 'event_imgs'

class Chepterwise_test(models.Model):
    class sem_choices(models.TextChoices):
        sem1 = 'sem1', 'sem1'
        sem2 = 'sem2', 'sem2'

    test_id = models.BigAutoField(primary_key=True)
    test_name = models.CharField(max_length=100)
    test_std =  models.ForeignKey(Std, on_delete=models.CASCADE)
    test_sub = models.ForeignKey(Subject, on_delete=models.CASCADE,null=True,blank=True)
    test_sem = models.CharField(choices=sem_choices, max_length=50)
    test_time = models.CharField(null=True,blank=True,max_length=200)
    domain_name = models.CharField(blank=True,null=True,max_length=100)
    

    def __str__(self):
        return f"Name : {self.test_name}  Time : {self.test_time}"
    
    class Meta:
        db_table = 'chepterwise_test'

class Test_questions_answer(models.Model):
    class que_type(models.TextChoices):
        Question_Answer = 'Question_Answer', 'Question_Answer'
        MCQ = 'MCQ', 'MCQ'
        Filling_Blanks = 'Filling_Blanks','Filling_Blanks'
        True_False = 'True_False','True_False'
    tq_id = models.BigAutoField(primary_key=True)
    tq_name = models.ForeignKey(Chepterwise_test,on_delete=models.CASCADE)
    tq_chepter = models.ForeignKey(Chepter,on_delete=models.CASCADE)
    tq_q_type = models.CharField(choices=que_type.choices,max_length=50)
    tq_question = models.TextField(blank=True,null=True)
    tq_answer = models.TextField(blank=True,null=True)
    tq_weightage = models.IntegerField()
    tq_hint = models.TextField(blank=True,null=True)
    tq_optiona = models.CharField(max_length=200,blank=True,null=True)
    tq_optionb = models.CharField(max_length=200,blank=True,null=True)
    tq_optionc = models.CharField(max_length=200,blank=True,null=True)
    tq_optiond = models.CharField(max_length=200,blank=True,null=True)
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.tq_q_type} - {self.tq_name}"
    
    class Meta:
        db_table = 'test_questions_answer'


class Test_attempted_users(models.Model):
    tau_id = models.BigAutoField(primary_key=True)        
    tau_test_id = models.ForeignKey(Chepterwise_test,on_delete=models.CASCADE)
    tau_stud_id = models.ForeignKey(Students,on_delete=models.CASCADE)
    tau_completion_time = models.CharField(max_length=200)
    tau_attempted_questions = models.IntegerField()
    tau_correct_ans = models.IntegerField(null=True,blank=True)
    tau_total_marks = models.FloatField()
    tau_obtained_marks = models.FloatField(null=True,blank=True)
    tau_date = models.DateField(null=True, blank=True)
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.tau_test_id} - {self.tau_completion_time}"
    
    class Meta:
        db_table = 'test_attempted_users'


class Test_submission(models.Model):
    ts_id = models.BigAutoField(primary_key=True)
    ts_stud_id = models.ForeignKey(Students,on_delete=models.CASCADE)
    ts_que_id = models.ForeignKey(Test_questions_answer,on_delete=models.CASCADE)
    ts_ans = models.TextField()
    ts_attempted = models.BooleanField(default=0)
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.ts_que_id} - {self.ts_ans} {self.ts_stud_id}"
    
    class Meta:
        db_table = 'test_submission'



class Inquiries(models.Model):
    class Gender(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'
        OTHER = 'Other', 'Other'
    inq_id = models.BigAutoField(primary_key=True)
    inq_name = models.CharField(max_length=200)
    inq_lastname = models.CharField(max_length=200)
    inq_contact = models.CharField(max_length=20)
    inq_email = models.CharField(max_length=100)
    inq_dob = models.DateField()
    inq_gender = models.CharField(max_length=10,choices=Gender.choices,default=Gender.MALE)
    inq_guardian_name = models.CharField(max_length=200)
    inq_guardian_email = models.CharField(max_length=100)
    inq_guardian_number = models.CharField(max_length=20)
    inq_guardian_profession = models.CharField(max_length=50)
    inq_address = models.TextField()
    inq_std = models.ForeignKey(Std, on_delete = models.CASCADE)
    inq_schoolname = models.CharField(max_length=100)
    inq_last_std_and_marks = models.CharField(max_length=20)
    inq_howuknow = models.CharField(max_length=100)
    stud_nationality = models.CharField(null=True, blank=True, max_length=255, default='India')
    inq_subjects = models.CharField(max_length=300, null=True, blank=True)
    inq_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    domain_name = models.CharField(blank=True,null=True,max_length=100)
    def __str__(self):
        return f"{self.inq_name}"
    
    class Meta:
        db_table = 'inquiries'       



class Doubt_section(models.Model):
    doubt_id = models.BigAutoField(primary_key=True)
    doubt_stud_id = models.ForeignKey(Students, on_delete = models.CASCADE)
    doubt_doubt = models.TextField()
    doubt_subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    doubt_faculty = models.ForeignKey(Faculties, on_delete=models.CASCADE, null=True, blank=True)
    doubt_date = models.DateTimeField(auto_now_add=True)
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.doubt_stud_id.stud_name}"
    
    class Meta:
        db_table = 'Doubt_section'


class Doubt_solution(models.Model):
    solution_id = models.BigAutoField(primary_key=True)
    solution_stud_id = models.ForeignKey(Students, on_delete = models.CASCADE,null=True,blank=True)
    solution_teacher_id = models.CharField(max_length=200, null=True,blank=True)
    solution_doubt_id = models.ForeignKey(Doubt_section,on_delete=models.CASCADE)
    solution = models.TextField()
    solution_verified = models.BooleanField(default=0)
    solution_verified_by_teacher = models.ForeignKey(Faculties,on_delete=models.CASCADE,null=True,blank=True)
    solution_date = models.DateTimeField(auto_now_add=True)
    domain_name = models.CharField(blank=True,null=True,max_length=100)
    
    def __str__(self):
        return f"{self.solution_id} - {self.solution_doubt_id.doubt_id}"
    
    class Meta:
        db_table = 'Doubt_solution'

class Faculty_Access(models.Model):
    fa_id = models.BigAutoField(primary_key=True)
    fa_faculty = models.ForeignKey(Faculties, on_delete=models.CASCADE)
    fa_batch = models.ForeignKey(Batches, on_delete=models.CASCADE)
    fa_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.fa_batch.batch_std, self.fa_batch.batch_name, self.fa_subject.sub_name}"
    
    class Meta:
        db_table = 'Faculty_Access'

class Banks(models.Model):
    bank_id = models.BigAutoField(primary_key=True)
    bank_name = models.CharField(max_length=355)
    bank_code = models.CharField(max_length=155)
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.bank_name}"
    
    class Meta:
        db_table = 'Banks'

class Fees_Collection(models.Model):
    class mode_choices(models.TextChoices):
        UPI = 'UPI', 'UPI'
        CHECK = 'CHECK', 'CHECK'
        CASH = 'CASH', 'CASH'
        DEBIT = 'DEBIT', 'DEBIT'
        CREDIT = 'CREDIT', 'CREDIT'
    fees_id = models.BigAutoField(primary_key=True)
    fees_stud_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    fees_paid = models.IntegerField()
    fees_mode = models.CharField(choices=mode_choices, max_length=255)
    fees_date = models.DateTimeField(auto_now_add=True)
    domain_name = models.CharField(blank=True,null=True,max_length=100)
    
    def __str__(self):
        return f"{self.fees_stud_id.stud_name, self.fees_paid, self.fees_mode, self.fees_date}"
    
    class Meta:
        db_table = 'Fees_Collection'

class Cheque_Collection(models.Model):
    cheque_id = models.BigAutoField(primary_key=True)
    cheque_stud_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    cheque_amount = models.FloatField()
    cheque_number = models.IntegerField()
    cheque_bank = models.ForeignKey(Banks, on_delete=models.CASCADE, blank=True, null=True)
    cheque_bounce = models.BooleanField(default=False)
    cheque_date = models.DateField()
    cheque_expiry = models.DateField(blank=True, null=True)
    cheque_paid = models.BooleanField(default=False)
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def save(self, *args, **kwargs):
        if not self.cheque_expiry:
            self.cheque_expiry = self.cheque_date + timedelta(days=90)
        super(Cheque_Collection, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.cheque_stud_id.stud_name, self.cheque_paid}"
    
    class Meta:
        db_table = 'Cheque_Collection'

class Discount(models.Model):
    discount_id = models.BigAutoField(primary_key=True)
    discount_stud_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    discount_pack_id = models.ForeignKey(Packs, on_delete=models.CASCADE)
    discount_amount = models.IntegerField()
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.discount_stud_id.stud_name, self.discount_amount}"
    
    class Meta:
        db_table = 'Discount'


class Credits(models.Model):
    credit_id = models.BigAutoField(primary_key=True)
    credit_amount = models.IntegerField()
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.credit_id, self.credit_amount}"
    
    class Meta:
        db_table = 'Credits'

class Transactions(models.Model):
    transaction_id = models.BigAutoField(primary_key=True)
    transaction_amount = models.IntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_verified = models.BooleanField(default=False)
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.transaction_id, self.transaction_amount, self.transaction_date}"
    
    class Meta:
        db_table = 'Transactions'


class Today_Teaching(models.Model):
    today_teaching_id = models.BigAutoField(primary_key=True)
    today_teaching_chap_id = models.ForeignKey(Chepter, on_delete=models.CASCADE)
    today_teaching_batches_id = models.ForeignKey(Batches, on_delete=models.CASCADE, null=True, blank=True)
    today_teaching_fac_id = models.ForeignKey(Faculties, on_delete=models.CASCADE)
    today_teaching_desc = models.CharField(max_length=600)
    today_teaching_date = models.DateTimeField(auto_now_add=True)
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.today_teaching_id, self.today_teaching_chap_id, self.today_teaching_fac_id}"
    
    class Meta:
        db_table = 'Today_Teaching'



class question_bank(models.Model):
    class que_type(models.TextChoices):
        Question_Answer = 'Question_Answer', 'Question_Answer'
        MCQ = 'MCQ', 'MCQ'
        Filling_Blanks = 'Filling_Blanks','Filling_Blanks'
        True_False = 'True_False','True_False'
    qb_id = models.BigAutoField(primary_key=True)
    qb_chepter = models.CharField(max_length=200, null=True, blank=True)
    qb_subject = models.CharField(max_length=155, null=True, blank=True)
    qb_std =  models.CharField(max_length=55, null=True, blank=True)
    qb_q_type = models.CharField(choices=que_type.choices,max_length=50)
    qb_question = models.TextField(blank=True,null=True)
    qb_answer = models.TextField(blank=True,null=True)
    qb_weightage = models.IntegerField()
    qb_hint = models.TextField(blank=True,null=True)
    qb_optiona = models.CharField(max_length=200,blank=True,null=True)
    qb_optionb = models.CharField(max_length=200,blank=True,null=True)
    qb_optionc = models.CharField(max_length=200,blank=True,null=True)
    qb_optiond = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return f"{self.qb_q_type} - {self.qb_chepter}"
    
    class Meta:
        db_table = 'question_bank'



class mail_templates(models.Model):
    class mail_option(models.TextChoices):
        Itroduction_mail = 'Itroduction_mail','Itroduction_mail'
        Marketing_mail = 'Marketing_mail','Marketing_mail'

    mail_temp_id = models.BigAutoField(primary_key=True)
    mail_temp_html = models.TextField(blank=True, null=True)
    mail_temp_type = models.CharField(choices=mail_option.choices, max_length=50)
    mail_temp_selected = models.BooleanField(default=0)
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.mail_temp_html} - {self.mail_temp_type}" 

    class Meta:
        db_table = 'mail_templates'