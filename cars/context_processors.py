def add_global_context(request):
    from .models import Brand, Record
    return {'total_brands_count': Brand.objects.all().count(),
            'total_records_count': Record.objects.all().count()}
