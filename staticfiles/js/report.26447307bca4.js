const reportForm = document.getElementById("reportForm");
const submitButton = document.getElementById("submitButton");
const resultMessage = document.getElementById("resultMessage");


reportForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    submitButton.disabled = true;
    submitButton.textContent = "AI is analyzing report...";

    resultMessage.className = "result-message";
    resultMessage.innerHTML = "";

    const reportData = {
        name: document.getElementById("name").value.trim(),
        contact: document.getElementById("contact").value.trim(),
        location: document.getElementById("location").value.trim(),
        language: document.getElementById("language").value,
        description: document
            .getElementById("description")
            .value
            .trim()
    };

    try {
        const response = await fetch("/api/reports", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(reportData)
        });

        const result = await response.json();

        if (!response.ok) {
            resultMessage.className =
                "result-message result-error";

            resultMessage.textContent =
                result.message || "Unable to submit report.";

            return;
        }

        const report = result.data;

        resultMessage.className =
            "result-message result-success";

        resultMessage.innerHTML = `
            <strong>Emergency report submitted successfully.</strong>

            <div class="ai-result">
                <strong>AI Classification:</strong>
                ${escapeHtml(report.category)}
                <br>

                <strong>Urgency:</strong>
                ${escapeHtml(report.urgency)}
                <br>

                <strong>AI Summary:</strong>
                ${escapeHtml(report.summary)}
                <br>

                <strong>Confidence:</strong>
                ${escapeHtml(report.confidence)}
                <br>

                ${
                    report.possibleDuplicate
                        ? "<strong>Warning:</strong> Possible duplicate crisis report."
                        : ""
                }
            </div>
        `;

        reportForm.reset();

    } catch (error) {
        console.error("Report submission error:", error);

        resultMessage.className =
            "result-message result-error";

        resultMessage.textContent =
            "Unable to connect to CrisisDesk AI.";

    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "Submit Emergency Report";
    }
});


function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value ?? "";
    return div.innerHTML;
}