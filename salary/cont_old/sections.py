from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.http import Http404



from ..logic import college as l_college
from ..logic.constants import SectionType

from ..models import (
    College,
    Section
)

from base import helpers
from .execptions import DisplayToUserException

from ..auth.validation import validate_college


class SectionsView(View):
    def get(self, req, college_id):
        college: College = helpers.fetch_model_clean(College, college_id)
        if college == None:
            raise Http404
        
        validate_college(college)

        active_sections = list(
            college.sections
            .filter(active=1)
            # .prefetch_related('merge_section_rows', 'merge_section_rows__target_section')
            .prefetch_related('merge_section_rows')
        )

        regular_sections = []
        merged_sections = []
        
        for s in active_sections:
            if s.m_type == SectionType.REGULAR:
                regular_sections.append(s)
            elif s.m_type == SectionType.MERGED:
                merged_sections.append(s)
                        

        m_sections_formatted = list()
        for s in merged_sections:  # type: Section

            children_names = [g.name for r in s.merge_section_rows.all() for g in active_sections if g.pk == r.target_section_id]
            children = " + ".join(children_names)

            m_sections_formatted.append((s.name, children))

        return render(req, "sl/pages/sections.html", {
            "college": college,
            'regular_sections': regular_sections,
            'merged_sections_formatted': m_sections_formatted,
        })
        


class ValidateSectionCreationMixin(object):
    def _validate_section(self, bag):
        name = bag.get('name')
        if not name:
            raise DisplayToUserException("Invalid name")

        college = helpers.fetch_model_clean(College, bag.get('college_id'))
        if college == None:
            raise DisplayToUserException("College not found")
        
        validate_college(college)

        if Section.objects.filter(name=name).count() > 0:
            raise DisplayToUserException("Section " + str(name) + " already exists")

        return name, college


class Action_CreateRegularSection(View, ValidateSectionCreationMixin):

    def _clean_input(self, bag):  # type: QueryDict
        return self._validate_section(bag)

    def post(self, req):
        bag = helpers.get_bag(req)
        name, college = self._clean_input(bag)

        college_impl = l_college.Impl_College(college)
        college_impl.add_regular_section(name)

        messages.success(req, "Section added successfully")
        return helpers.redirect_back(req)


class Action_CreateMergedSection(View, ValidateSectionCreationMixin):
    def _clean_input(self, bag):  # type: QueryDict
        college: College
        name, college = self._validate_section(bag)  # type: str, College
        section_id_list = list(map(helpers.to_int, bag.getlist('section_id')))

        if len(section_id_list) < 2:
            raise DisplayToUserException("Select atleast two sections")

        children = list(Section.objects.filter(pk__in=section_id_list).prefetch_related('college'))
        for child in children:
            if child.college.pk != college.pk:
                raise DisplayToUserException("Invalid sections")

        return name, college, children

    def post(self, req):
        bag = helpers.get_bag(req)
        name, college, children = self._clean_input(bag)

        college_impl = l_college.Impl_College(college)
        college_impl.add_merged_section(name, children)

        messages.success(req, 'Sections merged successfully')
        return helpers.redirect_back(req)
