from django.db import models 
from datetime import datetime, timedelta 
from django.contrib.auth.models import User 
from django.db.models.query import QuerySet 
 
 
# Create your models here. 
 
def today(): 
 	now = datetime.now() 
	start = datetime.min.replace(year=now.year, month=now.month, 
 			day=now.day) 
 	end = (start + timedelta(days=1)) - timedelta.resolution 
 	return (start, end) 
 
 
class EventQuerySet(QuerySet): 
 	def today(self): 
 		print "In query today" 
 		return self.filter(creation_date__range=today()) 
 
 
class EventManager(models.Manager): 
 	def get_query_set(self): 
 		print "In manager get query set" 
 		return EventQuerySet(self.model) 
 
 
 	def today(self): 
 		print "In manager today" 
 		return self.get_query_set().today() 
 
 
#Model's sub class 
class Event(models.Model): 
 	description = models.TextField() 
 	creation_date = models.DateTimeField(default=datetime.now) 
 	start_date = models.DateTimeField(null=True, blank=True) 
 	creator = models.ForeignKey(User, related_name='event_creator_set') 
 	attendees = models.ManyToManyField(User, through = "Attendance") 
 	latest = models.BooleanField(default=True) 
 	 
 	# link defaults object to our custom manager 
 	objects = EventManager() 
 
 
 	def __unicode__(self): 
 		return self.description 
 	 
 	def save(self, **kwargs): 
 		#objects is default manager 
 		Event.objects.today().filter(latest=True, 
 			creator=self.creator).update(latest=False) 
 		super(Event, self).save(**kwargs) 
 
 
class Attendance(models.Model): 
 	user = models.ForeignKey(User) 
 	event = models.ForeignKey(Event) 
 	registration_date = models.DateTimeField(default=datetime.now) 
 
 
 	def __unicode__(self): 
 		return "%s is attending %s" % (self.user.username, self.event) 
 	 
 	class Meta(object): 
 		verbose_name_plural = "Attendance" 
