from django.db import models
from better_choices import Choices
from simple_metaclass import ChoicesMeta


# from django docs
class Student(models.Model):

    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'

    YEAR_IN_SCHOOL_CHOICES = (
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    )
    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )

    @classmethod
    def rookies(cls):

        return cls.objects.filter(year_in_school=cls.FRESHMAN)


# now with the helper class
class Studentv2(models.Model):

    YEAR_IN_SCHOOL_CHOICES = Choices(
        ('FR', 'freshman', 'Freshman'),
        ('SO', 'sophomore', 'Sophomore'),
        ('JR', 'junior', 'Junior'),
        ('SR', 'senior', 'Senior')
    )
    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=YEAR_IN_SCHOOL_CHOICES.freshman,
    )

    @classmethod
    def rookies(cls):

        return cls.objects.filter(year_in_school=cls.YEAR_IN_SCHOOL_CHOICES.freshman)


# with the metaclass
class Studentv3(models.Model):

    class YearInSchool(object):
        __metaclass__ = ChoicesMeta

        freshman = 'FR'
        sophomore = 'SO'
        junior = 'JR'
        senior = 'SR'

    year_in_school = models.CharField(
        max_length=2,
        choices=YearInSchool,
        default=YearInSchool.freshman,
    )

    @classmethod
    def rookies(cls):

        return cls.objects.filter(year_in_school=cls.YearInSchool.freshman)

