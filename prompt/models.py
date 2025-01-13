from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
class Prompt(BaseModel):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='prompts')
    title=models.CharField(max_length=100)
    prompt_text=models.TextField()
    main_image=models.ImageField(upload_to='media', null=True, blank=True)
    
    def __str__(self):
        return self.title