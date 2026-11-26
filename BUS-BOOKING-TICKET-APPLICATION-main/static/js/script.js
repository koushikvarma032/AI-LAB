/**
 * RuleBus - Frontend JavaScript
 * Handles interactive seat selection, live RBP fare calculations, and modal management.
 */

document.addEventListener('DOMContentLoaded', () => {

    // ==========================================
    // 1. Mobile Menu Toggle
    // ==========================================
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const navLinks = document.querySelector('.nav-links');
    if (mobileMenuToggle && navLinks) {
        mobileMenuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }

    // ==========================================
    // 2. Interactive Seat Selection (seats.html)
    // ==========================================
    const seatGrid = document.getElementById('seatGrid');
    if (seatGrid) {
        const requiredPassengers = parseInt(document.querySelector('input[name="passengers_count"]')?.value || 1);
        const selectedSeatsInput = document.getElementById('selectedSeatsInput');
        const selectedSeatsText = document.getElementById('selectedSeatsText');
        const selectedCountText = document.getElementById('selectedCountText');
        const submitSeatsBtn = document.getElementById('submitSeatsBtn');
        let selectedSeats = [];

        seatGrid.addEventListener('click', (e) => {
            const seatBtn = e.target.closest('.seat-btn');
            if (!seatBtn || seatBtn.classList.contains('booked')) return;

            const seatNum = seatBtn.getAttribute('data-seat');

            if (seatBtn.classList.contains('selected')) {
                // Deselect
                seatBtn.classList.remove('selected');
                selectedSeats = selectedSeats.filter(s => s !== seatNum);
            } else {
                // Select if within limit
                if (selectedSeats.length >= requiredPassengers) {
                    alert(`You can only select up to ${requiredPassengers} seat(s) for this booking.`);
                    return;
                }
                seatBtn.classList.add('selected');
                selectedSeats.push(seatNum);
            }

            // Update UI & Hidden Form Inputs
            selectedSeatsInput.value = selectedSeats.join(',');
            selectedCountText.innerText = selectedSeats.length;

            if (selectedSeats.length > 0) {
                selectedSeatsText.innerText = selectedSeats.join(', ');
            } else {
                selectedSeatsText.innerText = 'None';
            }

            if (selectedSeats.length === requiredPassengers) {
                submitSeatsBtn.disabled = false;
            } else {
                submitSeatsBtn.disabled = true;
            }
        });
    }

    // ==========================================
    // 3. Live Rule Engine Fare Preview (passenger.html)
    // ==========================================
    const passengerForm = document.getElementById('passengerDetailsForm');
    if (passengerForm && window.BUS_BASE_FARE) {

        function calculateLiveFare() {
            const ageInputs = document.querySelectorAll('.passenger-age');
            const passengers = [];

            ageInputs.forEach((input, index) => {
                const ageVal = parseInt(input.value) || 0;
                passengers.push({ age: ageVal });

                // Update individual age badge text on card
                const badge = document.getElementById(`ageBadge-${index}`);
                if (badge) {
                    if (ageVal < 5) {
                        badge.innerText = "Infant Free Ticket (100% Off)";
                        badge.className = "age-rule-badge badge badge-success";
                    } else if (ageVal >= 5 && ageVal <= 12) {
                        badge.innerText = "Child Discount (50% Off)";
                        badge.className = "age-rule-badge badge badge-success";
                    } else if (ageVal >= 60) {
                        badge.innerText = "Senior Discount (10% Off)";
                        badge.className = "age-rule-badge badge badge-success";
                    } else {
                        badge.innerText = "Standard Fare";
                        badge.className = "age-rule-badge badge badge-secondary";
                    }
                }
            });

            // Call Flask RBP API for exact rule evaluation
            fetch('/api/calculate-fare', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    base_fare: window.BUS_BASE_FARE,
                    passengers: passengers,
                    travel_date: window.TRAVEL_DATE
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    const summary = data.fare_summary;
                    
                    // Update Breakdown Elements
                    document.getElementById('liveBaseTotal').innerText = `₹${summary.raw_total_base.toFixed(2)}`;
                    
                    const ageRow = document.getElementById('liveAgeDiscountsRow');
                    if (summary.total_age_discounts > 0) {
                        ageRow.style.display = 'flex';
                        document.getElementById('liveAgeDiscounts').innerText = `-₹${summary.total_age_discounts.toFixed(2)}`;
                    } else {
                        ageRow.style.display = 'none';
                    }

                    const groupRow = document.getElementById('liveGroupDiscountRow');
                    if (summary.group_discount > 0) {
                        groupRow.style.display = 'flex';
                        document.getElementById('liveGroupDiscount').innerText = `-₹${summary.group_discount.toFixed(2)}`;
                    } else {
                        groupRow.style.display = 'none';
                    }

                    const weekendRow = document.getElementById('liveWeekendRow');
                    if (summary.weekend_surcharge > 0) {
                        weekendRow.style.display = 'flex';
                        document.getElementById('liveWeekendSurcharge').innerText = `+₹${summary.weekend_surcharge.toFixed(2)}`;
                    } else {
                        weekendRow.style.display = 'none';
                    }

                    document.getElementById('liveFinalTotal').innerText = `₹${summary.final_total.toFixed(2)}`;

                    // Render Executed Rule Logs
                    const ruleLogsContainer = document.getElementById('liveRuleLogs');
                    if (ruleLogsContainer) {
                        ruleLogsContainer.innerHTML = '';
                        data.rule_logs.forEach(log => {
                            const li = document.createElement('li');
                            li.className = `rule-pill ${log.triggered ? 'pass' : 'info'}`;
                            li.innerHTML = `<i class="fa-solid fa-check"></i> <strong>${log.rule_name}:</strong> ${log.message}`;
                            ruleLogsContainer.appendChild(li);
                        });
                    }
                }
            })
            .catch(err => console.error("Error calculating live fare:", err));
        }

        // Attach event listeners to all age inputs
        document.querySelectorAll('.passenger-age').forEach(input => {
            input.addEventListener('input', calculateLiveFare);
            input.addEventListener('change', calculateLiveFare);
        });

        // Trigger initial calculation
        calculateLiveFare();
    }

    // ==========================================
    // 4. Cancellation Modal (bookings.html)
    // ==========================================
    const cancelModal = document.getElementById('cancelModal');
    if (cancelModal) {
        const modalCloseBtn = document.getElementById('closeModalBtn');
        const modalCancelClose = document.getElementById('cancelModalClose');
        const refundEvalBox = document.getElementById('refundEvalBox');
        const confirmCancelForm = document.getElementById('confirmCancelForm');
        const confirmCancelBtn = document.getElementById('confirmCancelBtn');

        function closeModal() {
            cancelModal.classList.remove('active');
        }

        if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeModal);
        if (modalCancelClose) modalCancelClose.addEventListener('click', closeModal);

        document.querySelectorAll('.open-cancel-modal').forEach(btn => {
            btn.addEventListener('click', () => {
                const bookingId = btn.getAttribute('data-booking-id');
                const busName = btn.getAttribute('data-bus-name');
                const route = btn.getAttribute('data-route');
                const travelDate = btn.getAttribute('data-date');
                const depTime = btn.getAttribute('data-time');
                const amount = parseFloat(btn.getAttribute('data-amount'));

                document.getElementById('modalBookingId').innerText = bookingId;
                confirmCancelForm.action = `/cancel-booking/${bookingId}`;
                cancelModal.classList.add('active');

                refundEvalBox.innerHTML = `
                    <div class="text-center py-3">
                        <i class="fa-solid fa-spinner fa-spin fa-2x"></i>
                        <p class="mt-2">Evaluating Cancellation Rules...</p>
                    </div>
                `;

                // Request Cancellation Evaluation API
                fetch('/api/evaluate-cancellation', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        booking_id: bookingId,
                        total_amount: amount,
                        travel_date: travelDate,
                        departure_time: depTime
                    })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'success') {
                        const evalData = data.cancellation_eval;
                        const log = evalData.rule_logs[0];

                        refundEvalBox.innerHTML = `
                            <div class="card p-3 bg-light">
                                <div class="d-flex justify-content-between mb-2">
                                    <span>Departure Status:</span>
                                    <strong>${evalData.hours_remaining} hrs until departure</strong>
                                </div>
                                <div class="d-flex justify-content-between mb-2">
                                    <span>Triggered Rule Tier:</span>
                                    <span class="badge badge-info">${log.status}</span>
                                </div>
                                <hr class="my-2">
                                <div class="d-flex justify-content-between mb-1">
                                    <span>Original Ticket Amount:</span>
                                    <span>₹${amount.toFixed(2)}</span>
                                </div>
                                <div class="d-flex justify-content-between mb-1 text-danger">
                                    <span>Cancellation Fee (${100 - evalData.refund_percentage}%):</span>
                                    <span>-₹${evalData.cancellation_fee.toFixed(2)}</span>
                                </div>
                                <div class="d-flex justify-content-between font-weight-bold text-success font-size-lg mt-2">
                                    <span>Refund Amount (${evalData.refund_percentage}%):</span>
                                    <span>₹${evalData.refund_amount.toFixed(2)}</span>
                                </div>
                                <code class="d-block mt-3 p-2 bg-white border rounded">${log.condition} → ${log.message}</code>
                            </div>
                        `;

                        confirmCancelBtn.disabled = false;
                    }
                })
                .catch(err => {
                    refundEvalBox.innerHTML = `<div class="alert alert-danger">Error evaluating cancellation rules.</div>`;
                });
            });
        });
    }
});
