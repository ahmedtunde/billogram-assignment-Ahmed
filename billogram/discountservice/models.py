from django.contrib.auth.models import AbstractUser, User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from billogram.utils.constants import STATUS_CHOICES
from billogram.framework import MyModel


now = datetime.now()
one_month_validity = now + relativedelta(months=+1)

class User(AbstractUser):
    is_brand = models.BooleanField(default=False)
    brand = models.ForeignKey('Brand', blank=True, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.is_brand and self.brand is None:
            self.is_brand = False

        return super().save(*args, **kwargs)

    def can_read(self, user):
        return True

    def can_update(self, user):
        return self == user

    def can_delete(self, user):
        return user.is_staff

    def can_create(self, user):
        return user.is_staff


class DiscountCode(MyModel):
    id = models.CharField(max_length=64, primary_key=True)
    rule = models.ForeignKey('DiscountRule', on_delete=models.CASCADE)
    valid_till = models.DateTimeField(default=one_month_validity)
    status = models.CharField(choices=STATUS_CHOICES, default="UNUSED", max_length=100)

    def __str__(self):
        return f"{self.id} until {self.valid_till}"

    # No discount codes are listed, but the user can fetch them by the ID
    # if they are aware of the ID
    def can_read(self, user):
        return True

    def can_create(self, user):
        if user.is_staff or user.is_brand:
            return True
        else:
            return False


class DiscountRule(MyModel):
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    discount = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])

    def __str__(self):
        return f"{self.discount}% on {self.brand} products"


class DiscountCodeUsage(MyModel):
    id = models.CharField(max_length=255, blank=True, primary_key=True)
    discount_code = models.ForeignKey('DiscountCode', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('discount_code', 'user')

    def __str__(self):
        return f"{self.id} at {self.used_at}"

    def save(self, *args, **kwargs):
        hashed_code = hash(self.discount_code.id)
        hashed_user_id = hash(self.user.id)
        _id = hash(hashed_code + hashed_user_id)
        self.id = _id
        return super().save(*args, **kwargs)

    def can_read(self, user):
        if user.is_staff:
            return True
        elif user.is_brand:
            return self.discount_code.rule.brand == user.brand
        else:
            return self.user == user

    def can_create(self, user):
        if user.is_staff or user.is_brand:
            return False
        else:
            return self.user == user


class Brand(MyModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# class DiscountVoucher(db.Model, ModelMixins):
#     id = db.Column(db.String, primary_key=True, default=generate_uuid)
#     discount_percentage = db.Column(db.Integer, nullable=False)
#     expiry_date = db.Column(db.DateTime, nullable=False)
#     is_active = db.Column(db.Boolean, default=True, nullable=False)
#     is_used = db.Column(db.Boolean, default=False, nullable=False)
#     brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
#     brand = db.relationship("Brand", backref=backref("brand", uselist=False))
#     customer_id = db.Column(db.Integer, nullable=True)

#     @classmethod
#     def get_new_discount_voucher(cls, brand_id, user_id):
#         """
#         Create a new voucher and assign it to logged in user.
#         :param brand_id:
#         :param user_id:
#         :return: dict: details of vouchers
#         """
#         got_discount_already = cls.query.filter_by(customer_id=user_id, brand_id=brand_id).first()

#         if got_discount_already:
#             return {"error": "Already got discount code"}

#         voucher = cls.query.filter(cls.expiry_date > datetime.utcnow()).filter_by(customer_id=None,
#                                                                                   is_active=True,
#                                                                                   is_used=False,
#                                                                                   brand_id=brand_id).first()
#         if voucher:
#             voucher.customer_id = user_id
#             voucher.save()
#             voucher_dict = voucher.to_dict()
#             voucher_dict['code'] = voucher_dict.pop('id')
#             # TODO: Notify brand for new user joined loyalty program using async task like celery.
#             return voucher_dict
#         else:
#             return {"error": "No vouchers available"}

#     @staticmethod
#     def create_discount_vouchers(payload, total_number_of_codes):
#         """
#         Responsible to create discount vouchers
#         :param payload: voucher config
#         :param total_number_of_codes: total number of vouchers to create
#         :return: dict
#         """
#         response = {}

#         validator = Validator(discount_code_schema, require_all=True)
#         if validator.validate(payload):
#             payload['expiry_date'] = datetime.utcfromtimestamp(payload['expiry_date'])
#             dvs = [DiscountVoucher(**payload) for i in range(total_number_of_codes)]
#             DiscountVoucher.bulk_save(dvs)
#             response = {"success": "vouchers created"}
#         else:
#             response = validator.errors

#         return response
