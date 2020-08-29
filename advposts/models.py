import uuid
from django.db import models
from accounts.models import AccountUser
from org.models import Org
from django.utils.timezone import now
from django.db.models.signals import pre_save
from .utils import unique_tender_id_generator
# Create your models here.

class AdvDetails(models.Model):
    class Meta:
        verbose_name_plural = 'Advertisement Details'

    STATUS_FLAG = (
        ('Active', 'Active'),
        ('Closed', 'Closed')
    )
    tenderID        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #ref_id          = models.CharField()
    title           = models.CharField(max_length=100, verbose_name='Title')
    descrip         = models.CharField(max_length=300, verbose_name='Description')
    organisation    = models.ForeignKey('org.Org', on_delete=models.CASCADE, verbose_name='Organisation')
    author          = models.ForeignKey('accounts.Accountuser', on_delete=models.CASCADE,)
    dept            = models.CharField(max_length=60, verbose_name='Department')
    state           = models.CharField(choices=STATUS_FLAG, default='Active', max_length=10)
    bid_start_date  = models.DateTimeField(default=now, verbose_name='Bidding Opening Date')
    bid_end_date    = models.DateTimeField(verbose_name='Bidding Closing Date')
    part_start_date = models.DateTimeField(verbose_name='Uploading Opening Date')
    part_end_date   = models.DateTimeField(verbose_name='Uploading Closing Date')
    comb_start_date = models.DateTimeField(verbose_name='Combining Opening Date')
    comb_end_date   = models.DateTimeField(verbose_name='Combining Closing Date')
    advFile         = models.FileField(upload_to = 'advert_doc')
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            this = AdvDetails.objects.get(id=self.id)
            if this.advFile != self.advFile:
                this.advFile.delete(False)
        except: pass
        super(AdvDetails, self).save(*args, **kwargs)

class BidDetails(models.Model):
    class Meta:
        verbose_name_plural = 'Bidding Details'

    bidID           = models.CharField(max_length=16, primary_key=True, blank=True)
    tenderID        = models.ForeignKey('advposts.AdvDetails', on_delete=models.CASCADE,)
    bidderID        = models.ForeignKey('accounts.Accountuser', on_delete=models.CASCADE,)
    orgID           = models.ForeignKey('org.Org', on_delete=models.CASCADE)
    partHolderID    = models.ForeignKey('org.OrgUser', on_delete=models.CASCADE)
    bidPartID       = models.CharField(max_length=70)
    bidFilePath     = models.FileField(upload_to = 'bids')
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bidPartID
    
    def createShare(self):
        pass

def pre_save_create_bidID(sender, instance, *args, **kwargs):
    if not instance.bidID:
        instance.bidID = unique_tender_id_generator(instance)

pre_save.connect(pre_save_create_bidID, sender=BidDetails)


class FileModel(models.Model):
    file = models.FileField(upload_to='uploaded_files/')
    created = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        self.file.delete()
        return super().delete(*args, **kwargs)