from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render

from .choices import bedroom_choices, price_choices, state_choices

from .models import Listing


# Create your views here.
def index(request):
  listings = Listing.objects.order_by('-list_date').filter(is_published=True)

  paginator = Paginator(listings, 3)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  context = {
    "listings": paged_listings
  }

  return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)

  context = {
    'listing': listing
  }
  return render(request, 'listings/listing.html', context)

def search(request):

  quereyset_list = Listing.objects.order_by('-list_date')

  # keyword search
  if 'keywords' in request.GET: 
    keywords = request.GET['keywords']
    if keywords: 
      quereyset_list = quereyset_list.filter(description__icontains=keywords)

  # city search
  if 'city' in request.GET: 
    city = request.GET['city']
    if city:
      quereyset_list = quereyset_list.filter(city__iexact=city)

  # state search
  if 'state' in request.GET: 
    state = request.GET['state']
    if state:
      quereyset_list = quereyset_list.filter(state__iexact=state)

  # bedrooms search
  if 'bedrooms' in request.GET: 
    bedrooms = request.GET['bedrooms']
    if bedrooms:
      quereyset_list = quereyset_list.filter(bedrooms__lte=bedrooms)

  # price search
  if 'price' in request.GET: 
    price = request.GET['price']
    if price:
      quereyset_list = quereyset_list.filter(price__lte=price)

  context = {
    'bedroor_choices': bedroom_choices,
    'price_choices': price_choices,
    'state_choices': state_choices,
    'listings': quereyset_list, 
    'values': request.GET
  }

  return render(request, 'listings/search.html', context)



