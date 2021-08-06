import os
import csv
import datetime
import string

from django.http import HttpResponse
from django.views import generic
from django.conf import settings
from datetime import datetime as dt

from .models import Car, Brand, Fuel, Body, Kind, Purpose, Model, Record, Operation, Department


class IndexView(generic.ListView):
    template_name = 'cars/index.html'
    context_object_name = 'car_list'

    def get_queryset(self):
        return Car.objects.order_by('license_plate')[:5]


class DetailView(generic.DetailView):
    model = Car
    template_name = 'cars/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_url'] = "https://www.google.com/search?q="
        return context


class BrandsView(generic.ListView):
    template_name = 'cars/brands.html'
    context_object_name = 'brand_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        letter = self.request.GET.get('letter') or 'a'
        context["current_letter"] = letter
        kind = self.request.GET.get('kind') or 4
        try:
            kind = int(kind)
        except:
            kind=4
        context["current_kind_id"] = kind
        context["alphabet"] = list("abcdefghijklmnopqrstuvwxyz")
        context["kind_list"] = Kind.objects.all().order_by('name')
        return context

    def get_queryset(self):
        letter = self.request.GET.get('letter') or 'a'
        kind = self.request.GET.get('kind') or ''
        try:
            kind = int(kind)
        except:
            kind = 4
        return Brand.objects.filter(name__istartswith=letter, model__car__kind_id=kind).distinct().order_by('name')


class BrandsDetailView(generic.DetailView):
    model = Brand
    template_name = 'cars/brand_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kind = self.request.GET.get('kind') or ''
        try:
            kind = int(kind)
        except:
            kind = ''
        context['model_list'] = Model.objects.filter(
            brand=self.object, car__kind_id=kind).distinct().order_by('name')
        letter = self.request.GET.get('letter') or 'a'
        context["current_letter"] = letter
        context["current_kind_id"] = kind
        context["alphabet"] = list("abcdefghijklmnopqrstuvwxyz")
        context["kind_list"] = Kind.objects.all().order_by('name')
        return context


class ModelsDetailView(generic.ListView):
    template_name = 'cars/model_detail.html'
    context_object_name = 'car_list'
    paginate_by = 30

    def get_queryset(self, **kwargs):
        kind = self.request.GET.get('kind') or ''
        try:
            kind = int(kind)
        except:
            kind = 4
        return Car.objects.filter(
            model=Model.objects.get(pk=self.kwargs['pk']), kind_id=kind).distinct().order_by(
            'make_year')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car_model'] = Model.objects.get(pk=self.kwargs['pk'])
        return context


class RecordsView(generic.ListView):
    template_name = 'cars/records.html'
    context_object_name = 'record_list'
    paginate_by = 30

    def get_queryset(self):
        return Record.objects.order_by('-d_reg')


class RecordsDetailView(generic.DetailView):
    model = Record
    template_name = 'cars/record_detail.html'


def load_data(request):
    with open(os.path.join(settings.BASE_DIR,
                           #                      'tz_opendata_z01012021_po01052021.csv'),
                           'tz_opendata_z01012021_po01072021.csv'),
              encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                person = row[0]
                reg_addr_koatuu = row[1]
                oper_code = row[2]
                oper_name = row[3]
                d_reg = row[4]
                dep_code = row[5]
                dep = row[6]
                brand = row[7]
                model = row[8]
                vin = row[9]
                make_year = row[10]
                color = row[11]
                kind = row[12]
                body = row[13]
                purpose = row[14]
                fuel = row[15]
                capacity = row[16]
                own_weight = row[17]
                total_weight = row[18]
                n_reg_new = row[19]

                q = Brand.objects.filter(name=brand)
                if not q:
                    brand_obj = Brand.objects.create(name=brand)
                else:
                    brand_obj = q[0]

                q = Model.objects.filter(name=model, brand=brand_obj)
                if not q:
                    model_obj = Model.objects.create(name=model,
                                                     brand=brand_obj)
                else:
                    model_obj = q[0]

                q = Fuel.objects.filter(name=fuel)
                if not q:
                    fuel_obj = Fuel.objects.create(name=fuel)
                else:
                    fuel_obj = q[0]

                q = Body.objects.filter(name=body)
                if not q:
                    body_obj = Body.objects.create(name=body)
                else:
                    body_obj = q[0]

                q = Kind.objects.filter(name=kind)
                if not q:
                    kind_obj = Kind.objects.create(name=kind)
                else:
                    kind_obj = q[0]

                q = Purpose.objects.filter(name=purpose)
                if not q:
                    purpose_obj = Purpose.objects.create(name=purpose)
                else:
                    purpose_obj = q[0]

                if n_reg_new:
                    q = Car.objects.filter(license_plate=n_reg_new)
                    if not q:
                        car_obj = Car.objects.create(license_plate=n_reg_new,
                                           model=model_obj,
                                           vin=vin,
                                           make_year=datetime.datetime(
                                               int(make_year), 1, 1),
                                           color=color,
                                           kind=kind_obj,
                                           body=body_obj,
                                           purpose=purpose_obj,
                                           fuel=fuel_obj,
                                           capacity=capacity,
                                           own_weight=own_weight,
                                           total_weight=total_weight
                                           )
                    else:
                        car_obj = q[0]
                q = Department.objects.filter(dep_code=dep_code)
                if not q:
                    department_obj = Department.objects.create(dep_code=dep_code,dep=dep)
                else:
                    department_obj = q[0]

                q = Operation.objects.filter(code=oper_code)
                if not q:
                    operation_obj = Operation.objects.create(code=oper_code,name=oper_name)
                else:
                    operation_obj = q[0]

                q = Record.objects.filter(person=person,
                                        reg_addr_koatuu = reg_addr_koatuu,
                                        operation = operation_obj,
                                        d_reg = dt.strptime(d_reg, "%d.%m.%Y"),
                                        department=department_obj,
                                        brand=brand_obj,
                                        model=model_obj,
                                        vin=vin,
                                        make_year=datetime.datetime(
                                           int(make_year), 1, 1),
                                        color=color,
                                        kind=kind_obj,
                                        body=body_obj,
                                        purpose=purpose_obj,
                                        fuel=fuel_obj,
                                        capacity=capacity,
                                        own_weight=own_weight,
                                        total_weight=total_weight,
                                        n_reg_new=n_reg_new,
                                        car=car_obj)
                if not q:
                    Record.objects.create(
                                        person=person,
                                        reg_addr_koatuu = reg_addr_koatuu,
                                        operation = operation_obj,
                                        d_reg = dt.strptime(d_reg, "%d.%m.%Y"),
                                        department=department_obj,
                                        brand=brand_obj,
                                        model=model_obj,
                                        vin=vin,
                                        make_year=datetime.datetime(
                                           int(make_year), 1, 1),
                                        color=color,
                                        kind=kind_obj,
                                        body=body_obj,
                                        purpose=purpose_obj,
                                        fuel=fuel_obj,
                                        capacity=capacity,
                                        own_weight=own_weight,
                                        total_weight=total_weight,
                                        n_reg_new=n_reg_new,
                                        car=car_obj
                                       )

                line_count += 1
        print(f'Processed {line_count} lines.')
    return HttpResponse('Done')
