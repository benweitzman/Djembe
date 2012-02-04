from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Sum

VOTES = (
    (-1,"down"),
    (1,"up"),
)

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class TagVote(models.Model):
    tag = models.ForeignKey('TagCount')
    user = models.ForeignKey(User)
    way = models.IntegerField(choices=VOTES,default=1)

class TagCount(models.Model):
    tag = models.ForeignKey(Tag, related_name="tag_name")
    count = models.IntegerField(default=0)
    voters = models.ManyToManyField(User,through=TagVote)

    def __unicode__(self):
        return self.tag.name

    class Meta:
        ordering = ['-count','tag']

    def save(self, *args, **kwargs):
        self.count = self.getCount()
        super(TagCount,self).save(*args,**kwargs)

    def getCount(self):
        count = 15
        votes = self.tagvote_set.aggregate(count=Sum('way'))['count']
        if votes: count += votes
        return count
    

