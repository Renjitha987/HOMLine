from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from .models import (
    Category, Service, Update, MembershipPlan, 
    ServiceRequest, ServiceRequestLog, FAQ, CustomerReview, MembershipEnquiry
)
from .forms import ServiceRequestForm, TrackRequestForm, MembershipEnquiryForm, QuickContactForm

def home_view(request):
    categories = Category.objects.prefetch_related('services').all()
    featured_services = Service.objects.filter(is_featured=True)[:6]
    featured_updates = Update.objects.filter(is_featured=True)[:3]
    membership_plans = MembershipPlan.objects.all()
    faqs = FAQ.objects.all()[:6]
    reviews = CustomerReview.objects.filter(is_verified=True)[:5]
    all_services = Service.objects.all()
    
    service_request_form = ServiceRequestForm()
    track_form = TrackRequestForm()

    if request.method == 'POST' and 'submit_request' in request.POST:
        service_request_form = ServiceRequestForm(request.POST, request.FILES)
        if service_request_form.is_valid():
            req_obj = service_request_form.save()
            
            # Create initial timeline log
            ServiceRequestLog.objects.create(
                request=req_obj,
                status='Pending',
                title='Request Registered',
                description='Your digital service request has been logged successfully into HOMline systems.'
            )
            
            messages.success(
                request, 
                f"Your request has been submitted successfully! Your Request ID is: {req_obj.request_id}. Please save this ID to track your request status."
            )
            return redirect('track_request_with_id', request_id=req_obj.request_id)
        else:
            messages.error(request, "There was an error in your submission. Please check the form details.")

    context = {
        'categories': categories,
        'featured_services': featured_services,
        'featured_updates': featured_updates,
        'membership_plans': membership_plans,
        'faqs': faqs,
        'reviews': reviews,
        'all_services': all_services,
        'service_request_form': service_request_form,
        'track_form': track_form,
        'active_tab': 'home'
    }
    return render(request, 'core/home.html', context)


def about_view(request):
    return render(request, 'core/about.html', {'active_tab': 'about'})


def services_list_view(request):
    categories = Category.objects.all()
    selected_category_slug = request.GET.get('category', 'all')
    search_query = request.GET.get('q', '').strip()

    services = Service.objects.select_related('category').all()

    if selected_category_slug and selected_category_slug != 'all':
        services = services.filter(category__slug=selected_category_slug)

    if search_query:
        services = services.filter(
            Q(title__icontains=search_query) | 
            Q(short_summary__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    context = {
        'categories': categories,
        'services': services,
        'selected_category_slug': selected_category_slug,
        'search_query': search_query,
        'active_tab': 'services'
    }
    return render(request, 'core/services_list.html', context)


def service_detail_view(request, slug):
    service = get_object_or_404(Service, slug=slug)
    related_services = Service.objects.filter(category=service.category).exclude(id=service.id)[:3]
    request_form = ServiceRequestForm(initial={'service': service})

    context = {
        'service': service,
        'related_services': related_services,
        'request_form': request_form,
        'active_tab': 'services'
    }
    return render(request, 'core/service_detail.html', context)


def how_it_works_view(request):
    return render(request, 'core/how_it_works.html', {'active_tab': 'how_it_works'})


def membership_view(request):
    plans = MembershipPlan.objects.all()
    enquiry_form = MembershipEnquiryForm()

    if request.method == 'POST':
        enquiry_form = MembershipEnquiryForm(request.POST)
        if enquiry_form.is_valid():
            enquiry_form.save()
            messages.success(request, "Thank you for your interest in HOMline Membership! Our team will contact you shortly.")
            return redirect('membership')

    context = {
        'plans': plans,
        'enquiry_form': enquiry_form,
        'active_tab': 'membership'
    }
    return render(request, 'core/membership.html', context)


def updates_list_view(request):
    updates = Update.objects.all()
    tag_filter = request.GET.get('tag', 'all')
    if tag_filter and tag_filter != 'all':
        updates = updates.filter(category_tag=tag_filter)

    context = {
        'updates': updates,
        'tag_filter': tag_filter,
        'active_tab': 'updates'
    }
    return render(request, 'core/updates_list.html', context)


def update_detail_view(request, slug):
    update_item = get_object_or_404(Update, slug=slug)
    recent_updates = Update.objects.exclude(id=update_item.id)[:4]

    context = {
        'update_item': update_item,
        'recent_updates': recent_updates,
        'active_tab': 'updates'
    }
    return render(request, 'core/update_detail.html', context)


def faqs_view(request):
    category_filter = request.GET.get('cat', 'all')
    search_q = request.GET.get('q', '').strip()

    faqs = FAQ.objects.all()
    if category_filter and category_filter != 'all':
        faqs = faqs.filter(category=category_filter)
    if search_q:
        faqs = faqs.filter(Q(question__icontains=search_q) | Q(answer__icontains=search_q))

    categories = [choice[0] for choice in FAQ.CATEGORY_CHOICES]

    context = {
        'faqs': faqs,
        'categories': categories,
        'category_filter': category_filter,
        'search_q': search_q,
        'active_tab': 'faqs'
    }
    return render(request, 'core/faqs.html', context)


def contact_view(request):
    form = QuickContactForm()
    if request.method == 'POST':
        form = QuickContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Thank you! Your message has been sent to HOMline DIGI seva. We will respond via Call / WhatsApp shortly.")
            return redirect('contact')

    return render(request, 'core/contact.html', {'form': form, 'active_tab': 'contact'})


def track_request_view(request, request_id=None):
    tracked_request = None
    searched_id = request_id or request.GET.get('request_id', '').strip()
    error_message = None
    timeline_logs = []

    if searched_id:
        try:
            tracked_request = ServiceRequest.objects.get(request_id__iexact=searched_id)
            timeline_logs = tracked_request.timeline_logs.all()
        except ServiceRequest.DoesNotExist:
            error_message = f"No service request found with ID '{searched_id}'. Please verify your reference number."

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('json') == '1':
        if tracked_request:
            logs_data = [{
                'title': log.title,
                'status': log.status,
                'description': log.description,
                'date': log.created_at.strftime('%d %b %Y, %I:%M %p')
            } for log in timeline_logs]

            return JsonResponse({
                'found': True,
                'request_id': tracked_request.request_id,
                'name': tracked_request.full_name,
                'service': tracked_request.get_service_title(),
                'status': tracked_request.status,
                'created_at': tracked_request.created_at.strftime('%d %b %Y, %I:%M %p'),
                'updated_at': tracked_request.updated_at.strftime('%d %b %Y, %I:%M %p'),
                'notes': tracked_request.admin_notes or 'Your request has been received and is being processed by HOMline support.',
                'timeline': logs_data
            })
        return JsonResponse({'found': False, 'error': error_message or 'Invalid Request ID'})

    context = {
        'tracked_request': tracked_request,
        'timeline_logs': timeline_logs,
        'searched_id': searched_id,
        'error_message': error_message,
        'active_tab': 'track'
    }
    return render(request, 'core/track_request.html', context)


def request_service_view(request):
    service_id = request.GET.get('service_id')
    initial_service = None
    if service_id:
        initial_service = Service.objects.filter(id=service_id).first()

    form = ServiceRequestForm(initial={'service': initial_service} if initial_service else None)

    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            req_obj = form.save()
            
            # Create initial timeline log
            ServiceRequestLog.objects.create(
                request=req_obj,
                status='Pending',
                title='Request Form Submitted',
                description='Your online application request has been received by HOMline support team.'
            )
            
            messages.success(
                request, 
                f"Your request has been registered! Request ID: {req_obj.request_id}."
            )
            return redirect('track_request_with_id', request_id=req_obj.request_id)

    return render(request, 'core/request_service.html', {'form': form, 'selected_service': initial_service})


def receipt_view(request, request_id):
    req_obj = get_object_or_404(ServiceRequest, request_id__iexact=request_id)
    return render(request, 'core/receipt.html', {'req_obj': req_obj})


def policy_view(request, policy_name):
    policies = {
        'terms': {
            'title': 'Terms & Conditions',
            'content': '''
            <h3>1. Introduction</h3>
            <p>Welcome to HOMline DIGI seva ("HOMline"). By accessing or using our services, website, and support channels (Call, WhatsApp, Email), you agree to comply with and be bound by these Terms & Conditions.</p>

            <h3>2. Nature of Service</h3>
            <p>HOMline DIGI seva is an independent digital service assistance platform that guides and assists users with online form submissions, portal registrations, documentation, and digital application processes. <strong>HOMline is NOT a government agency or official department.</strong></p>

            <h3>3. Service Disclaimer & Decision Authority</h3>
            <p>HOMline provides technical and operational assistance for supported online applications. Final approval, eligibility determination, issuance, timelines, and legal validity of any document or service remain exclusively with the respective official government authority, educational institution, or third-party service provider.</p>
            '''
        },
        'privacy': {
            'title': 'Privacy Policy',
            'content': '''
            <h3>1. Data Collection</h3>
            <p>HOMline DIGI seva collects personal details such as name, contact number, email address, and uploaded documents strictly for fulfilling your requested online service.</p>
            <h3>2. Data Confidentiality</h3>
            <p>We treat all customer documents and sensitive information with high confidentiality and appropriate security measures.</p>
            '''
        },
        'refund': {
            'title': 'Refund Policy',
            'content': '''
            <h3>1. Service Charge Refund</h3>
            <p>HOMline service fees cover assistance and processing work. If a request is cancelled before processing has initiated, a refund may be granted.</p>
            '''
        },
        'cancellation': {
            'title': 'Cancellation Policy',
            'content': '''
            <h3>1. Request Cancellation</h3>
            <p>Customers can request cancellation by calling 6282268453 or via WhatsApp before application submission.</p>
            '''
        },
        'data-protection': {
            'title': 'Data Protection & Confidentiality',
            'content': '''
            <h3>1. Security Practices</h3>
            <p>HOMline employs encrypted digital transmission and verified support staff for identity protection.</p>
            '''
        },
        'disclaimer': {
            'title': 'Service Disclaimer',
            'content': '''
            <div class="alert alert-warning p-4 rounded-3">
                <h5 class="fw-bold mb-2"><i class="bi bi-exclamation-triangle-fill me-2"></i>Official Notice & Disclaimer</h5>
                <p class="mb-0">HOMline DIGI seva provides digital assistance and guidance for supported online services. Availability, processing time, eligibility, approval and final decisions are determined solely by the respective government authority, board, institution or third-party service provider.</p>
            </div>
            '''
        }
    }

    policy_data = policies.get(policy_name, policies['disclaimer'])
    return render(request, 'core/policy.html', {'policy': policy_data, 'policy_name': policy_name})
