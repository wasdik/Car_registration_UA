from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Model(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return ''.join((self.name, ' (', self.brand.name, ')'))


class Fuel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Kind(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Body(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Purpose(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Car(models.Model):
    license_plate = models.CharField(max_length=8, null=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    vin = models.CharField(max_length=17, default="", blank=True)
    make_year = models.DateField('Make year')
    color = models.CharField(max_length=100)
    kind = models.ForeignKey(Kind, on_delete=models.CASCADE)
    body = models.ForeignKey(Body, on_delete=models.CASCADE)
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE)
    fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE)
    capacity = models.CharField(max_length=8)
    own_weight = models.CharField(max_length=8)
    total_weight = models.CharField(max_length=8)

    def __str__(self):
        return '' + str(self.model) + ' ' + str(
            self.make_year.year) + " (" + self.license_plate + ")"


class Operation(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Department(models.Model):
    dep_code = models.CharField(max_length=5)
    dep = models.CharField(max_length=10)

    def __str__(self):
        return self.dep


class Record(models.Model):
    person = models.CharField(max_length=1, blank=True)
    reg_addr_koatuu = models.CharField(max_length=8, blank=True)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, null=True)
    d_reg = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE, null=True)
    vin = vin = models.CharField(max_length=17, default="", blank=True)
    make_year = models.DateField('Make year', null=True)
    color = models.CharField(max_length=100, null=True)
    kind = models.ForeignKey(Kind, on_delete=models.CASCADE, null=True)
    body = models.ForeignKey(Body, on_delete=models.CASCADE, null=True)
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE, null=True)
    fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE, null=True)
    capacity = models.CharField(max_length=8, blank=True)
    own_weight = models.CharField(max_length=8, blank=True)
    total_weight = models.CharField(max_length=8, blank=True)
    n_reg_new = models.CharField(max_length=10, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '' + str(self.d_reg) + ' ' + str(
            self.operation) + " (" + str(self.department) + ")"
