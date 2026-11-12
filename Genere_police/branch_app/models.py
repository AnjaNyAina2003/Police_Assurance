from django.db import models

class Branche_assurance(models.Model):
    nom_branche = models.CharField(max_length=50, unique= True)
    prefixe = models.CharField(max_length=2, unique= True)
    
    def __str__(self):
        return f"{self.nom_branche}({self.prefixe})"