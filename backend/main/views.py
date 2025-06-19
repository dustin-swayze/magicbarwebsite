from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CocktailMenuImageForm, KitchenMenuImageForm, CarouselImageForm, ContactForm
from .models import CocktailMenuImage, KitchenMenuImage, CarouselImage, ContactMessage
from django.core.mail import send_mail



# Create your views here.
def home(request):
    latest_cocktail_menu = CocktailMenuImage.objects.filter(is_approved=True).order_by('-uploaded_at').first()
    latest_kitchen_menu = KitchenMenuImage.objects.filter(is_approved=True).order_by('-uploaded_at').first()
    carousel_images = CarouselImage.objects.filter(is_approved=True).order_by('-uploaded_at')

    return render(request, 'main/index.html', {
        'latest_menu': latest_cocktail_menu,
        'latest_kitchen_menu': latest_kitchen_menu,
        'carousel_images': carousel_images
    })

@login_required
def upload_menu(request):
    if request.method == 'POST':
        form = CocktailMenuImageForm(request.POST, request.FILES)
        if form.is_valid():
            menu_image = form.save(commit=False)
            menu_image.uploaded_by = request.user
            menu_image.is_approved = False  # Require admin approval
            menu_image.save()
            return redirect('upload_success')
    else:
        form = CocktailMenuImageForm()
    
    return render(request, 'main/upload_menu.html', {'form': form})

def upload_success(request):
    return render(request, 'main/upload_success.html')

@login_required
def upload_kitchen_menu(request):
    if request.method == 'POST':
        form = KitchenMenuImageForm(request.POST, request.FILES)
        if form.is_valid():
            menu_image = form.save(commit=False)
            menu_image.uploaded_by = request.user
            menu_image.is_approved = False
            menu_image.save()
            return redirect('upload_success')
    else:
        form = KitchenMenuImageForm()
    
    return render(request, 'main/upload_kitchen_menu.html', {'form': form})

@login_required
def upload_carousel_image(request):
    if request.method == 'POST':
        form = CarouselImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.uploaded_by = request.user
            image.is_approved = False
            image.save()
            return redirect('upload_success')  # or wherever you want to redirect
    else:
        form = CarouselImageForm()
    return render(request, 'main/upload_carousel_image.html', {'form': form})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            # Send email to manager
            send_mail(
                subject=f"New Contact Message from {contact.name}",
                message=contact.message,
                from_email=contact.email,
                recipient_list=['manager@example.com'],
                fail_silently=False,
            )
            return redirect('contact_success')
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})


def contact_success(request):
    return render(request, 'main/contact_success.html')

@login_required
@user_passes_test(lambda u: u.is_staff)
def view_messages(request):
    messages = ContactMessage.objects.order_by('-submitted_at')
    return render(request, 'main/view_messages.html', {'messages': messages})



def bar_menu_view(request):
    latest_menu = CocktailMenuImage.objects.filter(is_approved=True).order_by('-uploaded_at').first()
    return render(request, 'main/bar_menu.html', {'latest_menu': latest_menu})

def kitchen_menu_view(request):
    latest_kitchen_menu = KitchenMenuImage.objects.filter(is_approved=True).order_by('-uploaded_at').first()
    return render(request, 'main/kitchen_menu.html', {'latest_kitchen_menu': latest_kitchen_menu})
