from django.shortcuts import render, redirect
from .models import Bag, Reader
from .forms import BagForm, CheckoutForm
from django.contrib.auth.decorators import login_required

@login_required
def mybag(request):
    if request.method == "POST":
        bag_form = BagForm(request.POST)
        checkout_form = CheckoutForm(request.POST)
        if bag_form.is_valid() and checkout_form.is_valid():
            bag = bag_form.save(commit=False)
            active_reader = Reader.objects.filter(is_active=True).first()
            if active_reader:
                bag.reader = active_reader
                bag.save()

                # Save checkout information
                active_reader.name = checkout_form.cleaned_data['name']
                active_reader.phone_number = checkout_form.cleaned_data['phone_number']
                active_reader.reference_id = checkout_form.cleaned_data['reference_id']
                active_reader.save()

                # Perform checkout operations
                for item in Bag.objects.filter(reader=active_reader):
                    # Mark the books as checked out, etc.
                    item.status = 'checked_out'
                    item.save()

                return redirect('checkout_success')  # Redirect to a success page
    else:
        bag_form = BagForm()
        checkout_form = CheckoutForm()

    active_reader = Reader.objects.filter(is_active=True).first()
    if active_reader:
        bag_items = Bag.objects.filter(reader=active_reader)
    else:
        bag_items = []

    return render(request, 'mybag/mybag.html', {
        'bag_form': bag_form,
        'checkout_form': checkout_form,
        'bags': bag_items
    })

@login_required
def checkout(request):
    if request.method == "POST":
        checkout_form = CheckoutForm(request.POST)
        if checkout_form.is_valid():
            active_reader = Reader.objects.filter(is_active=True).first()
            if active_reader:
                active_reader.name = checkout_form.cleaned_data['name']
                active_reader.phone_number = checkout_form.cleaned_data['phone_number']
                active_reader.reference_id = checkout_form.cleaned_data['reference_id']
                active_reader.save()

                # Process checkout for all books in the bag
                bag_items = Bag.objects.filter(reader=active_reader)
                for item in bag_items:
                    # Mark the books as checked out, if necessary
                    # For example, you could update a status field
                    item.status = 'checked_out'
                    item.save()

                return redirect('checkout_success')  # Redirect to a success page
    else:
        checkout_form = CheckoutForm()

    return render(request, 'mybag/checkout.html', {
        'checkout_form': checkout_form,
    })