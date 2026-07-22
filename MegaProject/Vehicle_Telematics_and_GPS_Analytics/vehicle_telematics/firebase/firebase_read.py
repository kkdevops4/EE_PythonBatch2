from firebase.firebase_config import db


class FirebaseReader:

    def __init__(self):
        self.vehicle_id = "CAR001"

    def get_all_telemetry(self):

        docs = db.collection("vehicles") \
                 .document(self.vehicle_id) \
                 .collection("telemetry") \
                 .stream()

        telemetry_list = []

        for doc in docs:
            telemetry = doc.to_dict()
            telemetry_list.append(telemetry)

        return telemetry_list