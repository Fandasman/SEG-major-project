"""Unit tests of the club creation form."""
from django import forms
from django.test import TestCase
from clubs.forms import ClubForm
from clubs.models import Club
import datetime

#This code was taken from the clucker application

class ClubCreationFormTestCase(TestCase):
    """Unit tests of the Club Creation form."""
    def setUp(self):
        self.form_input = {'name': 'KCL book club', 'location': '30 Aldwych, London WC2B 4BG', 'description': 'Book Club for KCL informatics students.'}

    def test_form_contains_required_fields(self):
        form = ClubForm()
        self.assertIn('name', form.fields)
        self.assertIn('location', form.fields)
        self.assertIn('description', form.fields)

    def test_form_accepts_valid_input(self):
        form = ClubForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_name(self):
        self.form_input['name'] = ''
        form = ClubForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_description(self):
        self.form_input['description'] = ''
        form = ClubForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_location(self):
        self.form_input['location'] = ''
        form = ClubForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = ClubForm(data=self.form_input)
        before_count = Club.objects.count()
        self.club = form.save()
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count+1)
        this_club = Club.objects.get(name = self.club.name)
        self.assertEqual(this_club.name,'KCL book club')
        self.assertEqual(this_club.description,'Book Club for KCL informatics students.')
        self.assertEqual(this_club.location,'30 Aldwych, London WC2B 4BG')
