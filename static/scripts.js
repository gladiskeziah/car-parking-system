async function bookSlot() {
    const carId = document.getElementById('car_id').value;
    const parkingTime = document.getElementById('parking_time').value;

    const response = await fetch('/book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ car_id: carId, parking_time: parkingTime }),
    });

    const result = await response.json();
    document.getElementById('status').innerText = result.message;
}

async function releaseSlot() {
    const response = await fetch('/release', {
        method: 'POST',
    });

    const result = await response.json();
    document.getElementById('status').innerText = result.message;
}

async function showStatus() {
    const response = await fetch('/status', {
        method: 'GET',
    });

    const result = await response.json();
    document.getElementById('status').innerText = result.status;
}
