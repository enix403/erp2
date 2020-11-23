from __future__ import annotations
from typing import Optional, List

from ...models import (
    College,
    TimeTable,
    Section,
    TimeTableLecture,
    TimeTableCell
)
import base.helpers as helpers


class Dl_TableCell:
    pk: int
    subject_name: str
    faculty_name: str


class Dl_SectionRow:
    section_name: str
    cells: List[Optional[Dl_TableCell]]


class Dl_TimeTableInfo:
    weekday_num: int
    day_name: str
    table: Optional[TimeTable]
    is_current: bool

    lectures_sorted: Optional[List[TimeTableLecture]] = None
    section_rows: Optional[List[Dl_SectionRow]] = None


def get_day_name(day):
    return {
        0: 'Sunday',
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday'
    }.get(day, "ERROR")


def gen_section_row(table_cells: List[TimeTableCell], section: Section, lectures_sorted: List[TimeTableLecture]):
    cells_db = []

    # cells count (after getting filtered by the loop below) cannot be greater than lectures count
    # so if we have found at least len(lectures_sorted) cells, we can just break out of the loop
    lecture_count = len(lectures_sorted)
    cells_found = 0
    for c in table_cells:

        if cells_found >= lecture_count:
            break

        if c.section_id == section.pk:
            cells_db.append(c)
            cells_found += 1

    if len(cells_db) == 0:
        return None

    cells_db.sort(key=lambda c: c.lecture_index)

    section_row = Dl_SectionRow()
    section_row.section_name = section.name

    current_lecture_index = 0
    # the reason current_lecture_index and current_lecture.lecture_index are different is because the latter does not neccesarily
    # start at zero (bad naming i guess)

    dl_cells = []
    for c in cells_db:  # type: TimeTableCell
        current_lecture = lectures_sorted[current_lecture_index]

        while c.lecture_index != current_lecture.lecture_index:
            dl_cells.append(None)
            current_lecture_index += 1
            current_lecture = lectures_sorted[current_lecture_index]

        current_lecture_index += 1

        dl_cell = Dl_TableCell()
        dl_cell.pk = c.pk
        dl_cell.subject_name = c.subject.name
        dl_cell.faculty_name = c.faculty_param.name

        dl_cells.append(dl_cell)

    # fill up the remaining space with None
    total_cells_count = len(dl_cells)
    for _ in range(lecture_count - total_cells_count):
        dl_cells.append(None)

    section_row.cells = dl_cells

    return section_row


def get_table_section_rows(sections: List[Section], table_cells: List[TimeTableCell], lectures_sorted: List[TimeTableLecture]):
    rows = []
    for section in sections:
        section_row = gen_section_row(table_cells, section, lectures_sorted)
        if section_row == None:
            continue
        rows.append(section_row)

    return rows


def make_table_info_list(college: College, active_sections=None) -> List[Dl_TimeTableInfo]:
    table_list = []

    if active_sections is None:
        sections = [s for s in list(college.sections.all()) if s.active == 1]
    else:
        sections = active_sections

    college_active_tables = list(college.time_tables.filter(active=1)
                                 .prefetch_related('lectures', 'cells', 'cells__subject', 'cells__faculty_param'))
    # .prefetch_related('lectures', 'cells', 'cells__subject', 'cells__faculty_param', 'cells__section'))

    for i in range(1, 7):
        info = Dl_TimeTableInfo()
        info.weekday_num = i
        info.day_name = get_day_name(i)

        table: TimeTable = helpers.get_first([t for t in college_active_tables if t.week_day == info.weekday_num])
        info.table = table

        if table != None:
            info.lectures_sorted = list(sorted(list(table.lectures.all()), key=lambda l: l.lecture_index))

            table_cells = list(table.cells.filter(active=1))

            info.section_rows = get_table_section_rows(sections, table_cells, info.lectures_sorted)

        table_list.append(info)
    return table_list
