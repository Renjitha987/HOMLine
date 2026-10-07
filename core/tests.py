from django.test import TestCase, Client
from django.urls import reverse
from core.models import Category, Service, Update, MembershipPlan, FAQ, CustomerReview, ServiceRequest

class HOMlineProjectTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.category = Category.objects.create(
            name="Government & Identity",
            slug="government-identity",
            description="Gov services",
            icon_class="bi-card-heading",
            order=1
        )

        self.service = Service.objects.create(
            category=self.category,
            title="PAN Card New",
            slug="pan-card-new",
            short_summary="Apply for PAN",
            description="Detailed description for PAN card",
            required_documents="Aadhaar, Photo",
            homline_charge="₹150",
            third_party_fee="₹107",
            processing_time="2-3 days",
            is_featured=True,
            badge="Popular",
            icon_class="bi-credit-card"
        )

        self.update = Update.objects.create(
            title="Service Launch Notice",
            slug="service-launch-notice",
            category_tag="Service Update",
            summary="New features online",
            content="Full update notice text",
            is_featured=True
        )

        self.plan = MembershipPlan.objects.create(
            name="Basic Member",
            tagline="Essential support",
            price="₹299 / year",
            is_popular=True,
            features="Feature 1\nFeature 2",
            welcome_benefits="Benefit 1",
            order=1
        )

        self.faq = FAQ.objects.create(
            question="What is HOMline?",
            answer="Digital service assistance platform.",
            category="General",
            order=1
        )

        self.review = CustomerReview.objects.create(
            customer_name="Test Customer",
            location="Kochi",
            rating=5,
            service_used="PAN Card",
            review_text="Great service!",
            is_verified=True
        )

        self.service_request = ServiceRequest.objects.create(
            request_id="HOM-2026-TEST",
            full_name="Test User",
            mobile="6282268453",
            email="test@example.com",
            service=self.service,
            requirement_details="Needs PAN card",
            contact_preference="WhatsApp",
            status="Processing",
            admin_notes="Assigned to agent"
        )

    def test_homepage(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "DIGITAL SERVICES.")
        self.assertContains(response, "6282268453")

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About HOMline DIGI seva")

    def test_services_list_page(self):
        response = self.client.get(reverse('services_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PAN Card New")

    def test_service_detail_page(self):
        response = self.client.get(reverse('service_detail', kwargs={'slug': self.service.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PAN Card New")
        self.assertContains(response, "Required Service Disclaimer")

    def test_how_it_works_page(self):
        response = self.client.get(reverse('how_it_works'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "How HOMline Works")

    def test_membership_page(self):
        response = self.client.get(reverse('membership'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Basic Member")

    def test_updates_list_page(self):
        response = self.client.get(reverse('updates_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Service Launch Notice")

    def test_update_detail_page(self):
        response = self.client.get(reverse('update_detail', kwargs={'slug': self.update.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Service Launch Notice")

    def test_faqs_page(self):
        response = self.client.get(reverse('faqs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "What is HOMline?")

    def test_contact_page(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "6282268453")

    def test_track_request_page(self):
        response = self.client.get(reverse('track_request_with_id', kwargs={'request_id': 'HOM-2026-TEST'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HOM-2026-TEST")

    def test_track_request_ajax(self):
        response = self.client.get(reverse('track_request_with_id', kwargs={'request_id': 'HOM-2026-TEST'}), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data['found'])
        self.assertEqual(json_data['request_id'], 'HOM-2026-TEST')

    def test_receipt_page(self):
        response = self.client.get(reverse('receipt', kwargs={'request_id': 'HOM-2026-TEST'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "VERIFIED ACKNOWLEDGEMENT")

    def test_policy_page(self):
        response = self.client.get(reverse('policy', kwargs={'policy_name': 'disclaimer'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Official Notice & Disclaimer")

