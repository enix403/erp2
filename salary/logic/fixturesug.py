from __future__ import annotations
from typing import List
import datetime


from base import helpers


from ..models import (
    College,
    # TimeTable,
    TimeTableLecture,
    Staff,
    Fixture,
)
from .table.parsing import CellLectureInfo, ParsedTimeTable

from . import atnd_new as l_atnd
from . import roles
from .constants import StaffStatus, LectureType

from .lecture import calculate_given_load


class FixtureSuggestion:

    def __init__(self, college: College, section_id, ptable: ParsedTimeTable, cell_info: CellLectureInfo):
        self.college = college
        self.ptable = ptable
        self.target_cell = cell_info
        self.section_id = section_id

        # self._table_cells: List[TimeTableCell] = list(
        # table.cells.filter(active=1)
        # )

        self._sug_reason = None
        self._av_staff = []
        self._sug_staff = []

    def get_av_staff(self):
        return self._av_staff

    def get_sug_staff(self):
        return self._sug_staff

    def get_sug_reason(self):
        return self._sug_reason

    def is_empty_av(self):
        return len(self._av_staff) == 0

    def is_empty_sug(self):
        return len(self._sug_staff) == 0

    def process(self):
        av_staff = self.fixture_av_role_params()
        self._av_staff = av_staff
        sug_params, reason = self.fixture_sug_role_params(av_staff)
        self._sug_staff = sug_params
        self._sug_reason = reason

    # def v3(self, staffs):
        # return [], "COMP"

    def fixture_av_role_params(self):
        college_staff_all = list(
            self.college.staffs.filter(status=StaffStatus.ACTIVE)
                .select_related('main_roleparam_obj')
                .prefetch_related('fac_subjects__target_subject')
        )

        staffs = set()

        principle = helpers.get_first([s for s in college_staff_all if s.main_role == roles.ROLE_PRINCIPLE])
        if principle is not None:
            staffs.add(principle)

        conslr = helpers.get_first([s for s in college_staff_all if s.main_role == roles.ROLE_CONSELLER])
        if conslr is not None:
            staffs.add(conslr)

        busy_faculty_pk = set()

        for cell_info in self.ptable.parsed_cells[self.target_cell.cell.lecture_index].values():  # type: CellLectureInfo
            busy_faculty_pk.add(cell_info.faculty.pk)


        today_fixtures_staff_ids = set(
            Fixture.objects
            .filter(
                m_date=self.ptable.date,
                lecture_index=self.target_cell.lecture_index,
                college=self.college
            )
            .values_list('staff_id', flat=True)
        )


        for staff in college_staff_all:  # type: Staff
            if staff.main_role != roles.ROLE_FACULTY:
                continue

            if staff.pk in busy_faculty_pk:
                continue

            if staff.pk in today_fixtures_staff_ids:
                continue

            staffs.add(staff)

        am_manager = l_atnd.AttendanceManager(self.college, self.ptable.date)

        present = []
        for staff in staffs:

            info = am_manager.get_availability(staff, self.ptable.date)
            if info.available:
                # if True or l_atnd.check_avinfo_range(info, self.cell.lecture.time_start):
                present.append(staff)

        return present

    def _filter_underload(self, faculty_s):
        underload = []
        for faculty in faculty_s:  # type: Staff
            w_agreed = faculty.fetch_main_roleparam().w_agreed
            given_load = calculate_given_load(self.ptable, faculty.pk)
            if given_load < w_agreed:
                underload.append(faculty)

        return underload

    def _filter_class_t(self, faculty_s):
        res = []
        section_faculty_ids = set(
            self.ptable[i].get(self.section_id, CellLectureInfo()).faculty_id for i in range(self.ptable.num_lectures)
        )
        section_faculty_ids.discard(-1)

        for faculty in faculty_s:
            if faculty.pk in section_faculty_ids:
                res.append(faculty)

        return res

    def _filter_subject(self, faculty_s):
        res = []
        subject_pk = self.target_cell.subject.pk
        for faculty in faculty_s:
            for fac_sub in faculty.fac_subjects.all():  # type: FacSubject
                if fac_sub.target_subject_id == subject_pk:
                    res.append(faculty)
                    break
        return res

    def fixture_sug_role_params(self, staffs):

        sources = [
            (self._filter_class_t, "Class Teacher"),
            (self._filter_underload, "Underload"),
            (self._filter_subject, "Subject"),
        ]

        faculty_s = [s for s in staffs if s.main_role == roles.ROLE_FACULTY]

        last_index = len(sources) - 1

        next_faculty_s = faculty_s
        next_faculty_reason = sources[0][1]
        for i, (func, reason) in enumerate(sources):
            current = func(next_faculty_s)
            exists = len(current) == 1
            if exists or i == last_index:
                if exists:
                    return current, reason
                return next_faculty_s, next_faculty_reason
            if len(current) != 0:
                next_faculty_s = current
                next_faculty_reason = reason

        return [], ''


"""
from salary.logic import fixturesug as lf
from salary.logic.table.tablectrl import find_current_table
from salary.logic.table.parsing import TimeTableParser
import datetime

c = College.objects.first()
td = datetime.date.today()
t = find_current_table(c, td)
pt = TimeTableParser.parse_direct(t, td)


fg = lf.FixtureSuggestion(c, 2, pt, pt.parsed_cells[0][2])
fg.process()

print(fg._av_staff)

"""
