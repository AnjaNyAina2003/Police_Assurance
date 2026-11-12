from django.db import models

class Agence_assurance(models.Model):
    nom_agence = models.CharField(max_length=50, unique= True)
    ville = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.nom_agence}({self.ville})"
    
    def agence_only(self):
        return f"{self.nom_agence}"