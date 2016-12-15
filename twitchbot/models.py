from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    email = models.CharField(max_length=100)
    link = models.CharField(max_length=1000, blank=True)
    email_enabled = models.BooleanField(default=True)
    currency = models.DecimalField(max_digits=13, decimal_places=2, default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class UserClass(models.Model):
    user = models.ForeignKey('User', related_name='class_users')
    group = models.ForeignKey('Class', related_name='class_groups')

    def __unicode__(self):
        return "%s - %s" % (self.group.display, self.user.name)

    class Meta:
        ordering = ['group', 'user']
        verbose_name_plural="User classes"
        unique_together = ['user', 'group']

class Class(models.Model):
    id = models.CharField(max_length=1, primary_key=True)
    display = models.CharField(max_length=100)
    earn_rate = models.DecimalField(max_digits=12, decimal_places=2)

    def __unicode__(self):
        return self.display

    class Meta:
        ordering = ['display']
        verbose_name_plural="Classes"

class Inventory(models.Model):
    user_name = models.ForeignKey('User', related_name='inv_users')
    item_name = models.ForeignKey('Item', related_name='inv_items')
    quantity = models.IntegerField()

    def __unicode__(self):
        return "%s: %d %s" % (self.user_name.name, self.quantity, self.item_name.name)

    class Meta:
        ordering = ['user_name', 'item_name']
        verbose_name_plural="Inventories"
        unique_together = ['user_name', 'item_name']

class Item(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.CharField(max_length=2000)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name', 'price']

class Command(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    group = models.ForeignKey('Class', related_name='command_group')
    description = models.CharField(max_length=1000, blank=True)

    def __unicode__(self):
        return "%s: %s" % (self.name, self.description)

    class Meta:
        ordering = ['name']

class ChatCommand(Command):
    response = models.CharField(max_length=1000)

class ActivityCommand(Command):
    code = models.TextField()

