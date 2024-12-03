from django.db import models

class Users(models.Model):
    userID = models.CharField(max_length=100)
    file_urls = models.JSONField()
    
    class Meta:
        db_table = 'face_users' 
    
    def __str__(self):
        return self.userID

    def add_file_url(self, url):
        if not self.file_urls:
            self.file_urls = []
        self.file_urls.append(url)
        self.save()
