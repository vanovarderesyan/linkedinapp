from django.db import models

# Create your models here.

class Campaign(models.Model):
    compaign_name = models.CharField(null=True,blank=True, max_length=250)
    linkedin_id = models.CharField(null=True,blank=True, max_length=250)
    count = models.CharField(null=True,blank=True, max_length=250)
    linkedin_url = models.TextField(null=True,blank=True)

    

    class Meta:
        verbose_name = "Campaign"
        verbose_name_plural = "Campaign"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Campaign_detail", kwargs={"pk": self.pk})


class SendindUser(models.Model):
    mini_profile = models.CharField(null=True,blank=True, max_length=250)
    seen = models.BooleanField(default=False)
    campaign = models.ForeignKey(Campaign,null=True,blank=True, on_delete=models.CASCADE)
    connect = models.BooleanField(default=False)
    message = models.BooleanField(default=False)

    class Meta:
        verbose_name = "SendindUser"
        verbose_name_plural = "SendindUsers"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("SendindUser_detail", kwargs={"pk": self.pk})
