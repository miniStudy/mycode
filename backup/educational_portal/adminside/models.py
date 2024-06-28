from django.db import models

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
    sub_name = models.CharField(max_length=50)
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
    cm_file_icon = models.ImageField(upload_to='file_icons/', null=True, blank=True)

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



