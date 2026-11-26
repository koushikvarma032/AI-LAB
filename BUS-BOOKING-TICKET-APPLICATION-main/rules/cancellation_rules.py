"""
Rule-Based Programming Module: Cancellation & Refund Rules
Defines predefined IF-THEN rules for calculating ticket cancellation refunds based on departure timing.
"""
import datetime

class CancellationRules:

    @staticmethod
    def evaluate_cancellation_refund(total_amount, travel_date_str, departure_time_str):
        """
        Evaluates cancellation rules based on hours remaining until departure.
        
        Rules:
        1. IF time_until_departure > 24 hours THEN refund 80% (20% fee).
        2. IF time_until_departure >= 12 AND <= 24 hours THEN refund 50% (50% fee).
        3. IF time_until_departure < 12 hours THEN refund 0% (No refund).
        """
        rule_logs = []
        now = datetime.datetime.now()

        # Parse travel date and departure time
        try:
            dep_time_obj = datetime.datetime.strptime(departure_time_str.strip(), "%I:%M %p").time()
            date_obj = datetime.datetime.strptime(travel_date_str.strip(), "%Y-%m-%d").date()
            dep_datetime = datetime.datetime.combine(date_obj, dep_time_obj)
        except Exception:
            try:
                date_obj = datetime.datetime.strptime(travel_date_str.strip(), "%Y-%m-%d").date()
                dep_datetime = datetime.datetime.combine(date_obj, datetime.time(8, 0))
            except Exception:
                dep_datetime = now + datetime.timedelta(hours=25)

        hours_remaining = (dep_datetime - now).total_seconds() / 3600.0

        if hours_remaining > 24:
            refund_percentage = 80.0
            fee_percentage = 20.0
            condition_str = f"IF hours until departure ({hours_remaining:.1f} hrs) > 24 hours"
            status_str = "80% Refund Tier"
            action_str = "80% refund approved. 20% cancellation fee retained."
        elif 12 <= hours_remaining <= 24:
            refund_percentage = 50.0
            fee_percentage = 50.0
            condition_str = f"IF hours until departure ({hours_remaining:.1f} hrs) >= 12 AND <= 24 hours"
            status_str = "50% Refund Tier"
            action_str = "50% refund approved. 50% cancellation fee retained."
        else: # hours_remaining < 12
            refund_percentage = 0.0
            fee_percentage = 100.0
            condition_str = f"IF hours until departure ({hours_remaining:.1f} hrs) < 12 hours"
            status_str = "No Refund Tier (0%)"
            action_str = "No refund allowed for cancellations within 12 hours of departure."

        refund_amount = round(total_amount * (refund_percentage / 100.0), 2)
        cancellation_fee = round(total_amount - refund_amount, 2)

        rule_logs.append({
            "rule_name": "Cancellation Refund Rule",
            "condition": condition_str,
            "triggered": True,
            "status": status_str,
            "message": action_str,
            "hours_remaining": round(hours_remaining, 1),
            "total_amount": total_amount,
            "refund_percentage": refund_percentage,
            "refund_amount": refund_amount,
            "cancellation_fee": cancellation_fee
        })

        return {
            "can_cancel": True,
            "hours_remaining": round(hours_remaining, 1),
            "refund_percentage": refund_percentage,
            "refund_amount": refund_amount,
            "cancellation_fee": cancellation_fee,
            "rule_logs": rule_logs
        }
