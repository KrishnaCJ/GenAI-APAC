const apiBase = window.location.hostname === "localhost" ? "http://localhost:8080" : "";

const locationInput = document.getElementById("location");
const monthInput = document.getElementById("month");
const soilInput = document.getElementById("soil");
const submitButton = document.getElementById("submit");

const cropCard = document.getElementById("crop-card");
const weatherCard = document.getElementById("weather-card");
const decisionCard = document.getElementById("decision-card");
const marketCard = document.getElementById("market-card");
const todayAdvice = document.getElementById("today-advice");

async function fetchAdvice() {
  const payload = {
    location: locationInput.value.trim() || "Pune",
    month: parseInt(monthInput.value, 10),
    soil: soilInput.value,
  };

  const response = await fetch(`${apiBase}/api/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await response.json();
  renderCards(data);
}

function renderCards(data) {
  const result = data.result;

  cropCard.innerHTML = `
    <h3>Crop Advisor Agent</h3>
    <p><strong>Top crops:</strong> ${result.crop_advisor.crops.join(", ") || "None"}</p>
    <ul>${result.crop_advisor.reasons.map((r) => `<li>${r}</li>`).join("")}</ul>
  `;

  weatherCard.innerHTML = `
    <h3>Weather Intelligence Agent</h3>
    <p><strong>Rain risk:</strong> ${result.weather.rain_risk}</p>
    <p><strong>Rain next 10 days:</strong> ${result.weather.rainfall_mm_next_10d} mm</p>
  `;

  decisionCard.innerHTML = `
    <h3>Decision Agent</h3>
    <p>${result.decision.recommendation}</p>
    <ul>${result.decision.reasoning.map((r) => `<li>${r}</li>`).join("")}</ul>
  `;

  marketCard.innerHTML = `
    <h3>Monetization Insight</h3>
    ${renderMonetization(result.monetization)}
  `;

  todayAdvice.textContent = data.today_advice;
}

submitButton.addEventListener("click", (event) => {
  event.preventDefault();
  fetchAdvice();
});

function renderMonetization(monetization) {
  if (!monetization || !monetization.options || monetization.options.length === 0) {
    return "<p>No profit estimates available.</p>";
  }

  const rows = monetization.options
    .map(
      (option) =>
        `<li>${option.crop}: 	${option.expected_profit_inr.toLocaleString("en-IN")} INR/acre (${option.trend})</li>`
    )
    .join("");

  const best = monetization.best_option
    ? `<p><strong>Most profitable:</strong> ${monetization.best_option.crop}</p>`
    : "";

  return `${best}<ul>${rows}</ul>`;
}
