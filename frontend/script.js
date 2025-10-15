const API_URL = "http://127.0.0.1:8000/results";

document.getElementById("loadData").addEventListener("click", async () => {
    const response = await fetch(API_URL);
    const data = await response.json();

    const labels = data.map(d => d.Timestamp || d.time || ""); // zavisi kako se zove kolona
    const values = data.map(d => d.predicted_energy || d.prediction || d.value);

    const ctx = document.getElementById("chart").getContext("2d");
    new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [
                {
                    label: "Predicted Energy Consumption",
                    data: values,
                    borderWidth: 2,
                    borderColor: "rgb(75, 192, 192)",
                    fill: false,
                    tension: 0.1
                }
            ]
        }
    });
});

document.getElementById("predictForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const params = new URLSearchParams(formData);

    const res = await fetch(`${API_URL}/predict?${params.toString()}`);
    const data = await res.json();

    document.getElementById("result").textContent =
        `Predicted Energy Consumption: ${data.predicted_consumption} kWh`;
});