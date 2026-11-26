from config import Config

def validate_diagnostic_input(data):
    """
    Validates user submitted diagnostic evidence.
    Returns (is_valid, sanitized_data, error_message).
    """
    errors = []
    sanitized = {}
    
    # Required continuous numerical sensors
    numeric_fields = {
        'battery_voltage': float,
        'alternator_voltage': float,
        'engine_rpm': int,
        'engine_temperature': float,
        'coolant_temperature': float,
        'oil_pressure': float
    }
    
    for field, field_type in numeric_fields.items():
        val = data.get(field)
        if val is None or val == '':
            errors.append(f"Field '{field}' is required.")
            continue
        try:
            num_val = field_type(val)
            
            # Check range boundaries
            r = Config.VARIABLE_RANGES[field]
            if num_val < r['min'] or num_val > r['max']:
                errors.append(f"{field.replace('_', ' ').title()} value {num_val} is outside valid range [{r['min']} - {r['max']} {r['unit']}].")
            else:
                sanitized[field] = num_val
        except (ValueError, TypeError):
            errors.append(f"Field '{field}' must be a valid number.")
            
    # Binary symptoms
    for sym in Config.SYMPTOMS:
        raw_val = data.get(sym, 0)
        if isinstance(raw_val, bool):
            sanitized[sym] = 1 if raw_val else 0
        elif str(raw_val).strip() in ['1', 'true', 'True', 'YES', 'yes']:
            sanitized[sym] = 1
        else:
            sanitized[sym] = 0
            
    if errors:
        return False, None, " | ".join(errors)
        
    return True, sanitized, None

def convert_inputs_to_bayesian_evidence(inputs):
    """
    Converts continuous and binary user inputs into categorical evidence dictionary
    suitable for pgmpy DiscreteBayesianNetwork query.
    """
    evidence = {}
    
    # Discretize continuous values based on exact thresholds
    v_bat = inputs['battery_voltage']
    if v_bat < 12.0:
        evidence['battery_voltage_state'] = 'LOW'
    elif v_bat > 14.6:
        evidence['battery_voltage_state'] = 'HIGH'
    else:
        evidence['battery_voltage_state'] = 'NORMAL'
        
    v_alt = inputs['alternator_voltage']
    if v_alt < 13.2:
        evidence['alternator_voltage_state'] = 'LOW'
    elif v_alt > 15.0:
        evidence['alternator_voltage_state'] = 'HIGH'
    else:
        evidence['alternator_voltage_state'] = 'NORMAL'
        
    e_temp = inputs['engine_temperature']
    if e_temp > 108.0:
        evidence['engine_temp_state'] = 'CRITICAL'
    elif e_temp > 98.0:
        evidence['engine_temp_state'] = 'HIGH'
    else:
        evidence['engine_temp_state'] = 'NORMAL'
        
    c_temp = inputs['coolant_temperature']
    if c_temp > 105.0:
        evidence['coolant_temp_state'] = 'CRITICAL'
    elif c_temp > 95.0:
        evidence['coolant_temp_state'] = 'HIGH'
    else:
        evidence['coolant_temp_state'] = 'NORMAL'
        
    o_press = inputs['oil_pressure']
    if o_press < 25.0:
        evidence['oil_pressure_state'] = 'LOW'
    elif o_press > 65.0:
        evidence['oil_pressure_state'] = 'HIGH'
    else:
        evidence['oil_pressure_state'] = 'NORMAL'
        
    rpm = inputs['engine_rpm']
    if rpm < 650:
        evidence['rpm_state'] = 'STALL_LOW'
    elif rpm > 3500:
        evidence['rpm_state'] = 'HIGH'
    else:
        evidence['rpm_state'] = 'NORMAL'
        
    # Symptoms mapped as string '0' or '1'
    for sym in Config.SYMPTOMS:
        evidence[sym] = str(inputs[sym])
        
    return evidence
