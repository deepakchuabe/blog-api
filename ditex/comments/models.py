# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
# Create your models here.
from posts.models import Post
# Generic Foreign Key relation 
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Comment(models.Model):

	user 		= models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	#post        = models.ForeignKey(Post)

	#Generic relation 
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')


	content 	= models.TextField()
	timestamp 	= models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return str(self.user.username)

	def __unique__(self):
		return str(self.user.username)
