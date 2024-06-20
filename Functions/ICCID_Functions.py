def Luhn_Algorithm_Check(num):

    # Convert the number to a list of digits
    Digits = [int(d) for d in num]
    Checksum = 0

    # Double every second digit from the right    
    for i in range(len(Digits) - 2, -1, -2):
        Doubled_Value = Digits[i] * 2
        if Doubled_Value > 9:
            Doubled_Value -= 9
        Checksum += Doubled_Value
    
    # Add the rest of the digits
    Checksum += sum(Digits[-1::-2])
    
    # The number is valid if the checksum is a multiple of 10
    return Checksum % 10 == 0

def Verify_and_Strip_ICCID(iccid):

    # Check if the ICCID is valid
    if Luhn_Algorithm_Check(iccid):

        # If it is, strip the last digit
        return iccid[:-1]

    else:

        # If it is not, return None
        return iccid
