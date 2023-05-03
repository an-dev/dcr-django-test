from django.db.models import Count, Sum
from django.http import JsonResponse

from countries.models import Region


def stats(request):
    # TODO - Provide name, number_countries and total_population for each region

    regions = Region.objects.annotate(
        total_population=Sum('countries__population'),
        number_countries=Count('countries')
    ).values('name', 'number_countries', 'total_population')

    response = {"regions": [r for r in regions]}

    return JsonResponse(response)
