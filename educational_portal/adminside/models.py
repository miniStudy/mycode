from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class AdminData(models.Model):
    admin_id = models.BigAutoField(primary_key=True)
    admin_name = models.CharField(max_length=20)
    admin_pass = models.CharField(max_length=100)
    admin_email = models.EmailField(unique=True)
    admin_otp = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return f"{self.admin_email}"
    
    class Meta:
        db_table = 'AdminData'


class Boards(models.Model):
    brd_id = models.BigAutoField(primary_key=True)
    brd_name = models.CharField(max_length=20,unique=True)
    
    def __str__(self):
        return f"{self.brd_name}"
    
    class Meta:
        db_table = 'Boards'

class Std(models.Model):
    std_id = models.BigAutoField(primary_key=True)
    std_name = models.CharField(max_length=10)
    std_board = models.ForeignKey(Boards, on_delete=models.CASCADE)    

    def __str__(self):
        return f"{self.std_name} - {self.std_board}"
    
    class Meta:
        db_table = 'std'



class Subject(models.Model):
    sub_id = models.BigAutoField(primary_key=True)
    sub_name = models.CharField(max_length=50,unique=True)
    sub_std = models.ForeignKey(Std, on_delete=models.CASCADE)    

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

    def _str_(self):
        return f"{self.chep_name} - {self.chep_sem} {self.chep_std}"
    
    class Meta:
        db_table = 'chepter'

class Chepterwise_material(models.Model):
    cm_id = models.BigAutoField(primary_key=True)
    cm_chepter = models.ForeignKey(Chepter,on_delete=models.CASCADE)
    cm_filename = models.CharField(max_length=100)
    cm_file = models.FileField(upload_to ='uploads/')
    cm_file_icon = models.ImageField(upload_to='file_icons/', null=True,blank=True)

    def _str_(self):
        return f"{self.cm_filename} - {self.cm_chepter}"
        
    class Meta:
        db_table = 'Chepterwise_Material'


class Batches(models.Model):
    batch_id = models.BigAutoField(primary_key=True)
    batch_name = models.CharField(max_length=50)
    batch_std = models.ForeignKey(Std,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.batch_name} - {self.batch_std.std_name} | {self.batch_std.std_board.brd_name}"
    
    class Meta:
        db_table = 'batches'


class Packs(models.Model):
    pack_id = models.BigAutoField(primary_key=True)
    pack_name = models.CharField(max_length=50)
    pack_std = models.ForeignKey(Std,on_delete=models.CASCADE)
    pack_subjects = models.ManyToManyField(Subject, blank=True)
    pack_fees = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.pack_name} - {self.pack_std.std_name} | {self.pack_std.std_board.brd_name}"
    
    class Meta:
        db_table = 'packages'     

    
class Announcements(models.Model):
    announce_id = models.BigAutoField(primary_key=True)
    announce_title = models.CharField(max_length=100)
    announce_msg = models.TextField()
    announce_std = models.ForeignKey(Std,on_delete=models.CASCADE, blank=True,null=True)
    announce_batch = models.ForeignKey(Batches, on_delete=models.CASCADE,null=True, blank=True)
    announce_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
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
    stud_username = models.CharField(max_length=40)
    stud_email = models.EmailField(max_length=100)
    stud_dob = models.DateField()
    stud_gender = models.CharField(max_length=10,choices=Gender.choices,default=Gender.MALE)
    stud_guardian_name = models.CharField(max_length=200)
    stud_guardian_email = models.EmailField(max_length=200)
    stud_guardian_number = models.CharField(max_length=20)
    stud_guardian_profession = models.CharField(max_length=50)
    stud_address = models.TextField()
    stud_std = models.ForeignKey(Std, on_delete = models.CASCADE)
    stud_batch = models.ForeignKey(Batches, on_delete = models.CASCADE)
    stud_pack = models.ForeignKey(Packs, on_delete = models.CASCADE)
    stud_pass = models.TextField(blank=True,null=True)
    stud_otp = models.CharField(blank=True,null=True,max_length=10)

    def __str__(self):
        return f"{self.stud_name} {self.stud_lastname}"
    
    class Meta:
        db_table = 'student'  

class Faculties(models.Model):
    fac_id = models.BigAutoField(primary_key=True)
    fac_name = models.CharField(max_length=100)
    fac_number = models.CharField(max_length=20)
    fac_email = models.CharField(max_length=100)
    fac_address = models.TextField()
    Subjects = models.CharField(max_length=100)
    
    def _str_(self):
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
    
    def _str_(self):
        return f"{self.tt_batch} - {self.tt_day} | {self.tt_time1}"
    
    class Meta:
        db_table = 'timetable'
   
class Attendance(models.Model):
    atten_id = models.BigAutoField(primary_key=True)
    atten_student = models.ForeignKey(Students,on_delete=models.CASCADE)
    atten_timetable = models.ForeignKey(Timetable,on_delete=models.CASCADE)
    atten_date = models.DateTimeField(auto_now_add=True)
    atten_present = models.BooleanField(default=0)

    def _str_(self):
        return f"{self.atten_student} - {self.atten_timetable}"
    
    class Meta:
        db_table = 'attendence'

class Event(models.Model):
    event_id = models.BigAutoField(primary_key=True)
    event_name = models.CharField(max_length=500)
    event_date = models.DateField()
    event_img = models.ImageField(upload_to='uploads/events',null=True,blank=True)
    event_desc = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.event_name}"
    
    class Meta:
        db_table = 'event'



class Chepterwise_test(models.Model):
    class sem_choices(models.TextChoices):
        sem1 = 'sem1', 'sem1'
        sem2 = 'sem2', 'sem2'

    test_id = models.BigAutoField(primary_key=True)
    test_name = models.CharField(max_length=100)
    test_std =  models.ForeignKey(Std, on_delete=models.CASCADE)
    test_sub = models.ForeignKey(Subject, on_delete=models.CASCADE,null=True,blank=True)
    test_sem = models.CharField(choices=sem_choices, max_length=50)
    test_time = models.TimeField(null=True,blank=True)

    def _str_(self):
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
    tq_question = RichTextUploadingField(blank=True,null=True)
    tq_answer = RichTextUploadingField(blank=True,null=True)
    tq_weightage = models.IntegerField()
    tq_hint = models.TextField(blank=True,null=True)
    tq_optiona = models.CharField(max_length=200,blank=True,null=True)
    tq_optionb = models.CharField(max_length=200,blank=True,null=True)
    tq_optionc = models.CharField(max_length=200,blank=True,null=True)
    tq_optiond = models.CharField(max_length=200,blank=True,null=True)

    def _str_(self):
        return f"{self.tq_question} - {self.tq_q_type} - {self.tq_name}"
    
    class Meta:
        db_table = 'test_questions_answer'


class Test_attempted_users(models.Model):
    tau_id = models.BigAutoField(primary_key=True)        
    tau_test_id = models.ForeignKey(Chepterwise_test,on_delete=models.CASCADE)
    tau_stud_id = models.ForeignKey(Students,on_delete=models.CASCADE)
    tau_completion_time = models.TimeField()
    tau_attempted_questions = models.IntegerField()
    tau_correct_ans = models.IntegerField()
    tau_total_marks = models.FloatField()
    tau_obtained_marks = models.FloatField()

    def _str_(self):
        return f"{self.tau_test_id} - {self.tau_completion_time}"
    
    class Meta:
        db_table = 'test_attempted_users'


class Test_submission(models.Model):
    ts_id = models.BigAutoField(primary_key=True)
    ts_stud_id = models.ForeignKey(Students,on_delete=models.CASCADE)
    ts_que_id = models.ForeignKey(Test_questions_answer,on_delete=models.CASCADE)
    ts_ans = models.TextField()
    ts_attempted = models.BooleanField(default=0)

    def _str_(self):
        return f"{self.ts_que_id} - {self.ts_ans} {self.ts_stud_id}"
    
    class Meta:
        db_table = 'test_submission'

