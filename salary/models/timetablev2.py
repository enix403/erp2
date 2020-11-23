from django.db import models
from .core import RelatableModel, College, Subject
from .staff import Person
from .sectioning import Section


from .auth import AppUser

from ..logic.constants import Gender, FacultyCategory
from ..logic import roles


class Staff_v2(models.Model, RelatableModel):
    relation_name = 'staff_v2_id'

    class Meta:
        db_table = 'sl_staffs_v2'

    person = Person.get_key()
    college = College.get_key(r_name='staffs_v2')
    status = models.PositiveSmallIntegerField(db_column="status")

    transfer_from = models.PositiveIntegerField(db_column='transfer_from_sid', null=True, blank=True)
    transfer_date = models.DateField()

    main_role = models.SmallIntegerField(db_column='main_role')

    role_params: models.Manager
    fac_subjects: models.Manager

    def format_subject_name(self):
        if self.main_role != roles.ROLE_FACULTY:
            return ' - '

        main_subject = self.fac_subjects.filter(main=1).prefetch_related("target_subject").first()
        if main_subject != None:
            return main_subject.target_subject.name

        return '-ERROR-'


class RoleParam_v2(models.Model, RelatableModel):
    relation_name = 'rp_id'

    class Meta:
        db_table = 'sl_role_params_v2'

    staff = Staff_v2.get_key(r_name='role_params')

    w_agreed = models.SmallIntegerField(db_column='w_agreed')
    x_rate = models.SmallIntegerField(db_column='x_rate')
    category = models.SmallIntegerField(db_column='category')
    salary = models.IntegerField(db_column='salary')

    role = models.SmallIntegerField(db_column='role')

    prev_role_param = models.OneToOneField(
        'self',
        db_column='prev_rp_id',
        db_constraint=False,
        related_name="+",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )

    main = models.PositiveSmallIntegerField(db_column='main')
    active = models.PositiveSmallIntegerField(db_column='active')

    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True)

    def user_acc_exists(self):
        return AppUser.objects.filter(role_param_id=self.pk).exists()

    def format_role_name(self):
        # return 'Role_Name'
        role = roles.role_from_id(self.role)
        if role != None:
            return role.name

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


class FacSubject_v2(models.Model, RelatableModel):
    relation_name = 'fac_subject_id'

    class Meta:
        db_table = "sl_fac_subjects_v2"

    staff = Staff_v2.get_key(r_name='fac_subjects')
    target_subject = Subject.get_key('target_subject_id')
    main = models.IntegerField(db_column='main')


class TimeTable_v2(models.Model, RelatableModel):

    relation_name = 'tbl_id'

    class Meta:
        db_table = 'sl_tbls'

    college = College.get_key()

    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)

    main = models.PositiveSmallIntegerField()


class TimeTableCell_v2(models.Model, RelatableModel):

    relation_name = 'tbl_cell_id'

    class Meta:
        db_table = 'sl_tbl_cells'

    table = TimeTable_v2.get_key()

    lecture_index = models.PositiveSmallIntegerField()
    section = Section.get_key()

    active = models.PositiveSmallIntegerField()

    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True)


class TimeTableCellFragment(models.Model, RelatableModel):
    relation_name = 'tbl_cellfrag_id'

    class Meta:
        db_table = 'sl_tbl_cellfrags'

    cell = TimeTableCell_v2.get_key()

    staff = Staff_v2.get_key()
    subject = Subject.get_key()

    rep_policy = models.CharField(max_length=20)
