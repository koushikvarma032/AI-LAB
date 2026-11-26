"""
Rule Engine Central Coordinator
Imports seat rules, fare rules, cancellation rules, and booking status rules.
Evaluates end-to-end rules and outputs structured audit decisions.
"""
from rules.seat_rules import SeatRules
from rules.fare_rules import FareRules
from rules.cancellation_rules import CancellationRules

class RuleEngine:

    @staticmethod
    def evaluate_booking_status_rule(payment_successful, seats_available):
        """
        Evaluates booking status rule.
        
        Rules:
        1. IF payment is successful AND seats are available THEN booking status = CONFIRMED.
        2. IF payment fails THEN booking status = PAYMENT FAILED.
        3. IF seats are unavailable THEN booking status = REJECTED.
        """
        if not seats_available:
            rule_log = {
                "rule_name": "Booking Final Status Rule",
                "condition": "IF seats ARE unavailable",
                "triggered": True,
                "status": "REJECTED",
                "message": "Booking status set to REJECTED due to seat unavailability."
            }
            return "REJECTED", rule_log

        if not payment_successful:
            rule_log = {
                "rule_name": "Booking Final Status Rule",
                "condition": "IF payment FAILS",
                "triggered": True,
                "status": "PAYMENT FAILED",
                "message": "Booking status set to PAYMENT FAILED due to unconfirmed payment."
            }
            return "PAYMENT FAILED", rule_log

        rule_log = {
            "rule_name": "Booking Final Status Rule",
            "condition": "IF payment IS successful AND seats ARE available",
            "triggered": True,
            "status": "CONFIRMED",
            "message": "Booking status set to CONFIRMED."
        }
        return "CONFIRMED", rule_log

    @classmethod
    def evaluate_full_booking(cls, bus, requested_seats, passenger_list, travel_date_str, already_booked_seats, payment_successful=True):
        """
        Evaluates complete booking flow through all Rule Engine components.
        
        Returns:
        {
          "bookingAllowed": bool,
          "bookingStatus": str,
          "fareSummary": dict,
          "message": str,
          "executedRules": list
        }
        """
        executed_rules = []

        # 1. Evaluate Seat Availability Rules
        requested_count = len(requested_seats)
        available_count = bus.get('available_seats', 30) - len(already_booked_seats)

        seat_ok, seat_msg, seat_logs = SeatRules.evaluate_seat_availability(
            requested_count, available_count, requested_seats, already_booked_seats
        )
        executed_rules.extend(seat_logs)

        if not seat_ok:
            status, status_log = cls.evaluate_booking_status_rule(payment_successful=False, seats_available=False)
            executed_rules.append(status_log)
            return {
                "bookingAllowed": False,
                "bookingStatus": status,
                "fareSummary": None,
                "message": seat_msg,
                "executedRules": executed_rules
            }

        # 2. Evaluate Fare Calculation & Discount Rules
        base_fare = float(bus['base_fare'])
        fare_summary, fare_logs = FareRules.calculate_total_fare(base_fare, passenger_list, travel_date_str)
        executed_rules.extend(fare_logs)

        # 3. Evaluate Booking Status Rule
        booking_status, status_log = cls.evaluate_booking_status_rule(payment_successful, seats_available=True)
        executed_rules.append(status_log)

        return {
            "bookingAllowed": (booking_status == "CONFIRMED"),
            "bookingStatus": booking_status,
            "fareSummary": fare_summary,
            "message": f"Booking {booking_status.lower()} successfully.",
            "executedRules": executed_rules
        }

    @staticmethod
    def evaluate_cancellation(total_amount, travel_date_str, departure_time_str):
        """Delegates cancellation refund evaluation to CancellationRules."""
        return CancellationRules.evaluate_cancellation_refund(total_amount, travel_date_str, departure_time_str)
