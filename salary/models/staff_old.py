from django.db import models
from .core import RelatableModel, College, Subject
from .auth import AppUser

from ..logic.constants import Gender, FacultyCategory
from ..logic import roles

class Person(models.Model, RelatableModel):
    relation_name = "person_id"

    class Meta:
        db_table = "sl_persons"

    name = models.CharField(max_length=100, db_column='name')
    cnic = models.CharField(max_length=100, db_column='cnic')
    bank_acc = models.CharField(max_length=100, db_column='bank_acc')

    gender = models.SmallIntegerField(db_column='gender')
    erp_number = models.IntegerField(db_column='erp_number')
    
    def format_gender_name(self):
        if self.gender == Gender.MALE:
            return 'Male'
        elif self.gender == Gender.FEMALE:
            return 'Female'
        
        return '--ERROR--'

    j_date_kips = models.DateField("j_date_kips")


class Staff(models.Model, RelatableModel):
    relation_name = "staff_id"

    class Meta:
        db_table = "sl_staffs"

    person = Person.get_key()
    college = College.get_key(r_name='staffs')
    
    transfer_from = models.PositiveIntegerField(db_column='transfer_from_sid', null=True, blank=True)
    status = models.PositiveSmallIntegerField(db_column="status")
    
    role_params: models.Manager


class RoleParam(models.Model, RelatableModel):
    relation_name = "role_param_id"

    class Meta:
        db_table = "sl_role_params"

    staff = Staff.get_key("staff_id", 'role_params')
    college = College.get_key(r_name='role_params')
    
    # shortcut to staff.person.name
    # it is needed most of the time so it is duplicated it here
    name = models.CharField(max_length=100, db_column='name') 
    
    
    role = models.SmallIntegerField(db_column='role')
    w_agreed = models.SmallIntegerField(db_column='w_agreed')
    x_rate = models.SmallIntegerField(db_column='x_rate')
    category = models.SmallIntegerField(db_column='category')
    salary = models.IntegerField(db_column='salary')

    active = models.PositiveSmallIntegerField(db_column='active')
    main = models.PositiveSmallIntegerField(db_column='main')
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)

    j_date_campus = models.DateField()
    
    fac_subjects: models.Manager
    
    def user_acc_exists(self):
        return AppUser.objects.filter(role_param_id=self.pk).exists()
    
    def format_role_name(self):
        # return 'Role_Name'
        role = roles.role_from_id(self.role)
        if role != None:
            return role.name
        
        return '-ERROR-'
    
    def format_subject_name(self):
        if not self.is_faculty():
            return ' - '
        
        main_subject = self.fac_subjects.filter(main=1).prefetch_related("target_subject").first()
        if main_subject != None:
            return main_subject.target_subject.name
        
        return '-ERROR-'
    
    def format_category_name(self):
        if not self.is_faculty():
            return ' - '
        
        if self.category == FacultyCategory.FAC_CATERGORY_M:
            return 'Morning'
        if self.category == FacultyCategory.FAC_CATERGORY_M_AND_E:
            return 'Morning & Evening'
        if self.category == FacultyCategory.FAC_CATERGORY_M_PLUS_E:
            return 'Morning + Evening'
        if self.category == FacultyCategory.FAC_CATERGORY_V:
            return 'Visiting'
        
        return '-ERROR-'

    
    def format_agreed_workload(self):
        if self.is_faculty():
            return self.w_agreed
        
        return ' - '
    
    def format_x_rate(self):
        if self.is_faculty():
            return '{:,}'.format(self.x_rate)

        return ' - '
    
    def format_salary(self):
        return '{:,}'.format(self.salary)
    
    def is_faculty(self):
        return self.role == roles.ROLE_FACULTY
        
    
class FacSubject(models.Model, RelatableModel):
    relation_name = 'fac_subject_id'

    class Meta:
        db_table = "sl_fac_subjects"

    faculty_param = RoleParam.get_key('faculty_param_id', 'fac_subjects')
    target_subject = Subject.get_key('target_subject_id')
    main = models.IntegerField(db_column='main')
