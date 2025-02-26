from django.db import models

class SecurityScan(models.Model):
    target = models.CharField(max_length=255)
    tool_used = models.CharField(max_length=50)  
    status = models.CharField(max_length=20, default="pending")  # pending, running, completed, failed
    result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tool_used} scan on {self.target} - {self.status}"