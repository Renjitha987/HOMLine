import uuid
from django.db import models
from django.utils.text import slugify

def generate_request_id():
    return f"HOM-2026-{uuid.uuid4().hex[:6].upper()}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=50, default="bi-grid", help_text="Bootstrap icon class e.g. bi-shield-check")
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    short_summary = models.TextField()
    description = models.TextField()
    required_documents = models.TextField(help_text="Line separated or bullet points of required documents")
    homline_charge = models.CharField(max_length=100, default="₹150 - ₹300", help_text="HOMline service charge")
    third_party_fee = models.CharField(max_length=150, default="As per Government / Official portal rates", help_text="Third-party / Application fee")
    processing_time = models.CharField(max_length=100, default="2 - 5 Working Days")
    is_featured = models.BooleanField(default=True)
    badge = models.CharField(max_length=50, blank=True, help_text="e.g. Popular, Essential, Fast Track")
    icon_class = models.CharField(max_length=50, default="bi-file-earmark-check")

    class Meta:
        ordering = ['category', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Update(models.Model):
    TAG_CHOICES = [
        ('Service Update', 'Service Update'),
        ('Important Notice', 'Important Notice'),
        ('Service Availability Update', 'Service Availability Update'),
        ('General News', 'General News'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category_tag = models.CharField(max_length=50, choices=TAG_CHOICES, default='Service Update')
    summary = models.TextField()
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=True, help_text="Show on Homepage top 3 updates")

    class Meta:
        ordering = ['-published_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200)
    price = models.CharField(max_length=50, help_text="e.g. ₹499 / year")
    is_popular = models.BooleanField(default=False)
    features = models.TextField(help_text="One feature per line")
    welcome_benefits = models.TextField(help_text="One welcome benefit per line")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name

    def get_features_list(self):
        return [f.strip() for f in self.features.split('\n') if f.strip()]

    def get_welcome_benefits_list(self):
        return [b.strip() for b in self.welcome_benefits.split('\n') if b.strip()]


class MembershipEnquiry(models.Model):
    name = models.CharField(max_length=120)
    mobile = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    preferred_plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Enquiry from {self.name} - {self.mobile}"


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Under Review', 'Under Review'),
        ('Processing', 'Processing'),
        ('Information Required', 'Information Required'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    CONTACT_CHOICES = [
        ('WhatsApp', 'WhatsApp'),
        ('Call', 'Call'),
        ('Email', 'Email'),
    ]

    request_id = models.CharField(max_length=20, unique=True, default=generate_request_id)
    full_name = models.CharField(max_length=120)
    mobile = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    service_name_manual = models.CharField(max_length=150, blank=True, help_text="Used if custom service requested")
    requirement_details = models.TextField()
    contact_preference = models.CharField(max_length=20, choices=CONTACT_CHOICES, default='WhatsApp')
    document_upload = models.FileField(upload_to='service_docs/%Y/%m/', blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    admin_notes = models.TextField(blank=True, help_text="Notes visible or status updates")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.request_id} - {self.full_name} ({self.status})"

    def get_service_title(self):
        if self.service:
            return self.service.title
        return self.service_name_manual or "General Digital Assistance"


class ServiceRequestLog(models.Model):
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='timeline_logs')
    status = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Log [{self.status}] for {self.request.request_id}"


class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('General', 'General'),
        ('Fees & Charges', 'Fees & Charges'),
        ('Processing & Approvals', 'Processing & Approvals'),
        ('Privacy & Safety', 'Privacy & Safety'),
    ]

    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='General')
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['order', 'id']

    def __str__(self):
        return self.question


class CustomerReview(models.Model):
    customer_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, default="Kerala, India")
    rating = models.IntegerField(default=5)
    service_used = models.CharField(max_length=150)
    review_text = models.TextField()
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.customer_name}"
