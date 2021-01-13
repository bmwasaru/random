def clean_mobile_number(mobile_number):
    if mobile_number.startswith('0'):
        mobile = list(mobile_number)
        mobile[0] = '+254'
        return "".join(mobile)


assert clean_mobile_number('0700000000') == '+254700000000'
