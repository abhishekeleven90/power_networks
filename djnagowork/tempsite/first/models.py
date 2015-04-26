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

#adding here latest................................................................................

class Nationalparty(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    abbr = models.CharField(unique=True, max_length=10)
    symbol = models.CharField(max_length=200, blank=True)
    foundingyear = models.IntegerField(blank=True, null=True)
    fetchyear = models.IntegerField()
    source = models.CharField(max_length=1000)
    class Meta:
        db_table = 'nationalparty'
    def __unicode__(self):
        return self.name

class Stateparty(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    state = models.ForeignKey('States', blank=True, null=True)
    abbr = models.CharField(unique=True, max_length=10)
    symbol = models.CharField(max_length=200, blank=True)
    foundingyear = models.IntegerField(blank=True, null=True)
    fetchyear = models.IntegerField()
    source = models.CharField(max_length=1000)
    class Meta:
        db_table = 'stateparty'
    def __unicode__(self):
        return self.name

class UnrecognizedParty(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    abbr = models.CharField(max_length=10, blank=True)
    symbol = models.CharField(max_length=200, blank=True)
    foundingyear = models.IntegerField(blank=True, null=True)
    fetchyear = models.IntegerField()
    source = models.CharField(max_length=1000)
    class Meta:
        db_table = 'unrecognized_party'
    def __unicode__(self):
        return self.name


class Politicalparty(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    state = models.ForeignKey('States', blank=True, null=True)
    abbr = models.CharField(max_length=10)
    symbol = models.CharField(max_length=200, blank=True)
    foundingyear = models.IntegerField(blank=True, null=True)
    fetchyear = models.IntegerField()
    source = models.CharField(max_length=1000)
    class Meta:
        db_table = 'politicalparty'
    def __unicode__(self):
        return self.name

class PoliticalPartyAlias(models.Model):
    id = bigauto.BigAutoField(primary_key=True)
    party = models.ForeignKey('Politicalparty')
    name = models.CharField(max_length=200)
    is_primary = models.IntegerField()
    class Meta:
        db_table = 'politicalpartyalias'
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

class QcBod(models.Model):
    id = bigauto.BigAutoField(primary_key=True)
    cin = models.ForeignKey('QcCompany', db_column='cin', blank=True, null=True)
    din = models.ForeignKey('QcDirector', db_column='din', blank=True, null=True)
    doa = models.CharField(max_length=15, blank=True)
    designation = models.CharField(max_length=300, blank=True)
    class Meta:
        db_table = 'qc_bod'

class QcCompany(models.Model):
    cin = models.CharField(primary_key=True, max_length=25)
    authorizedsharecapital = models.CharField(db_column='AuthorizedShareCapital', max_length=50, blank=True) # Field name made lowercase.
    classofcompany = models.CharField(db_column='ClassofCompany', max_length=50, blank=True) # Field name made lowercase.
    companycategory = models.CharField(db_column='CompanyCategory', max_length=250, blank=True) # Field name made lowercase.
    companystatusforefiling = models.CharField(db_column='CompanyStatusforeFiling', max_length=60, blank=True) # Field name made lowercase.
    companysubcategory = models.CharField(db_column='CompanySubCategory', max_length=70, blank=True) # Field name made lowercase.
    dateofincorporation = models.CharField(db_column='DateofIncorporation', max_length=15, blank=True) # Field name made lowercase.
    dateoflastannualgeneralmeeting = models.CharField(db_column='DateofLastAnnualGeneralMeeting', max_length=15, blank=True) # Field name made lowercase.
    dateoflatestbalancesheet = models.CharField(db_column='DateofLatestBalanceSheet', max_length=15, blank=True) # Field name made lowercase.
    emailid = models.CharField(db_column='EmailID', max_length=150, blank=True) # Field name made lowercase.
    listingstatus = models.CharField(db_column='Listingstatus', max_length=50, blank=True) # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=500, blank=True) # Field name made lowercase.
    numberofmembers = models.IntegerField(db_column='NumberofMembers', blank=True, null=True) # Field name made lowercase.
    paidupcapital = models.CharField(db_column='PaidUpCapital', max_length=50, blank=True) # Field name made lowercase.
    registeredofficeaddress = models.CharField(db_column='RegisteredOfficeAddress', max_length=1800, blank=True) # Field name made lowercase.
    registrationnumber = models.CharField(db_column='RegistrationNumber', max_length=14, blank=True) # Field name made lowercase.
    registrationstate = models.CharField(db_column='RegistrationState', max_length=70, blank=True) # Field name made lowercase.
    link = models.CharField(max_length=500, blank=True)
    class Meta:
        db_table = 'qc_company'

class QcDirector(models.Model):
    din = models.CharField(primary_key=True, max_length=12)
    address = models.CharField(max_length=1800, blank=True)
    dsc_status = models.CharField(max_length=40, blank=True)
    link = models.CharField(max_length=400, blank=True)
    name = models.CharField(max_length=300, blank=True)
    class Meta:
        db_table = 'qc_director'

class QTrack(models.Model):
    mynetaid = models.IntegerField(primary_key=True)
    class Meta:
        db_table = 'q_track'

class QQuery(models.Model):
    id = models.AutoField(primary_key=True)
    hashmyfield = models.CharField(max_length=32)
    class Meta:
        db_table = 'q_query'