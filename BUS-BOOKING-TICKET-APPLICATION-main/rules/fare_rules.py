"""
Rule-Based Programming Module: Fare & Pricing Rules
Defines predefined IF-THEN rules for age discounts, group discounts, and weekend surcharges.
"""
import datetime

class FareRules:

    @staticmethod
    def evaluate_passenger_age_rule(base_fare, age):
        """
        Evaluates age-based ticket fare rules for an individual passenger.
        
        Rules:
        1. IF age < 5 THEN 100% Free Ticket (Discount = base_fare).
        2. IF age >= 5 AND age <= 12 THEN 50% Child Discount.
        3. IF age >= 60 THEN 10% Senior Citizen Discount.
        4. IF age > 12 AND age < 60 THEN Normal Fare (0% Discount).
        """
        discount_amount = 0.0
        discount_reason = "Normal Fare"
        rule_name = "Passenger Age Rule"
        
        if age < 5:
            discount_amount = base_fare
            discount_reason = "Infant Free Ticket (100% Off)"
            condition_str = f"IF age ({age}) < 5"
            action_str = f"Ticket is FREE (100% discount applied: -₹{discount_amount:.2f})"
        elif 5 <= age <= 12:
            discount_amount = base_fare * 0.50
            discount_reason = "Child Discount (50% Off)"
            condition_str = f"IF age ({age}) >= 5 AND age ({age}) <= 12"
            action_str = f"Apply 50% Child Discount (-₹{discount_amount:.2f})"
        elif age >= 60:
            discount_amount = base_fare * 0.10
            discount_reason = "Senior Citizen Discount (10% Off)"
            condition_str = f"IF age ({age}) >= 60"
            action_str = f"Apply 10% Senior Citizen Discount (-₹{discount_amount:.2f})"
        else: # 12 < age < 60
            discount_amount = 0.0
            discount_reason = "Normal Fare (No Discount)"
            condition_str = f"IF age ({age}) > 12 AND age ({age}) < 60"
            action_str = "Charge Normal Fare (₹" + f"{base_fare:.2f})"

        final_fare = base_fare - discount_amount

        rule_log = {
            "rule_name": rule_name,
            "condition": condition_str,
            "triggered": True,
            "status": discount_reason,
            "message": action_str,
            "base_fare": base_fare,
            "discount_amount": discount_amount,
            "final_fare": final_fare
        }

        return final_fare, discount_amount, discount_reason, rule_log

    @staticmethod
    def evaluate_group_discount_rule(subtotal, passenger_count):
        """
        Evaluates group discount rule.
        
        Rule:
        IF passenger_count >= 4 THEN apply 5% group discount.
        """
        if passenger_count >= 4:
            group_discount = subtotal * 0.05
            rule_log = {
                "rule_name": "Group Booking Rule",
                "condition": f"IF passenger count ({passenger_count}) >= 4",
                "triggered": True,
                "status": "APPLIED",
                "message": f"5% Group Discount applied (-₹{group_discount:.2f})",
                "discount_amount": group_discount
            }
            return group_discount, rule_log
        else:
            rule_log = {
                "rule_name": "Group Booking Rule",
                "condition": f"IF passenger count ({passenger_count}) >= 4",
                "triggered": False,
                "status": "NOT APPLIED",
                "message": "Group discount requires 4 or more passengers.",
                "discount_amount": 0.0
            }
            return 0.0, rule_log

    @staticmethod
    def evaluate_weekend_surcharge_rule(base_total, travel_date_str):
        """
        Evaluates weekend surcharge rule.
        
        Rule:
        IF travel_date is Saturday (weekday 5) OR Sunday (weekday 6)
        THEN add 10% weekend surcharge.
        """
        try:
            date_obj = datetime.datetime.strptime(travel_date_str, '%Y-%m-%d')
            day_name = date_obj.strftime('%A')
            is_weekend = date_obj.weekday() in (5, 6) # 5 = Saturday, 6 = Sunday
        except Exception:
            day_name = "Unknown"
            is_weekend = False

        if is_weekend:
            surcharge = base_total * 0.10
            rule_log = {
                "rule_name": "Weekend Travel Rule",
                "condition": f"IF travel date ({travel_date_str}, {day_name}) IS Weekend",
                "triggered": True,
                "status": "APPLIED",
                "message": f"10% Weekend Surcharge added (+₹{surcharge:.2f})",
                "surcharge_amount": surcharge
            }
            return surcharge, rule_log
        else:
            rule_log = {
                "rule_name": "Weekend Travel Rule",
                "condition": f"IF travel date ({travel_date_str}, {day_name}) IS Weekend",
                "triggered": False,
                "status": "NOT APPLIED",
                "message": f"Weekday travel ({day_name}) - Standard rates apply.",
                "surcharge_amount": 0.0
            }
            return 0.0, rule_log

    @classmethod
    def calculate_total_fare(cls, base_fare, passengers, travel_date_str):
        """
        Orchestrates all fare rules for a group of passengers.
        Returns passenger breakdown, total amount, and complete rule execution logs.
        """
        passenger_results = []
        rule_logs = []
        raw_total_base = base_fare * len(passengers)
        passengers_subtotal = 0.0
        total_age_discounts = 0.0

        # Step 1: Evaluate Individual Age Rules for each passenger
        for idx, p in enumerate(passengers, start=1):
            p_name = p.get('name', f"Passenger {idx}")
            p_age = int(p.get('age', 18))
            
            p_final, p_disc, p_reason, p_rule_log = cls.evaluate_passenger_age_rule(base_fare, p_age)
            p_rule_log["rule_name"] = f"Passenger {idx} Age Rule ({p_name})"
            rule_logs.append(p_rule_log)

            passengers_subtotal += p_final
            total_age_discounts += p_disc

            passenger_results.append({
                "name": p_name,
                "age": p_age,
                "gender": p.get('gender', 'Other'),
                "phone": p.get('phone', ''),
                "base_fare": base_fare,
                "discount_amount": p_disc,
                "discount_reason": p_reason,
                "final_fare": p_final
            })

        # Step 2: Evaluate Group Discount Rule on passenger subtotal
        group_disc, group_rule_log = cls.evaluate_group_discount_rule(passengers_subtotal, len(passengers))
        rule_logs.append(group_rule_log)

        after_group_total = passengers_subtotal - group_disc

        # Step 3: Evaluate Weekend Surcharge Rule on raw base total
        weekend_surcharge, weekend_rule_log = cls.evaluate_weekend_surcharge_rule(raw_total_base, travel_date_str)
        rule_logs.append(weekend_rule_log)

        final_total = after_group_total + weekend_surcharge

        fare_summary = {
            "raw_total_base": raw_total_base,
            "passengers_subtotal": passengers_subtotal,
            "total_age_discounts": total_age_discounts,
            "group_discount": group_disc,
            "weekend_surcharge": weekend_surcharge,
            "final_total": round(final_total, 2),
            "passenger_details": passenger_results
        }

        return fare_summary, rule_logs
