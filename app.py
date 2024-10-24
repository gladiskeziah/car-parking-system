from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime, timedelta
import heapq

app = Flask(__name__, static_folder='static')

class Car:
    def __init__(self, car_id, arrival_time, parking_time):
        self.car_id = car_id
        self.arrival_time = arrival_time
        self.parking_time = parking_time
        self.leaving_time = arrival_time + timedelta(hours=parking_time)

    def __lt__(self, other):
        return self.parking_time < other.parking_time

class ParkingLot:
    def __init__(self, total_slots=10):
        self.total_slots = total_slots
        self.available_slots = total_slots
        self.parked_cars = []
        self.waiting_list = []
        heapq.heapify(self.parked_cars)
        heapq.heapify(self.waiting_list)

    def book_slot(self, car):
        if self.available_slots > 0:
            heapq.heappush(self.parked_cars, car)
            self.available_slots -= 1
            return f"Slot booked for Car {car.car_id}. Leaving time: {car.leaving_time}"
        else:
            longest_parking_car = heapq.nlargest(1, self.parked_cars)[0]
            if car.parking_time < longest_parking_car.parking_time:
                self.parked_cars.remove(longest_parking_car)
                heapq.heapify(self.parked_cars)
                heapq.heappush(self.parked_cars, car)
                heapq.heappush(self.waiting_list, longest_parking_car)
                return (f"Slot booked for Car {car.car_id}. Leaving time: {car.leaving_time}. "
                        f"Car {longest_parking_car.car_id} with longer parking time was swapped and moved to the waiting list.")
            else:
                heapq.heappush(self.waiting_list, car)
                return (f"No slots available. Car {car.car_id} has been added to the waiting list.")

    def release_slot(self):
        if self.parked_cars:
            car = heapq.heappop(self.parked_cars)
            self.available_slots += 1
            if self.waiting_list:
                next_car = heapq.heappop(self.waiting_list)
                heapq.heappush(self.parked_cars, next_car)
                self.available_slots -= 1
                return (f"Slot released for Car {car.car_id}. "
                        f"Car {next_car.car_id} from the waiting list has been moved to the slot.")
            return f"Slot released for Car {car.car_id}."
        else:
            return "No cars to release."

    def show_status(self):
        status = f"Parking Lot Status: {self.available_slots}/{self.total_slots} slots available\n"
        for car in self.parked_cars:
            status += f"Car {car.car_id} - Parking Time: {car.parking_time} hours - Leaving Time: {car.leaving_time}\n"
        status += "\nWaiting List:\n"
        for car in self.waiting_list:
            status += f"Car {car.car_id} - Parking Time: {car.parking_time} hours\n"
        return status

parking_lot = ParkingLot()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/book', methods=['POST'])
def book_slot():
    data = request.json
    car_id = data['car_id']
    parking_time = int(data['parking_time'])
    arrival_time = datetime.now()
    car = Car(car_id, arrival_time, parking_time)
    message = parking_lot.book_slot(car)
    return jsonify({'message': message})

@app.route('/release', methods=['POST'])
def release_slot():
    message = parking_lot.release_slot()
    return jsonify({'message': message})

@app.route('/status', methods=['GET'])
def show_status():
    status = parking_lot.show_status()
    return jsonify({'status': status})

if __name__ == '__main__':
    app.run(debug=True)
