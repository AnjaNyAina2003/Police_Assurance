from django.db import models, transaction, IntegrityError

from police_app.models import Police_assurance

class Quittance(models.Model):
    num_quittance = models.CharField(max_length=100, unique=True, editable=False)
    police_assurance = models.ForeignKey(Police_assurance, on_delete=models.SET_NULL, related_name='quittances', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        num = self.police_assurance.num_police if self.police_assurance else "sans police"
        return f"{self.num_quittance} - Police: {num}"

    def save(self, *args, **kwargs):
        if self.num_quittance:
            return super().save(*args, **kwargs)
        for _ in range(5):
            dernier = (Quittance.objects.filter(num_quittance__startswith='QT')
                    .order_by('-num_quittance').first())
            dernier_num = dernier.num_quittance[2:] if dernier else "00000"
            self.num_quittance = f"QT{self.convert_to_base36(int(dernier_num, 36) + 1, 5)}"
            try:
                with transaction.atomic():
                    return super().save(*args, **kwargs)
            except IntegrityError:
                self.num_quittance = ''
        raise IntegrityError("Impossible de générer un numéro de quittance unique")

    @staticmethod
    def convert_to_base36(number, length):
        base36_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = ""

        while number > 0:
            number, remainder = divmod(number, 36)
            result = base36_chars[remainder] + result

        return result.zfill(length)