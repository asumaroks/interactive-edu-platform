const apiUrl = "http://127.0.0.1:5000";

async function createRoom() {
    const response = await fetch(`${apiUrl}/create-room`, { method: "POST" });
    const data = await response.json();
    document.getElementById("roomCode").innerText = `Код комнаты: ${data.room_code}`;
}

async function createTest() {
    const roomCode = document.getElementById("testRoomCode").value;
    const questions = JSON.parse(document.getElementById("questions").value);

    const response = await fetch(`${apiUrl}/create-test`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ room_code: parseInt(roomCode), questions }),
    });

    const data = await response.json();
    document.getElementById("testMessage").innerText = data.message || data.error;
}

async function joinRoom() {
    const roomCode = document.getElementById("joinRoomCode").value;
    const studentName = document.getElementById("studentName").value;

    const response = await fetch(`${apiUrl}/join-room`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ room_code: parseInt(roomCode), student_name: studentName }),
    });

    const data = await response.json();
    document.getElementById("joinMessage").innerText = data.message || data.error;
}

async function submitAnswers() {
    const roomCode = document.getElementById("answerRoomCode").value;
    const studentName = document.getElementById("answerStudentName").value;
    const answers = JSON.parse(document.getElementById("answers").value);

    const response = await fetch(`${apiUrl}/submit-answers`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ room_code: parseInt(roomCode), student_name: studentName, answers }),
    });

    const data = await response.json();
    document.getElementById("answerMessage").innerText = data.message || data.error;
}

async function startTest() {
    const roomCode = document.getElementById("startRoomCode").value;

    const response = await fetch(`${apiUrl}/start-test`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ room_code: parseInt(roomCode) }),
    });

    const data = await response.json();
    document.getElementById("startMessage").innerText = data.message || data.error;
}

async function exportResults() {
    const roomCode = document.getElementById("exportRoomCode").value;

    const response = await fetch(`${apiUrl}/export-results?room_code=${roomCode}`);
    if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `results_${roomCode}.xlsx`;
        document.body.appendChild(a);
        a.click();
        a.remove();
    } else {
        const data = await response.json();
        alert(data.error);
    }
}