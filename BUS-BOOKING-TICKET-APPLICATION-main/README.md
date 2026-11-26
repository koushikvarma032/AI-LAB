# RuleBus: Rule-Based Bus Ticket Booking System

A complete, working bus ticket booking application built using **Python Flask**, **SQLite**, and **HTML/CSS/JavaScript**, specifically created as a demonstration of **Rule-Based Programming (RBP)**.

---

## 1. Project Title
**RuleBus — Rule-Based Bus Ticket Booking System**

---

## 2. Problem Statement
Traditional bus booking systems often hardcode decision logic randomly across user interface scripts, making pricing rules, age discounts, and cancellation policies difficult to audit, maintain, or update. Moreover, students often confuse Rule-Based Systems with Machine Learning AI models.

There is a need for a clean, beginner-friendly transport booking application where **all business decisions are strictly driven by a modular Rule Engine** using predefined IF–THEN rules with complete transparency and execution logging.

---

## 3. Objective
- Demonstrate **Rule-Based Programming (RBP)** in a real-world web application.
- Show that complex business logic (pricing, discounts, seat capacity, status, refunds) can be executed **without Machine Learning / AI prediction models**.
- Provide a clean, modern, and fully functional Flask + SQLite web application for academic project submission and viva presentation.

---

## 4. What is Rule-Based Programming (RBP)?
**Rule-Based Programming** is a programming paradigm where system behavior and decision-making are defined using **predefined IF–THEN rules** evaluated by a **rule engine**.

Unlike Machine Learning:
- **No statistical guessing or training data**: Decisions are 100% deterministic based on explicit conditional logic.
- **Explainability**: Every outcome can be traced directly to the specific rule(s) triggered.
- **Modularity**: Rules can be modified, added, or removed independently without breaking UI components.

---

## 5. Why Bus Ticket Booking is a Good RBP Example
Bus ticketing involves multi-layered, conditional business logic:
- Seat capacity and conflict verification.
- Tiered passenger age pricing (Infants free, Child discounts, Senior citizen discounts).
- Volume / Group booking incentives (5% group discount for $\ge 4$ passengers).
- Date-dependent surcharges (Weekend travel surcharges).
- Departure time-based cancellation refund tiers ($>24\text{h} = 80\%$, $12\text{--}24\text{h} = 50\%$, $<12\text{h} = 0\%$).

All these requirements fit naturally into explicit `IF condition THEN action` rule evaluations.

---

## 6. Rules Implemented

### Seat Availability Rules (`rules/seat_rules.py`)
- **Rule S1**: `IF requested_seats <= available_seats` $\rightarrow$ Allow seat allocation.
- **Rule S2**: `IF requested_seats > available_seats` $\rightarrow$ Reject with *"Not enough seats available."*
- **Rule S3**: `IF selected_seat IN booked_seats` $\rightarrow$ Reject with *"Seat already booked."*

### Passenger Age Rules (`rules/fare_rules.py`)
- **Rule F1 (Infant)**: `IF age < 5` $\rightarrow$ 100% Free Ticket ($\text{Fare} = \text{₹}0$).
- **Rule F2 (Child)**: `IF age >= 5 AND age <= 12` $\rightarrow$ Apply 50% Child Discount.
- **Rule F3 (Senior)**: `IF age >= 60` $\rightarrow$ Apply 10% Senior Citizen Discount.
- **Rule F4 (Adult)**: `IF age > 12 AND age < 60` $\rightarrow$ Charge Normal Fare (0% discount).

### Group & Surcharge Rules (`rules/fare_rules.py`)
- **Rule F5 (Group Discount)**: `IF passenger_count >= 4` $\rightarrow$ Apply 5% Group Discount on booking subtotal.
- **Rule F6 (Weekend Surcharge)**: `IF travel_date IS Saturday OR Sunday` $\rightarrow$ Add 10% Weekend Surcharge.

### Booking Status Rules (`rules/rule_engine.py`)
- **Rule B1**: `IF payment_successful == True AND seats_available == True` $\rightarrow$ Booking Status = `CONFIRMED`.
- **Rule B2**: `IF payment_successful == False` $\rightarrow$ Booking Status = `PAYMENT FAILED`.
- **Rule B3**: `IF seats_available == False` $\rightarrow$ Booking Status = `REJECTED`.

### Cancellation Refund Rules (`rules/cancellation_rules.py`)
- **Rule C1**: `IF hours_until_departure > 24` $\rightarrow$ Refund 80% (20% fee).
- **Rule C2**: `IF hours_until_departure >= 12 AND <= 24` $\rightarrow$ Refund 50% (50% fee).
- **Rule C3**: `IF hours_until_departure < 12` $\rightarrow$ Refund 0% (100% fee).

---

## 7. Technologies Used
- **Backend**: Python 3 (Flask Framework)
- **Database**: SQLite3 (`database/database.db`)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Templating**: Jinja2
- **Icons**: Font Awesome 6

---

## 8. System Workflow
```text
User Search / Selection
         │
         ▼
HTML / CSS / JS Interface
         │
         ▼
Flask Routes (app.py)
         │
         ▼
Python Rule Engine (rules/)
 ├── seat_rules.py
 ├── fare_rules.py
 └── cancellation_rules.py
         │
         ▼
SQLite Database (database/db.py)
         │
         ▼
Deterministic JSON & Rendered Ticket
```

---

## 9. Project Structure
```text
BUS-BOOKING-TICKET-APPLICATION/
├── app.py                      # Main Flask application routes & endpoints
├── requirements.txt            # Dependency file (Flask)
├── README.md                   # Complete documentation & Viva Q&A
│
├── database/
│   ├── db.py                   # SQLite helper module & initial data seeding
│   └── database.db             # Auto-generated SQLite database file
│
├── rules/
│   ├── __init__.py
│   ├── rule_engine.py          # Central rule coordinator
│   ├── seat_rules.py           # Seat capacity & conflict rules
│   ├── fare_rules.py           # Age, group, and weekend pricing rules
│   └── cancellation_rules.py   # Time-tiered refund calculation rules
│
├── static/
│   ├── css/
│   │   └── style.css           # Custom responsive styles & print stylesheet
│   └── js/
│       └── script.js           # Interactive seat grid, live fare preview, modal JS
│
└── templates/
    ├── base.html               # Base Jinja2 layout with navbar & footer
    ├── index.html              # Home page introducing RBP
    ├── search.html             # Bus search & route discovery
    ├── seats.html              # Interactive seat selection grid
    ├── passenger.html          # Passenger details form & live fare preview
    ├── payment.html            # Mock payment gateway & rule audit summary
    ├── confirmation.html       # Printable e-ticket & rule execution log
    ├── bookings.html           # My Bookings dashboard & cancellation modal
    └── rules.html              # "How Rules Work" guide & interactive simulator
```

---

## 10. How to Install

1. Open your terminal / command prompt.
2. Navigate to the project root directory:
   ```bash
   git clone https://github.com/varshith1708/BUS-BOOKING-TICKET-APPLICATION.git
   cd BUS-BOOKING-TICKET-APPLICATION
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 11. How to Run

1. Execute the Flask application:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to:
   ```text
   http://127.0.0.1:5000
   ```
3. The database (`database/database.db`) will automatically initialize and populate sample buses on launch.

---

## 12. Example Rule Execution (Demonstration Scenario)

### Scenario Input:
- **Route**: Ahmedabad to Rajkot
- **Base Fare**: ₹500 per seat
- **Travel Date**: Future Date (Weekday)
- **Passenger 1**: Rahul, Age 20
- **Passenger 2**: Amit, Age 10

### Rule Engine Execution Steps:
1. **Seat Availability Rule**: Requested 2 seats, 30 available $\rightarrow$ **PASSED**.
2. **Passenger 1 Age Rule**: Age 20 > 12 and < 60 $\rightarrow$ Normal Fare = **₹500**.
3. **Passenger 2 Age Rule**: Age 10 $\ge$ 5 and $\le$ 12 $\rightarrow$ **50% Child Discount Applied** ($-₹250$) $\rightarrow$ Fare = **₹250**.
4. **Group Discount Rule**: Passengers (2) < 4 $\rightarrow$ **NOT APPLIED**.
5. **Weekend Rule**: Weekday $\rightarrow$ **NOT APPLIED**.
6. **Booking Status Rule**: Payment Successful & Seats Available $\rightarrow$ Status = **CONFIRMED**.

### Final Output:
- **Total Amount**: $\text{₹}500 + \text{₹}250 = \mathbf{\text{₹}750}$
- **Rule Audit Log**:
  - `✓ Seat Availability Rule → Passed`
  - `✓ Passenger 1 Age Rule → Normal Fare`
  - `✓ Passenger 2 Age Rule → 50% Child Discount Applied`
  - `✓ Booking Status Rule → Booking Confirmed`

---

## 13. Future Improvements
- Integrate dynamic rule editing via an Admin Portal dashboard.
- Support multi-currency rules and dynamic surge pricing rules based on peak holiday calendar dates.
- Export rule execution logs to PDF or JSON audit files.

---

## 14. Conclusion
RuleBus successfully demonstrates that Rule-Based Programming offers a clean, transparent, and reliable architectural pattern for complex business logic. Every decision in the system is fully explainable, deterministic, and verifiable through audit execution logs.

---

## 15. Viva Preparation Guide (10 Likely Viva Questions & Answers)

### Key Files to Understand for Viva:
1. `app.py`: Handles HTTP routes and delegates logic to rule modules.
2. `rules/rule_engine.py`: Central coordinator executing seat, fare, status, and cancellation rules.
3. `rules/fare_rules.py`: Contains python functions implementing age discounts, group discounts, and weekend surcharges.
4. `rules/cancellation_rules.py`: Contains time-tiered refund calculation rules.
5. `database/db.py`: SQLite schema and data persistence.

---

### Viva Questions & Answers

#### Q1: What is Rule-Based Programming (RBP) and how does it differ from Machine Learning?
**Answer**: Rule-Based Programming relies on explicit, human-coded `IF-THEN` conditional rules evaluated by a rule engine. It is 100% deterministic and explainable. Machine Learning, by contrast, uses statistical models trained on data to predict outcomes without explicit programming.

#### Q2: Why did you choose Python Flask for this RBP project?
**Answer**: Flask provides a lightweight, modular Python framework. Since RBP logic is best written in clean Python modules (`rules/`), Flask seamlessly bridges the frontend UI and the Python Rule Engine backend.

#### Q3: Where is the decision logic implemented in your project?
**Answer**: Decision logic is implemented strictly in separate Python files under the `rules/` directory (`seat_rules.py`, `fare_rules.py`, `cancellation_rules.py`, `rule_engine.py`), NOT hardcoded in JavaScript or HTML templates.

#### Q4: How does the system handle passenger age discounts?
**Answer**: The function `evaluate_passenger_age_rule` in `rules/fare_rules.py` evaluates the passenger's age:
- Age < 5 $\rightarrow$ 100% free
- $5 \le \text{Age} \le 12 \rightarrow$ 50% discount
- $\text{Age} \ge 60 \rightarrow$ 10% discount
- Otherwise $\rightarrow$ Normal fare.

#### Q5: How are duplicate seat bookings prevented?
**Answer**: `rules/seat_rules.py` checks requested seat numbers against the `booked_seats` table in SQLite for the selected bus and date. If any requested seat matches an already booked seat, the rule rejects the booking with an explicit conflict message.

#### Q6: How does the cancellation refund rule work?
**Answer**: `rules/cancellation_rules.py` calculates the hours remaining between current time and departure datetime:
- $> 24$ hours $\rightarrow$ 80% refund (20% fee)
- $12\text{--}24$ hours $\rightarrow$ 50% refund (50% fee)
- $< 12$ hours $\rightarrow$ 0% refund (100% fee).

#### Q7: What happens when 4 or more passengers book together?
**Answer**: `evaluate_group_discount_rule` in `rules/fare_rules.py` evaluates `IF passenger_count >= 4` and applies an additional 5% discount on the subtotal fare.

#### Q8: What is the Rule Execution Audit Log?
**Answer**: It is a structured JSON list produced by `RuleEngine` during evaluation. It records every rule evaluated, the condition checked, whether it passed/applied, and the resulting message, allowing full transparency on tickets and payment pages.

#### Q9: How is data persisted in the application?
**Answer**: Data is stored locally in an SQLite database (`database/database.db`). Relational tables include `buses`, `bookings`, `passengers`, and `booked_seats`.

#### Q10: How do you verify the system works without an internet connection or external API?
**Answer**: All bus routes are pre-populated into SQLite automatically upon app startup via `init_db()` in `database/db.py`, making the application completely self-contained and runnable offline.
