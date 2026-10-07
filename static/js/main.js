// HOMline DIGI seva - Master Interactive Main JS

document.addEventListener('DOMContentLoaded', function () {
  console.log('HOMline DIGI seva initialized.');

  // 1. Instant Track Request via AJAX
  const trackFormAjax = document.getElementById('trackFormAjax');
  const trackResultContainer = document.getElementById('trackResultContainer');

  if (trackFormAjax) {
    trackFormAjax.addEventListener('submit', function (e) {
      e.preventDefault();
      const requestIdInput = document.getElementById('ajaxRequestIdInput');
      const reqId = requestIdInput ? requestIdInput.value.trim() : '';

      if (!reqId) return;

      trackResultContainer.innerHTML = `
        <div class="text-center p-4">
          <div class="spinner-border text-teal" role="status">
            <span class="visually-hidden">Searching...</span>
          </div>
          <p class="mt-2 text-muted">Locating your request ID: <strong>${reqId}</strong>...</p>
        </div>
      `;

      fetch(`/track/${encodeURIComponent(reqId)}/?json=1`, {
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.found) {
          let badgeClass = 'bg-warning text-dark';
          if (data.status === 'Completed') badgeClass = 'bg-success text-white';
          if (data.status === 'Processing') badgeClass = 'bg-info text-dark';
          if (data.status === 'Cancelled') badgeClass = 'bg-danger text-white';

          let timelineHtml = '';
          if (data.timeline && data.timeline.length > 0) {
            timelineHtml = `
              <div class="mt-4 pt-3 border-top">
                <h6 class="fw-bold text-navy mb-3"><i class="bi bi-clock-history text-teal me-1"></i> Activity History Logs:</h6>
                <div class="border-start border-2 border-teal ps-3 ms-2">
                  ${data.timeline.map(log => `
                    <div class="mb-2">
                      <div class="d-flex align-items-center gap-2">
                        <span class="badge bg-teal text-white font-monospace" style="font-size:0.7rem;">${log.status}</span>
                        <strong class="text-navy small">${log.title}</strong>
                        <span class="text-muted font-monospace ms-auto" style="font-size:0.72rem;">${log.date}</span>
                      </div>
                      ${log.description ? `<p class="text-muted small mb-0 mt-1">${log.description}</p>` : ''}
                    </div>
                  `).join('')}
                </div>
              </div>
            `;
          }

          trackResultContainer.innerHTML = `
            <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
              <div class="card-header bg-navy text-white p-3 d-flex justify-content-between align-items-center">
                <div>
                  <h6 class="mb-0 text-white font-brand">Request ID: ${data.request_id}</h6>
                  <small class="text-white-50">Submitted: ${data.created_at}</small>
                </div>
                <div class="d-flex align-items-center gap-2">
                  <span class="badge ${badgeClass} px-3 py-2 rounded-pill fs-6">${data.status}</span>
                  <a href="/receipt/${data.request_id}/" target="_blank" class="btn btn-sm btn-gold font-monospace fw-bold">
                    <i class="bi bi-printer-fill me-1"></i> PDF Slip
                  </a>
                </div>
              </div>
              <div class="card-body p-4">
                <div class="row g-3 mb-3">
                  <div class="col-md-6">
                    <span class="text-muted small d-block">Customer Name</span>
                    <strong class="text-navy fs-6">${data.name}</strong>
                  </div>
                  <div class="col-md-6">
                    <span class="text-muted small d-block">Requested Service</span>
                    <strong class="text-navy fs-6">${data.service}</strong>
                  </div>
                </div>
                <div class="p-3 bg-light rounded-3 border-start border-4 border-teal mb-3">
                  <span class="text-muted small d-block fw-semibold mb-1">HOMline Status Note:</span>
                  <p class="mb-0 text-dark font-monospace fs-6">${data.notes}</p>
                </div>
                ${timelineHtml}
                <div class="d-flex justify-content-between align-items-center text-muted small mt-3 pt-2 border-top">
                  <span>Last Updated: ${data.updated_at}</span>
                  <a href="https://wa.me/916282268453?text=Hi%20HOMline,%20I%20have%20an%20enquiry%20regarding%20Request%20ID%20${data.request_id}" target="_blank" class="btn btn-sm btn-whatsapp">
                    <i class="bi bi-whatsapp me-1"></i> WhatsApp Support
                  </a>
                </div>
              </div>
            </div>
          `;
        } else {
          trackResultContainer.innerHTML = `
            <div class="alert alert-danger rounded-3 p-3">
              <i class="bi bi-exclamation-circle-fill me-2"></i> ${data.error || 'No record found with this Request ID.'}
            </div>
          `;
        }
      })
      .catch(err => {
        console.error(err);
        trackResultContainer.innerHTML = `
          <div class="alert alert-danger rounded-3 p-3">
            <i class="bi bi-wifi-off me-2"></i> Unable to connect to HOMline tracking server. Please try again or contact WhatsApp support at 6282268453.
          </div>
        `;
      });
    });
  }

  // 2. Interactive Service Fee Estimator Calculator
  const calcServiceSelect = document.getElementById('calcServiceSelect');
  const calcPriorityMode = document.getElementById('calcPriorityMode');
  const calcDeliveryMode = document.getElementById('calcDeliveryMode');
  
  function updateFeeCalculation() {
    if (!calcServiceSelect) return;
    const selectedOption = calcServiceSelect.options[calcServiceSelect.selectedIndex];
    const baseHomlineFee = parseInt(selectedOption.getAttribute('data-homline-fee') || '200');
    const thirdPartyFee = selectedOption.getAttribute('data-third-fee') || 'As per Govt portal';
    
    let priorityAdd = 0;
    if (calcPriorityMode && calcPriorityMode.value === 'express') priorityAdd = 100;

    let deliveryAdd = 0;
    if (calcDeliveryMode && calcDeliveryMode.value === 'home_print') deliveryAdd = 50;

    const totalHomlineCharge = baseHomlineFee + priorityAdd + deliveryAdd;

    const outputHomline = document.getElementById('calcOutputHomline');
    const outputThird = document.getElementById('calcOutputThird');
    const outputTotal = document.getElementById('calcOutputTotal');

    if (outputHomline) outputHomline.innerText = `₹${totalHomlineCharge}`;
    if (outputThird) outputThird.innerText = thirdPartyFee;
    if (outputTotal) outputTotal.innerText = `₹${totalHomlineCharge} + (${thirdPartyFee})`;
  }

  if (calcServiceSelect) {
    calcServiceSelect.addEventListener('change', updateFeeCalculation);
    if (calcPriorityMode) calcPriorityMode.addEventListener('change', updateFeeCalculation);
    if (calcDeliveryMode) calcDeliveryMode.addEventListener('change', updateFeeCalculation);
    updateFeeCalculation();
  }

  // 3. Floating WhatsApp Smart Assistant Toggle
  const waTrigger = document.getElementById('waAssistantTrigger');
  const waBox = document.getElementById('waAssistantBox');
  const waClose = document.getElementById('waAssistantClose');

  if (waTrigger && waBox) {
    waTrigger.addEventListener('click', function () {
      waBox.classList.toggle('active');
    });
    if (waClose) {
      waClose.addEventListener('click', function () {
        waBox.classList.remove('active');
      });
    }
  }

  // 4. Auto pre-select service in Modal / Request page
  const requestModal = document.getElementById('requestModal');
  if (requestModal) {
    requestModal.addEventListener('show.bs.modal', function (event) {
      const button = event.relatedTarget;
      if (button) {
        const serviceId = button.getAttribute('data-bs-service-id');
        const serviceSelect = document.getElementById('serviceSelect');
        if (serviceSelect && serviceId) {
          serviceSelect.value = serviceId;
        }
      }
    });
  }
});

// Quick WhatsApp Message Sender Function
function sendCustomWhatsAppMessage(presetText) {
  const customInput = document.getElementById('waCustomMessageInput');
  let textToSend = presetText;
  if (!textToSend && customInput) {
    textToSend = customInput.value.trim();
  }
  if (!textToSend) textToSend = "Hi HOMline, I would like to enquire about digital assistance.";
  
  const waUrl = `https://wa.me/916282268453?text=${encodeURIComponent(textToSend)}`;
  window.open(waUrl, '_blank');
}
