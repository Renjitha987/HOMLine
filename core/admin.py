import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import (
    Category, Service, Update, MembershipPlan, 
    MembershipEnquiry, ServiceRequest, ServiceRequestLog, FAQ, CustomerReview
)

def export_requests_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="homline_service_requests.csv"'
    writer = csv.writer(response)
    writer.writerow(['Request ID', 'Full Name', 'Mobile', 'Email', 'Service', 'Status', 'Preference', 'Created At'])
    for obj in queryset:
        writer.writerow([
            obj.request_id,
            obj.full_name,
            obj.mobile,
            obj.email or '',
            obj.get_service_title(),
            obj.status,
            obj.contact_preference,
            obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    return response

export_requests_csv.short_description = "Export Selected Requests to CSV"


class ServiceRequestLogInline(admin.TabularInline):
    model = ServiceRequestLog
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'icon_class')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'homline_charge', 'third_party_fee', 'is_featured')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'short_summary', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_tag', 'published_at', 'is_featured')
    list_filter = ('category_tag', 'is_featured')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_popular', 'order')
    list_editable = ('is_popular', 'order')


@admin.register(MembershipEnquiry)
class MembershipEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'email', 'preferred_plan', 'created_at')
    list_filter = ('preferred_plan', 'created_at')
    search_fields = ('name', 'mobile', 'email')


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'full_name', 'mobile', 'get_service_title', 'status', 'contact_preference', 'created_at')
    list_filter = ('status', 'contact_preference', 'created_at')
    search_fields = ('request_id', 'full_name', 'mobile', 'email', 'requirement_details')
    list_editable = ('status',)
    inlines = [ServiceRequestLogInline]
    actions = [export_requests_csv]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order')
    list_filter = ('category',)
    search_fields = ('question', 'answer')
    list_editable = ('order',)


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'service_used', 'rating', 'is_verified', 'created_at')
    list_filter = ('rating', 'is_verified')
