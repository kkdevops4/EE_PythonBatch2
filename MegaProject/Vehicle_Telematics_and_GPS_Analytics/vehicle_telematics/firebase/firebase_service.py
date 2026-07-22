
from firebase.firebase_config import db


class FirebaseService:

    def __init__(self):
        self.vehicle_id = "CAR001"

    def clear_previous_telemetry(self):

        docs = db.collection("vehicles") \
                 .document(self.vehicle_id) \
                 .collection("telemetry") \
                 .stream()

        for doc in docs:
            doc.reference.delete()

        print("Previous telemetry deleted!")

    def upload_telemetry(self, telemetry):

        db.collection("vehicles") \
          .document(self.vehicle_id) \
          .collection("telemetry") \
          .add(telemetry)

        print("Telemetry uploaded successfully!")