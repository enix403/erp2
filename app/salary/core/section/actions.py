from app.salary.models import Section, MergeSectionRow

class SectionType:
    REGULAR = 0
    MERGED = 1


def create_section(college_id, name, stype, active=1):
    section = Section()
    section.name = name
    section.m_type = stype
    section.active = active
    section.college_id = college_id

    return section


def make_regular_section(college_id, name):
    section = create_section(college_id, name, SectionType.REGULAR)
    section.save()
    return section


def make_merged_section(college_id, name, children: list):
    parent_section: Section = create_section(college_id, name, SectionType.MERGED)
    parent_section.save()

    merge_rows_bulk = []

    for child in children:  # type: Section
        row = MergeSectionRow()
        row.parent_section = parent_section
        row.target_section = child

        merge_rows_bulk.append(row)

    MergeSectionRow.objects.bulk_create(merge_rows_bulk)

    return parent_section