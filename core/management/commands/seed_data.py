from django.core.management.base import BaseCommand
from core.models import (
    Category, Service, Update, MembershipPlan, 
    FAQ, CustomerReview, ServiceRequest
)

class Command(BaseCommand):
    help = 'Seeds database with realistic initial data for HOMline DIGI seva'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # 1. Categories
        cat_gov, _ = Category.objects.get_or_create(
            slug='government-identity',
            defaults={
                'name': 'Government & Identity',
                'description': 'PAN, passport-related, voter-related and other supported government services',
                'icon_class': 'bi-card-heading',
                'order': 1
            }
        )

        cat_edu, _ = Category.objects.get_or_create(
            slug='education',
            defaults={
                'name': 'Education',
                'description': 'Applications, results, certificates, registrations and student support',
                'icon_class': 'bi-mortarboard-fill',
                'order': 2
            }
        )

        cat_biz, _ = Category.objects.get_or_create(
            slug='business-professional',
            defaults={
                'name': 'Business & Professional',
                'description': 'Online registrations, documentation and supported business services',
                'icon_class': 'bi-briefcase-fill',
                'order': 3
            }
        )

        cat_digi, _ = Category.objects.get_or_create(
            slug='digital-online',
            defaults={
                'name': 'Digital & Online',
                'description': 'Online forms, registrations, portal assistance and digital services',
                'icon_class': 'bi-globe2',
                'order': 4
            }
        )

        cat_doc, _ = Category.objects.get_or_create(
            slug='document-application',
            defaults={
                'name': 'Document & Application',
                'description': 'Guidance and assistance for supported online applications',
                'icon_class': 'bi-file-earmark-text-fill',
                'order': 5
            }
        )

        self.stdout.write(self.style.SUCCESS('Created 5 Categories.'))

        # 2. Services
        services_data = [
            # Gov & Identity
            {
                'category': cat_gov,
                'title': 'PAN Card (New / Correction / Update)',
                'slug': 'pan-card-services',
                'short_summary': 'Hassle-free application for fresh PAN allocation, data corrections, name change or duplicate reprint.',
                'description': 'HOMline assists you in preparing and submitting your PAN card application through supported online portals. Whether you need a fresh PAN for employment/banking or corrections in existing details (Name, DOB, Address, Photo), we guide you through every step.',
                'required_documents': '• Proof of Identity (Aadhaar Card / Voter ID / Passport)\n• Proof of Address (Aadhaar / Utility Bill / Bank Statement)\n• Proof of Date of Birth (Birth Certificate / SSLC Marksheet)\n• 2 Passport Size Photos (for physical applications)',
                'homline_charge': '₹150 - ₹250',
                'third_party_fee': '₹107 (Standard Government Portal Fee)',
                'processing_time': '2 - 5 Working Days for e-PAN',
                'is_featured': True,
                'badge': 'Popular',
                'icon_class': 'bi-credit-card-2-front-fill'
            },
            {
                'category': cat_gov,
                'title': 'Passport Online Application & Appointment',
                'slug': 'passport-application-assistance',
                'short_summary': 'Complete assistance for fresh passport, re-issue, address update and PSK appointment booking.',
                'description': 'Navigating Passport Seva portals can be complex. HOMline provides end-to-end guidance for fresh applications, passport renewals, Tatkaal requests, and slot booking at nearest Passport Seva Kendra (PSK).',
                'required_documents': '• Aadhaar Card (with updated mobile number)\n• Proof of Birth (Birth Certificate / School Leaving Cert)\n• Proof of Residence (Voter Card / Bank Passbook / Electricity Bill)\n• Existing Passport copy (for re-issue / renewal)',
                'homline_charge': '₹300 - ₹500',
                'third_party_fee': '₹1,500 (Fresh/Normal) / ₹2,000 (Tatkal)',
                'processing_time': 'Appointment slot booked within 24-48 hrs',
                'is_featured': True,
                'badge': 'Essential',
                'icon_class': 'bi-passport-fill'
            },
            {
                'category': cat_gov,
                'title': 'Voter ID Card Services',
                'slug': 'voter-id-services',
                'short_summary': 'Form 6 new registration, constituency transfer, address change & digital EPIC download.',
                'description': 'Complete guidance for voter registration on the National Voters Service Portal (NVSP). We assist with Form 6 (New Voter), Form 8 (Correction & Address Change), and e-EPIC digital voter card downloads.',
                'required_documents': '• Aadhaar Card / Identity Proof\n• Proof of Address (Ration Card / Rent Agreement / Electricity Bill)\n• Passport size photograph',
                'homline_charge': '₹100 - ₹200',
                'third_party_fee': 'Free / Minimal Portal Charge',
                'processing_time': '3 - 7 Working Days',
                'is_featured': False,
                'badge': '',
                'icon_class': 'bi-person-badge-fill'
            },

            # Education
            {
                'category': cat_edu,
                'title': 'Academic Exam & Admission Registrations',
                'slug': 'academic-exam-registrations',
                'short_summary': 'Guided registration and online form submission for entrance exams, universities & boards.',
                'description': 'Avoid costly form errors during high-stakes entrance exam registrations (CUET, NEET, KEAM, PSC exams, University admissions). HOMline helps you upload correct document formats and complete submissions accurately.',
                'required_documents': '• 10th & 12th Marksheets / Certificates\n• Caste / Category Certificate (if applicable)\n• Passport size photo & signature scan\n• Valid Mobile & Email ID',
                'homline_charge': '₹150 - ₹300',
                'third_party_fee': 'As per respective board/university exam fee',
                'processing_time': 'Same Day Processing',
                'is_featured': True,
                'badge': 'High Demand',
                'icon_class': 'bi-journal-bookmark-fill'
            },
            {
                'category': cat_edu,
                'title': 'Student Scholarship Portal Assistance',
                'slug': 'scholarship-portal-assistance',
                'short_summary': 'Online application guidance for State, National Scholarship Portal (NSP) & private grants.',
                'description': 'Step-by-step assistance for eligible students applying for National Scholarship Portal (NSP), State Minority Scholarships, Post-Matric grants, and Merit awards.',
                'required_documents': '• Student Aadhaar & Bank Passbook\n• Income Certificate & Caste Certificate\n• Current Fee Receipt & Previous Mark List\n• Institution Verification Form',
                'homline_charge': '₹150 - ₹250',
                'third_party_fee': 'Free (NSP & Govt Portals)',
                'processing_time': '1 - 3 Working Days',
                'is_featured': False,
                'badge': '',
                'icon_class': 'bi-mortarboard'
            },

            # Business & Professional
            {
                'category': cat_biz,
                'title': 'Udyam MSME & FSSAI Registration',
                'slug': 'udyam-msme-fssai-registration',
                'short_summary': 'Government MSME recognition & Food License (FSSAI) application guidance for small businesses.',
                'description': 'Set up your enterprise with official Udyam MSME registration and FSSAI basic food license online assistance. HOMline ensures proper documentation so your shop or business can access credit & benefits.',
                'required_documents': '• Aadhaar & PAN of Proprietor/Partners\n• Business Address Proof (Electricity Bill / Rent Deed)\n• Business Name & Category Details\n• Bank Account details',
                'homline_charge': '₹250 - ₹450',
                'third_party_fee': '₹100 (FSSAI 1 Yr Basic) / ₹0 (Udyam Govt portal)',
                'processing_time': '2 - 4 Working Days',
                'is_featured': True,
                'badge': 'Business',
                'icon_class': 'bi-building-check'
            },

            # Digital & Online
            {
                'category': cat_digi,
                'title': 'Digital Certificates & Online Downloads',
                'slug': 'digital-certificates-download',
                'short_summary': 'Assistance downloading Income, Caste, Relationship & Domicile e-Certificates.',
                'description': 'Easily apply for or retrieve state revenue e-Certificates (Income, Caste, Native, Valuation) through e-District portals with full assistance from HOMline.',
                'required_documents': '• Ration Card / Aadhaar\n• Village Office / Local Authority details\n• Application reference number (for tracking)',
                'homline_charge': '₹100 - ₹200',
                'third_party_fee': '₹15 - ₹30 (e-District Fee)',
                'processing_time': '3 - 7 Working Days (Subject to Village Office approval)',
                'is_featured': False,
                'badge': '',
                'icon_class': 'bi-file-earmark-lock-fill'
            },

            # Document & Application
            {
                'category': cat_doc,
                'title': 'Document Formatting & Size Optimization',
                'slug': 'document-formatting-optimization',
                'short_summary': 'Professional scan, PDF conversion, image compression & portal upload formatting.',
                'description': 'Struggling with strict document upload dimensions (e.g. 50KB JPEG, specific resolution, merged PDF)? Send your files via WhatsApp to HOMline for precision formatting & compression.',
                'required_documents': '• Original document photos/scans via WhatsApp',
                'homline_charge': '₹50 - ₹100',
                'third_party_fee': 'None',
                'processing_time': 'Instant / 1 Hour',
                'is_featured': True,
                'badge': 'Fast',
                'icon_class': 'bi-aspect-ratio-fill'
            },
        ]

        for s_data in services_data:
            Service.objects.get_or_create(slug=s_data['slug'], defaults=s_data)

        self.stdout.write(self.style.SUCCESS(f'Created {len(services_data)} Services.'))

        # 3. Updates
        updates_data = [
            {
                'title': 'New Digital Assistance Services Added to HOMline Directory',
                'slug': 'new-digital-services-added',
                'category_tag': 'Service Update',
                'summary': 'We have expanded our catalog to support passport appointment bookings, Udyam MSME setup, and entrance exam form filling.',
                'content': 'HOMline DIGI seva is pleased to announce expanded support for essential digital applications. Customers can now request step-by-step assistance for Passport Seva Kendra appointments, FSSAI registration, and national scholarship portals directly from our home page or via WhatsApp.',
                'is_featured': True
            },
            {
                'title': 'Important Notice: Third-Party & Government Fee Transparency',
                'slug': 'important-notice-fee-transparency',
                'category_tag': 'Important Notice',
                'summary': 'HOMline maintains strict separation between our nominal service fee and official government charges.',
                'content': 'To ensure complete transparency, every service card on HOMline clearly distinguishes between the HOMline Service Charge (our assistance fee) and official Third-Party/Government Portal fees. Third-party fees are paid directly to respective authorities.',
                'is_featured': True
            },
            {
                'title': 'High-Volume Academic Registration Window - Fast-Track Slot Booking',
                'slug': 'academic-registration-window-update',
                'category_tag': 'Service Availability Update',
                'summary': 'Dedicated WhatsApp assistance line active for student admissions & scholarship applications.',
                'content': 'Due to upcoming university registration deadlines, our support team has enabled fast-track queue handling for students. Message us on WhatsApp 6282268453 for rapid document formatting and error-free portal submission.',
                'is_featured': True
            },
            {
                'title': 'HOMline Support Operating Hours & Holiday Schedule',
                'slug': 'homline-support-schedule-notice',
                'category_tag': 'General News',
                'summary': 'Submit online requests 24x7. Support team responds Monday to Saturday 9:00 AM - 8:00 PM.',
                'content': 'You can submit service requests and track your reference IDs on homline.com 24 hours a day, 7 days a week. Direct call and WhatsApp support is active Monday through Saturday from 9 AM to 8 PM IST.',
                'is_featured': False
            }
        ]

        for u_data in updates_data:
            Update.objects.get_or_create(slug=u_data['slug'], defaults=u_data)

        self.stdout.write(self.style.SUCCESS('Created 4 Updates.'))

        # 4. Membership Plans
        membership_data = [
            {
                'name': 'Basic Member',
                'tagline': 'Essential support for individuals needing regular digital assistance.',
                'price': '₹299 / year',
                'is_popular': False,
                'features': 'Priority queue for routine online requests\n10% discount on HOMline service charges\nFree document scan & compression formatting\nDirect WhatsApp dedicated line access',
                'welcome_benefits': '₹50 welcome voucher towards your first service request\nFree digital document storage guidance',
                'order': 1
            },
            {
                'name': 'Gold DIGI Member',
                'tagline': 'Complete digital coverage for families and frequent service users.',
                'price': '₹599 / year',
                'is_popular': True,
                'features': 'Highest priority handling for all applications\n25% discount on all HOMline service charges\nFree instant SMS & WhatsApp status alerts\nDedicated HOMline digital personal assistant\nCoverage for up to 4 family members',
                'welcome_benefits': '₹150 welcome credit voucher\n1 Free PAN / Certificate service assistance included',
                'order': 2
            },
            {
                'name': 'Premium Enterprise',
                'tagline': 'Tailored support for small businesses, shops, and institutions.',
                'price': '₹1,499 / year',
                'is_popular': False,
                'features': 'Unlimited business document formatting & compliance checks\n35% discount on all service assistance\nDedicated account manager & priority phone access\nMonthly service summary reports & portal monitoring',
                'welcome_benefits': '₹300 welcome credit voucher\nFree Udyam / MSME application guidance included',
                'order': 3
            },
        ]

        for m_data in membership_data:
            MembershipPlan.objects.get_or_create(name=m_data['name'], defaults=m_data)

        self.stdout.write(self.style.SUCCESS('Created 3 Membership Plans.'))

        # 5. FAQs
        faqs_data = [
            {
                'question': 'What is HOMline?',
                'answer': 'HOMline DIGI seva is an accessible digital service assistance platform that helps customers navigate, prepare, and submit supported online government, educational, business, and portal applications with ease.',
                'category': 'General',
                'order': 1
            },
            {
                'question': 'How can I request a service?',
                'answer': 'You can request a service in 3 easy ways: 1) Fill out our online Request Form on this website, 2) Send a message on WhatsApp to 6282268453, or 3) Call HOMline directly at 6282268453.',
                'category': 'General',
                'order': 2
            },
            {
                'question': 'Is HOMline available 24×7?',
                'answer': 'Yes! Requests and enquiries can be submitted online through our website 24 hours a day, 7 days a week. Response and processing depend on official portal hours and service type.',
                'category': 'General',
                'order': 3
            },
            {
                'question': 'How much does a service cost?',
                'answer': 'Each service clearly specifies the HOMline Service Charge (for our guidance & process support) and, where applicable, any separate official Application or Third-Party Fee determined by the respective provider.',
                'category': 'Fees & Charges',
                'order': 4
            },
            {
                'question': 'Do you guarantee approval?',
                'answer': 'No. HOMline provides expert application guidance and form filling. Eligibility, approval, processing timelines, and final decisions remain solely with the relevant government authority or third-party service provider.',
                'category': 'Processing & Approvals',
                'order': 5
            },
            {
                'question': 'Can I cancel my request?',
                'answer': 'Yes, cancellation and refund eligibility are subject to HOMline\'s applicable policies. If portal work has not commenced, service fee refunds can be issued.',
                'category': 'Fees & Charges',
                'order': 6
            },
            {
                'question': 'Are my documents safe?',
                'answer': 'Absolutely. HOMline strictly adheres to data protection and confidentiality best practices. Your personal documents are processed solely for your requested application and handled with maximum care.',
                'category': 'Privacy & Safety',
                'order': 7
            },
        ]

        for f_data in faqs_data:
            FAQ.objects.get_or_create(question=f_data['question'], defaults=f_data)

        self.stdout.write(self.style.SUCCESS('Created 7 FAQs.'))

        # 6. Customer Reviews
        reviews_data = [
            {
                'customer_name': 'Anish Kumar',
                'location': 'Kochi, Kerala',
                'rating': 5,
                'service_used': 'Passport Application Assistance',
                'review_text': 'HOMline made my passport renewal so simple! They verified my documents over WhatsApp and booked the PSK slot in just one day. Exceptional guidance.',
                'is_verified': True
            },
            {
                'customer_name': 'Dr. Mariamma Joseph',
                'location': 'Kottayam, Kerala',
                'rating': 5,
                'service_used': 'PAN Card Correction',
                'review_text': 'I was struggling with photo and DOB corrections on the NSDL portal. HOMline corrected the application and kept me informed at every step.',
                'is_verified': True
            },
            {
                'customer_name': 'Rahul Nair',
                'location': 'Thiruvananthapuram',
                'rating': 5,
                'service_used': 'CUET Exam Registration',
                'review_text': 'Very trustworthy and quick. They resized my documents to exact portal dimensions and submitted my exam form without any hassle. Highly recommended!',
                'is_verified': True
            },
            {
                'customer_name': 'Saji Varghese',
                'location': 'Thrissur',
                'rating': 5,
                'service_used': 'Udyam MSME License',
                'review_text': 'Got my shop registered under MSME within 48 hours. Transparent charges and polite customer support via WhatsApp.',
                'is_verified': True
            },
        ]

        for r_data in reviews_data:
            CustomerReview.objects.get_or_create(customer_name=r_data['customer_name'], defaults=r_data)

        self.stdout.write(self.style.SUCCESS('Created 4 Customer Reviews.'))

        # 7. Sample Service Request for instant testing
        sample_req, created = ServiceRequest.objects.get_or_create(
            request_id='HOM-2026-DEMO',
            defaults={
                'full_name': 'Sample Customer',
                'mobile': '6282268453',
                'email': 'customer@example.com',
                'service_name_manual': 'PAN Card Application',
                'requirement_details': 'New PAN card application with Aadhaar verification.',
                'contact_preference': 'WhatsApp',
                'status': 'Processing',
                'admin_notes': 'Document verified. Application submitted to official portal under acknowledgement receipt #9821734.'
            }
        )

        self.stdout.write(self.style.SUCCESS(f'Created sample tracking request with ID: HOM-2026-DEMO'))
        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
