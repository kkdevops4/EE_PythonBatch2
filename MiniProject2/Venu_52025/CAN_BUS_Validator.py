# ==============================
# CAN BUS MESSAGE VALIDATOR
# ==============================

# Custom Exceptions

class InvalidCANIDError(Exception):
    def __init__(self, message):
        super().__init__(message)


class DLCMismatchError(Exception):
    def __init__(self, message):
        super().__init__(message)


class PayloadFormatError(Exception):
    def __init__(self, message):
        super().__init__(message)


# CAN ID Class

class CANID:

    def validate(self, can_id):

        try:
            int(can_id, 16)

        except ValueError as e:
            raise InvalidCANIDError(
                f"Invalid CAN ID: '{can_id}' is not a hex value"
            ) from e


# DLC Class

class DLC:

    def validate(self, dlc):

        try:
            return int(dlc)

        except ValueError as e:
            raise DLCMismatchError(
                f"Invalid DLC: '{dlc}' is not a number"
            ) from e


# Payload Class

class Payload:

    def validate(self, payload):

        data = payload.split()

        try:
            for byte in data:
                int(byte, 16)

        except ValueError as e:
            raise PayloadFormatError(
                f"Invalid Payload: '{byte}' is not a hex value"
            ) from e

        return data


# Save Result

def save_result(can_id, dlc, payload, result):

    file = open("can_log.txt", "a")

    file.write(
        f"CAN_ID={can_id}  DLC={dlc}  PAYLOAD={payload}  --> {result}\n"
    )

    file.close()


# Main Program

print("================================")
print(" CAN BUS MESSAGE VALIDATOR")
print("================================")

can_id = input("Enter CAN ID : ")
dlc = input("Enter DLC : ")
payload = input("Enter Payload : ")

try:

    can = CANID()
    dlc_obj = DLC()
    payload_obj = Payload()

    # Validation
    can.validate(can_id)

    dlc_value = dlc_obj.validate(dlc)

    payload_data = payload_obj.validate(payload)

    # DLC vs Payload Length Check
    if dlc_value != len(payload_data):

        raise DLCMismatchError(
            f"DLC={dlc_value} but payload has {len(payload_data)} byte(s)"
        )

    result = "VALID MESSAGE"

except Exception as e:

    result = "INVALID - " + str(e)

print("\nResult :", result)

save_result(can_id, dlc, payload, result)

print("Result saved in can_log.txt")