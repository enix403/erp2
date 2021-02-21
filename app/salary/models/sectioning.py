from django.db import models
from .core import RelatableModel, College


class Section(models.Model, RelatableModel):
    relation_name = "section_id"

    class Meta:
        db_table = "sl_sections"

    name = models.CharField(max_length=15, db_column='name')
    college = College.get_key('college_id', 'sections')
    m_type = models.SmallIntegerField(db_column='m_type')
    active = models.SmallIntegerField(db_column='active')
    
    merge_section_rows: models.Manager


class MergeSectionRow(models.Model, RelatableModel):
    relation_name = "merge_section_row_id"

    class Meta:
        db_table = "sl_merge_section_rows"

    parent_section = Section.get_key("parent_section_id", 'merge_section_rows')
    target_section = Section.get_key("target_section_id")
