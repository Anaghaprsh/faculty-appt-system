from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# In-memory data store (simulates DB)
faculty_db = {
    "F001": {"name": "Dr. Ramesh Kumar", "department": "CS", "available_slots": ["09:00", "11:00", "14:00"]},
    "F002": {"name": "Prof. Sneha Nair", "department": "CS", "available_slots": ["10:00", "13:00", "15:00"]},
    "F003": {"name": "Dr. Arjun Mehta", "department": "CS", "available_slots": ["09:30", "12:00", "16:00"]},
}

appointments_db = []

@app.route("/")
def home():
    return jsonify({"message": "Faculty Appointment Management System API", "status": "running"})

@app.route("/api/faculty", methods=["GET"])
def get_all_faculty():
    return jsonify({"faculty": faculty_db})

@app.route("/api/faculty/<faculty_id>", methods=["GET"])
def get_faculty(faculty_id):
    faculty = faculty_db.get(faculty_id)
    if not faculty:
        return jsonify({"error": "Faculty not found"}), 404
    return jsonify({"faculty_id": faculty_id, **faculty})

@app.route("/api/faculty/<faculty_id>/availability", methods=["GET"])
def get_availability(faculty_id):
    faculty = faculty_db.get(faculty_id)
    if not faculty:
        return jsonify({"error": "Faculty not found"}), 404
    return jsonify({
        "faculty_id": faculty_id,
        "name": faculty["name"],
        "available_slots": faculty["available_slots"]
    })

@app.route("/api/appointments", methods=["POST"])
def book_appointment():
    data = request.get_json()
    required = ["student_name", "usn", "faculty_id", "slot"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    faculty = faculty_db.get(data["faculty_id"])
    if not faculty:
        return jsonify({"error": "Faculty not found"}), 404

    if data["slot"] not in faculty["available_slots"]:
        return jsonify({"error": "Slot not available"}), 409

    appointment = {
        "appointment_id": f"APT{len(appointments_db)+1:03d}",
        "student_name": data["student_name"],
        "usn": data["usn"],
        "faculty_id": data["faculty_id"],
        "faculty_name": faculty["name"],
        "slot": data["slot"],
        "booked_at": datetime.now().isoformat()
    }
    appointments_db.append(appointment)
    faculty["available_slots"].remove(data["slot"])
    return jsonify({"message": "Appointment booked!", "appointment": appointment}), 201

@app.route("/api/appointments", methods=["GET"])
def get_appointments():
    return jsonify({"appointments": appointments_db})

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
