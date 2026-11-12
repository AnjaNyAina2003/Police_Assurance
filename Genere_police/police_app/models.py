from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db import models, transaction, IntegrityError

from agence_app.models import Agence_assurance
from auth_app.models import User
from branch_app.models import Branche_assurance
from client_app.models import Clients

class Police_assurance(models.Model):
    STATUS_CHOICES = [
        ('actif', 'Actif'),
        ('expiree', 'Expiree'),
        ('annulee', 'Annulee'),
        ('suspendue', 'Suspendue'),
    ]
    num_police = models.CharField(max_length=20, unique=True, editable=False, null=True)
    num_compte_client = models.ForeignKey(Clients, on_delete=models.SET_NULL, related_name='client', null=True)
    date_generation = models.DateTimeField(auto_now_add=True, null=True)
    id_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    id_branche = models.ForeignKey(Branche_assurance, on_delete=models.SET_NULL, null=True, blank=True)
    agence = models.ForeignKey(Agence_assurance, on_delete=models.SET_NULL, null=True, blank=True)
    duree_couverture = models.IntegerField(help_text="Durée de couverture en mois", null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='actif')
    date_expiration = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return self.num_police

    def save(self, *args, **kwargs):
        if self.duree_couverture and not self.date_expiration:
            date_base = self.date_generation or timezone.now()
            self.date_expiration = date_base + relativedelta(months= self.duree_couverture)

        if self.num_police:
            super().save(*args, **kwargs)
        else:
            if self.id_branche is None:
                raise ValueError("Une branche est requise pour générer le numéro de police")
            prefixe = self.id_branche.prefixe
            for _ in range(5):
                dernier = (Police_assurance.objects
                        .filter(id_branche=self.id_branche)
                        .order_by('-num_police').first())
                dernier_num = dernier.num_police[len(prefixe):] if dernier else "00000"
                self.num_police = f"{prefixe}{self.convert_to_base36(int(dernier_num, 36) + 1, 5)}"
                try:
                    with transaction.atomic():
                        super().save(*args, **kwargs)
                    break
                except IntegrityError:
                    self.num_police = None
            else:
                raise IntegrityError("Impossible de générer un numéro de police unique")

        self.update_status()

    def update_status(self):
        if (self.status == 'actif' and self.date_expiration
                and timezone.now() > self.date_expiration):
            self.status = 'expiree'
            Police_assurance.objects.filter(pk=self.pk).update(status='expiree')

    @staticmethod
    def convert_to_base36(number, length):
        base36_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = ""

        while number > 0:
            number, remainder = divmod(number, 36)
            result = base36_chars[remainder] + result

        return result.zfill(length)
