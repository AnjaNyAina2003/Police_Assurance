from django.db import models, transaction, IntegrityError
from django.utils import timezone
from datetime import timedelta

class Clients(models.Model):
    num_compte_client = models.CharField(max_length=100, unique=True, editable=False)
    nom_client = models.CharField(max_length=100)
    prenom_client = models.CharField(max_length=100)    
    telephone = models.CharField(max_length=25)
    adresse = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.num_compte_client} - {self.nom_client} {self.prenom_client}"

    def save(self, *args, **kwargs):
        if self.num_compte_client:
            return super().save(*args, **kwargs)
        for _ in range(5):
            dernier = (Clients.objects.filter(num_compte_client__startswith='CLI')
                    .order_by('-num_compte_client').first())
            dernier_num = dernier.num_compte_client[3:] if dernier else "00000"
            self.num_compte_client = f"CLI{self.convert_to_base36(int(dernier_num, 36) + 1, 5)}"
            try:
                with transaction.atomic():
                    return super().save(*args, **kwargs)
            except IntegrityError:
                self.num_compte_client = ''
        raise IntegrityError("Impossible de générer un numéro de compte unique")

    @staticmethod
    def convert_to_base36(number, length):
        base36_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = ""

        while number > 0:
            number, remainder = divmod(number, 36)
            result = base36_chars[remainder] + result

        return result.zfill(length)
