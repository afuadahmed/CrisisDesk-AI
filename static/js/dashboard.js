const reportList = document.getElementById("reportList");
const refreshButton = document.getElementById("refreshButton");

const totalReports = document.getElementById("totalReports");
const criticalReports = document.getElementById("criticalReports");
const possibleDuplicates = document.getElementById("possibleDuplicates");


async function loadAnalytics() {
    try {
        const response = await fetch("/api/analytics/summary");
        const result = await response.json();

        if (!result.success) {
            return;
        }

        totalReports.textContent = result.data.totalReports;
        criticalReports.textContent = result.data.criticalReports;
        possibleDuplicates.textContent = result.data.possibleDuplicates;

    } catch (error) {
        console.error("Analytics error:", error);
    }
}


async function loadReports() {
    reportList.innerHTML = `
        <p class="loading">Loading reports...</p>
    `;

    try {
        const response = await fetch(
            "/api/reports?ordering=-created_at&page_size=20"
        );

        const result = await response.json();
        const reports = result.results.data;

        if (reports.length === 0) {
            reportList.innerHTML = `
                <p class="loading">No reports found.</p>
            `;
            return;
        }

        reportList.innerHTML = reports
            .map(createReportCard)
            .join("");

    } catch (error) {
        console.error("Report loading error:", error);

        reportList.innerHTML = `
            <p class="loading">Unable to load reports.</p>
        `;
    }
}


function createReportCard(report) {
    const urgencyClass = `badge-${report.urgency}`;

    return `
        <article
            class="report-card"
            onclick="handleReportCardClick(event, '${report.id}')"
        >

            <div class="report-top">

                <div>
                    <h3>${escapeHtml(report.category)}</h3>

                    <p class="report-location">
                        ${escapeHtml(report.location)}
                    </p>
                </div>

                <span class="badge ${urgencyClass}">
                    ${escapeHtml(report.urgency)}
                </span>

            </div>

            <p class="report-summary">
                ${escapeHtml(report.summary)}
            </p>

            <div class="report-action">
                <strong>AI Suggested Action</strong><br>
                ${escapeHtml(report.suggestedAction)}
            </div>

            <div class="report-footer">

                <div class="report-meta">

                    <span>
                        Confidence: ${report.confidence}
                    </span>

                    ${
                        report.possibleDuplicate
                            ? `<span class="duplicate-warning">
                                Possible Duplicate
                               </span>`
                            : ""
                    }

                </div>

                <select
                    class="status-select"
                    onchange="updateReportStatus(
                        '${report.id}',
                        this.value
                    )"
                >
                    ${createStatusOptions(report.status)}
                </select>

            </div>

        </article>
    `;
}

function handleReportCardClick(event, reportId) {
    if (event.target.closest(".status-select")) {
        return;
    }

    openReportModal(reportId);
}


function createStatusOptions(currentStatus) {
    const statuses = [
        "pending",
        "in_review",
        "assigned",
        "resolved",
        "rejected"
    ];

    return statuses
        .map(status => `
            <option
                value="${status}"
                ${status === currentStatus ? "selected" : ""}
            >
                ${formatStatus(status)}
            </option>
        `)
        .join("");
}


function formatStatus(status) {
    return status
        .replace("_", " ")
        .replace(/\b\w/g, letter => letter.toUpperCase());
}


async function updateReportStatus(reportId, newStatus) {
    try {
        const response = await fetch(
            `/api/reports/${reportId}/status`,
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    status: newStatus
                })
            }
        );

        const result = await response.json();

        if (!response.ok) {
            alert(result.message || "Status update failed.");
            return;
        }

        await loadDashboard();

    } catch (error) {
        console.error("Status update error:", error);

        alert("Unable to update report status.");
    }
}


function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value ?? "";
    return div.innerHTML;
}


async function loadDashboard() {
    await Promise.all([
        loadAnalytics(),
        loadReports()
    ]);
}


refreshButton.addEventListener(
    "click",
    loadDashboard
);


loadDashboard();

async function openReportModal(reportId) {
    const modal = document.getElementById("reportModal");

    try {
        const response = await fetch(`/api/reports/${reportId}`);
        const result = await response.json();

        if (!response.ok || !result.success) {
            throw new Error("Failed to load report details.");
        }

        const report = result.data;

        document.getElementById("modalCategory").textContent =
            report.category || "Unknown";

        document.getElementById("modalUrgency").textContent =
            report.urgency || "-";

        document.getElementById("modalStatus").textContent =
            (report.status || "-").replace("_", " ");

        document.getElementById("modalConfidence").textContent =
            report.confidence ?? "-";

        document.getElementById("modalLocation").textContent =
            report.location || "-";

        document.getElementById("modalSummary").textContent =
            report.summary || "-";

        document.getElementById("modalSuggestedAction").textContent =
            report.suggestedAction || "-";

        document.getElementById("modalDescription").textContent =
            report.description || "-";

        document.getElementById("modalReporter").textContent =
            report.name || "Anonymous";

        document.getElementById("modalContact").textContent =
            report.contact || "Not provided";

        const duplicateWarning =
            document.getElementById("modalDuplicate");

        if (report.possibleDuplicate) {
            duplicateWarning.classList.add("active");
        } else {
            duplicateWarning.classList.remove("active");
        }

        modal.classList.add("active");
        document.body.classList.add("modal-open");

    } catch (error) {
        console.error("Report detail error:", error);
        alert("Unable to load report details.");
    }
}


function closeReportModal() {
    const modal = document.getElementById("reportModal");

    modal.classList.remove("active");
    document.body.classList.remove("modal-open");
}


document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        closeReportModal();
    }
});