from django.db import models
from .core import RelatableModel, College, Subject
from .auth import AppUser
from . import fields

from app.salary.core.staff import FacultyCategory, Gender, roles


class Person(models.Model, RelatableModel):
    relation_name = "person_id"

    class Meta:
        db_table = "sl_persons"

    name = models.CharField(max_length=100, db_column='name')
    cnic = models.CharField(max_length=20, db_column='cnic')
    bank_acc = models.CharField(max_length=100, db_column='bank_acc')

    gender = fields.PositiveTinyInt(db_column='gender')

    # The unique ID Number assigned to this person by the organization
    comp_number = models.IntegerField(db_column='comp_number')

    # The date this person joined the organization
    init_date = models.DateField(db_column='init_date')

    # def format_gender_name(self):
        # if self.gender == Gender.MALE:
            # return 'Male'
        # elif self.gender == Gender.FEMALE:
            # return 'Female'

        # return '--ERROR--'


class Staff(models.Model, RelatableModel):
    relation_name = 'staff_id'

    class Meta:
        db_table = 'sl_staffs'

    person = Person.get_key()

    # Denormalizing self.person.name for quick access
    # because it is needed most of the time
    name = models.CharField(max_length=100, db_column='name')

    college = College.get_key(r_name='staffs')

    # Active, Inactive or being transfered
    status = fields.PositiveTinyInt(db_column="status")

    # ID of the previous staff obj the person was transferred from, or null (0)
    transfer_from_sid = models.PositiveIntegerField(db_column='transfer_from_sid', default=0)

    # The date this staff obj was created (not necessarily activated at this date)
    transfer_date = models.DateField()

    # The date this staff obj activates (not the date this staff obj was created)
    activate_date = models.DateField()

    # Shortcut to main_roleparam_obj.role for quick access
    main_role = fields.PositiveTinyInt(db_column='main_role')

    # Does this person has a faculty role among its roles
    has_faculty = fields.PositiveTinyInt(db_column='has_faculty')
    
    main_roleparam_obj = models.OneToOneField(
        'salary.RoleParam',
        db_column='main_roleparam_id',
        db_constraint=False,
        related_name="+",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )

    role_params: models.Manager
    fac_subjects: models.Manager

    # def format_subject_name(self):
    #     if self.main_role != roles.ROLE_FACULTY:
    #         return ' - '

    #     # main_subject = self.fac_subjects.filter(main=1).prefetch_related("target_subject").first()
        
    #     mains_lst = [fs for fs in self.fac_subjects.all() if fs.main == 1]
        
    #     if len(mains_lst) > 0:
    #         main_subject = mains_lst[0] 
    #         return main_subject.target_subject.name

    #     return '-ERROR-'
    
    # def fetch_main_roleparam(self):
    #     if self.main_roleparam_obj is not None:
    #         return self.main_roleparam_obj
        
    #     return self.role_params.filter(active=1, main=1)
    
    # @property
    # def role_suffix(self):
        # return 'F' if self.main_role == roles.ROLE_FACULTY else 'A'
    

class RoleParam(models.Model, RelatableModel):
    relation_name = 'rp_id'

    class Meta:
        db_table = 'sl_role_params'

    staff = Staff.get_key(r_name='role_params')

    w_agreed = fields.PositiveTinyInt(db_column='w_agreed')  # Agreed workload (Faculty only)
    x_rate = models.SmallIntegerField(db_column='x_rate')  # Extra Lecture Rate (Faculty only)
    category = fields.PositiveTinyInt(db_column='category')  # Faculty category (Faculty only)
    salary = models.IntegerField(db_column='salary')

    role = fields.PositiveTinyInt(db_column='role')  # Staff role (Principal, Faculty, Vice Principal... etc)

    # ID of the previous RoleParam (like a linked list)
    prev_role_param = models.OneToOneField(
        'self',
        db_column='prev_rp_id',
        db_constraint=False,
        related_name="+",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )

    # Boolean to indicate if this RoleParam is the main RoleParam of the parent Staff
    main = fields.PositiveTinyInt(db_column='main')

    active = fields.PositiveTinyInt(db_column='active')  # bool

    # Start and end dates of this RoleParam effect period (Both inclusive)
    date_start = models.DateField()
    date_end = models.DateField(default="9999-12-31")
    
    # TODO: move this to utils and make proper context for staff.html template

    # def user_acc_exists(self):
    #     return AppUser.objects.filter(role_param_id=self.pk).exists()

    # def format_role_name(self):
    #     # return 'Role_Name'
    #     role = roles.role_from_id(self.role)
    #     if role != None:
    #         return role.name

    #     return '-ERROR-'

    # def format_category_name(self):
    #     if not self.is_faculty():
    #         return ' - '

    #     if self.category == FacultyCategory.FAC_CATERGORY_M:
    #         return 'Morning'
    #     if self.category == FacultyCategory.FAC_CATERGORY_M_AND_E:
    #         return 'Morning & Evening'
    #     if self.category == FacultyCategory.FAC_CATERGORY_M_PLUS_E:
    #         return 'Morning + Evening'
    #     if self.category == FacultyCategory.FAC_CATERGORY_V:
    #         return 'Visiting'

    #     return '-ERROR-'

    # def format_agreed_workload(self):
    #     if self.is_faculty():
    #         return self.w_agreed

    #     return ' - '

    # def format_x_rate(self):
    #     if self.is_faculty():
    #         return '{:,}'.format(self.x_rate)

    #     return ' - '

    # def format_salary(self):
    #     return '{:,}'.format(self.salary)

    # def is_faculty(self):
    #     return self.role == roles.ROLE_FACULTY


class FacSubject(models.Model, RelatableModel):
    relation_name = 'fac_subject_id'

    class Meta:
        db_table = "sl_fac_subjects"

    staff = Staff.get_key(r_name='fac_subjects')
    target_subject = Subject.get_key('target_subject_id')
    main = fields.PositiveTinyInt(db_column='main')
