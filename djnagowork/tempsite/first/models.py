# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
import bigauto

class Entity(models.Model):
    id = bigauto.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    blurb = models.CharField(max_length=200, blank=True)
    summary = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    website = models.CharField(max_length=100, blank=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    primary_ext = models.CharField(max_length=50)
    merged_id = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    start_date = models.CharField(max_length=10, blank=True)
    end_date = models.CharField(max_length=10, blank=True)
    is_current = models.IntegerField(blank=True, null=True)
    last_user_id = models.BigIntegerField(blank=True, null=True)
    is_deleted = models.IntegerField()
    class Meta:
        db_table = 'entity'
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

class ExtensionDefinition(models.Model):
    id = bigauto.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    display_name = models.CharField(max_length=50)
    has_fields = models.IntegerField()
    parent = models.ForeignKey('self', blank=True, null=True)
    tier = models.BigIntegerField(blank=True, null=True)
    class Meta:
        db_table = 'extension_definition'
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

class ExtensionRecord(models.Model):
    id = bigauto.BigAutoField(primary_key=True)
    entity = models.ForeignKey(Entity)
    definition = models.ForeignKey(ExtensionDefinition)
    last_user_id = models.BigIntegerField(blank=True, null=True)
    class Meta:
        db_table = 'extension_record'
    def __unicode__(self):  # Python 3: def __str__(self):
        return str(self.id)+','+str(self.entity)+','+str(self.definition)

class Alias(models.Model):
    id = bigauto.BigAutoField(primary_key=True)
    entity = models.ForeignKey('Entity')
    name = models.CharField(max_length=200)
    context = models.CharField(max_length=50, blank=True)
    is_primary = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)#trigger
    updated_at = models.DateTimeField(blank=True, null=True)#trigger
    last_user_id = models.BigIntegerField(blank=True, null=True)
    class Meta:
        db_table = 'alias'
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

class ParliamentaryConstituency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    typeof = models.CharField(max_length=5)
    state = models.ForeignKey('States')
    class Meta:
        db_table = 'parliamentary_constituency'
    def __unicode__(self):
        return self.name

class States(models.Model):
    id = models.AutoField(primary_key=True)
    isocode = models.CharField(unique=True, max_length=5)
    fullname = models.CharField(max_length=200)
    typeof = models.CharField(max_length=1)
    class Meta:
        db_table = 'states'
    def __unicode__(self):
        return self.fullname