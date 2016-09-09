#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.


class LearningPlan(models.Model):
	"学习计划表"
	id = models.AutoField(primary_key=True)
	level = models.IntegerField(default=0)
	num= models.IntegerField(default=0)
	user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

class Notes(models.Model):
	"笔记表"
	id = models.AutoField(primary_key=True)
	body = models.TextField(max_length=1000)
	time = models.DateTimeField()
	author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
	target_word = models.ForeignKey(
        'Words',
        on_delete=models.CASCADE,
    )

class Words(models.Model):
	"单词表，存放所有单词"
	id = models.AutoField(primary_key=True)
	english = models.CharField(max_length=20)
	explanation = models.CharField(max_length=100)
	example = models.TextField(max_length=1000)
	synonym = models.CharField(max_length=100)
	level = models.IntegerField(default=0)

	def toDict(self):
		
		return {
			'id':self.id,
			'explanation':[exp for exp in self.explanation.split('|')][0:-1],
			'example':[emp for emp in self.example.split('|')][0:4],
			'synonym':[s for s in self.synonym.split('|')][0:-1],
			'notes':[{'author':notes.author.username,'body':notes.body,'time':notes.time} for notes in self.notes_set.all()]
			
		}
		
		

class LearningList(models.Model):
	"单词表，存放正在学习的单词"
	id = models.AutoField(primary_key=True)
	repeat_times = models.IntegerField(default=0)
	review_time = models.DateTimeField()
	author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
	word = models.ForeignKey(
        'Words',
        on_delete=models.CASCADE,
    )




