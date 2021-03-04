from __future__ import annotations
from django.views import View
from django.http import Http404
from django.shortcuts import render
from django.contrib import messages
from app.salary.typehints import HttpRequest

from app.base import utils
from app.salary.core.exceptions import UserLogicException
from app.salary.core.college import college_validate_simple

from app.salary.models import Section, College

from . import actions
from .permissions import SectionPermissions


class SectionsView(View):
    def get(self, req: HttpRequest, college_id):
        req.auth_manager.require_perm(
            SectionPermissions, "reg_sec:read", "meg_sec:read"
        )

        college: College = College.objects.filter(pk=college_id).first()
        if college == None:
            raise Http404

        college_validate_simple(req, college.pk)

        active_sections = list(
            college.sections.filter(active=1).prefetch_related("merge_section_rows")
        )

        regular_sections = []
        merged_sections = []

        for s in active_sections:
            if s.m_type == actions.SectionType.REGULAR:
                regular_sections.append(s)
            elif s.m_type == actions.SectionType.MERGED:
                merged_sections.append(s)

        m_sections_formatted = list()
        for s in merged_sections:  # type: Section

            children_names = [
                g.name
                for r in s.merge_section_rows.all()
                for g in active_sections
                if g.pk == r.target_section_id
            ]
            children = " + ".join(children_names)

            m_sections_formatted.append((s.name, children))

        return render(
            req,
            "sl/sections.html",
            {
                "college": college,
                "regular_sections": regular_sections,
                "merged_sections_formatted": m_sections_formatted,
            },
        )


class ValidateSectionCreationMixin(object):
    def _validate_section(self, bag):
        name = bag.get("name")
        if not name:
            raise UserLogicException("Invalid name")

        college = College.objects.filter(pk=utils.to_int(bag.get("college_id"))).first()
        if college is None:
            raise UserLogicException("College not found")

        if Section.objects.filter(name=name, college=college).exists():
            raise UserLogicException("Section " + str(name) + " already exists")

        return name, college


class Action_CreateRegularSection(View, ValidateSectionCreationMixin):
    def _clean_input(self, bag):
        return self._validate_section(bag)

    def post(self, req: HttpRequest):
        req.auth_manager.require_perm(SectionPermissions, "reg_sec:create")

        name, college = self._clean_input(req.POST)
        college_validate_simple(req, college.pk)
        actions.make_regular_section(college.pk, name)

        messages.success(req, "Section added successfully")
        return utils.redirect_back(req)


class Action_CreateMergedSection(View, ValidateSectionCreationMixin):
    def _clean_input(self, bag):
        name, college = self._validate_section(bag)  # type: str, College
        section_id_list = list(map(utils.to_int, bag.getlist('section_id')))

        if len(section_id_list) < 2:
            raise UserLogicException("Select atleast two sections")

        children = list(Section.objects.filter(pk__in=section_id_list))

        if len(children) != len(section_id_list):
            # Atleast one of the given sections was not found
            raise UserLogicException("Cannot find section(s)")

        for child in children: # type: Section
            if child.college_id != college.pk:
                raise UserLogicException("Invalid sections")

        return name, college, children

    def post(self, req):
        req.auth_manager.require_perm(SectionPermissions, "meg_sec:create")
        bag = utils.get_bag(req)
        name, college, children = self._clean_input(bag)

        actions.make_merged_section(college.pk, name, children)

        messages.success(req, 'Sections merged successfully')
        return utils.redirect_back(req)
