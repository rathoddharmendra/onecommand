# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class AccessRecord(models.Model):
    entry_id = models.CharField(max_length=264,unique=True)
    date = models.DateField()
    comp_name = models.CharField(max_length=264)
    command = models.CharField(max_length=264)
    
    def __str__(self):
        return self.date
    
