"""
Rule-Based Programming Module: Seat Availability & Conflict Rules
Defines predefined IF-THEN rules for evaluating seat selection.
"""

class SeatRules:
    @staticmethod
    def evaluate_seat_availability(requested_count, available_count, selected_seats, already_booked_seats):
        """
        Evaluates seat capacity and seat conflict rules.
        
        Rules:
        1. IF requested_count <= available_count THEN seat capacity OK.
        2. IF requested_count > available_count THEN reject ("Not enough seats available.").
        3. IF any selected seat is already booked THEN reject ("Seat already booked.").
        """
        rule_logs = []

        # Rule 1 & 2: Seat Quantity / Capacity Rule
        if requested_count <= 0:
            rule_logs.append({
                "rule_name": "Seat Quantity Validation Rule",
                "condition": "IF requested_seats <= 0",
                "triggered": True,
                "status": "REJECTED",
                "message": "Please select at least 1 seat."
            })
            return False, "Please select at least 1 seat.", rule_logs

        if requested_count <= available_count:
            rule_logs.append({
                "rule_name": "Seat Availability Capacity Rule",
                "condition": f"IF requested_seats ({requested_count}) <= available_seats ({available_count})",
                "triggered": True,
                "status": "PASSED",
                "message": f"Seat availability confirmed. {requested_count} seat(s) requested, {available_count} available."
            })
        else:
            rule_logs.append({
                "rule_name": "Seat Availability Capacity Rule",
                "condition": f"IF requested_seats ({requested_count}) > available_seats ({available_count})",
                "triggered": True,
                "status": "REJECTED",
                "message": "Not enough seats available."
            })
            return False, "Not enough seats available.", rule_logs

        # Rule 3: Conflict Rule
        conflicting_seats = [seat for seat in selected_seats if seat in already_booked_seats]
        if conflicting_seats:
            conflict_str = ", ".join(conflicting_seats)
            rule_logs.append({
                "rule_name": "Seat Occupancy Conflict Rule",
                "condition": f"IF selected seats ({conflict_str}) IN already_booked_seats",
                "triggered": True,
                "status": "REJECTED",
                "message": f"Seat(s) {conflict_str} are already booked. Please choose other seats."
            })
            return False, f"Seat(s) {conflict_str} are already booked.", rule_logs
        else:
            rule_logs.append({
                "rule_name": "Seat Occupancy Conflict Rule",
                "condition": "IF selected seats NOT IN already_booked_seats",
                "triggered": True,
                "status": "PASSED",
                "message": "All requested seats are available for booking."
            })

        return True, "Seat selection valid.", rule_logs
