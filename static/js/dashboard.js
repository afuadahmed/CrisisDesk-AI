const reportList = document.getElementById("reportList");

const refreshButton =
    document.getElementById("refreshButton");

const categoryFilter =
    document.getElementById("categoryFilter");

const urgencyFilter =
    document.getElementById("urgencyFilter");

const statusFilter =
    document.getElementById("statusFilter");

const orderingFilter =
    document.getElementById("orderingFilter");


const totalReports =
    document.getElementById("totalReports");

const criticalReports =
    document.getElementById("criticalReports");

const possibleDuplicates =
    document.getElementById("possibleDuplicates");


let loadedIncidents = [];


async function loadAnalytics() {
    try {
        const response = await fetch(
            "/api/reports/stats/summary"
        );

        const result = await response.json();

        if (
            !response.ok ||
            !result.success
        ) {
            throw new Error(
                "Failed to load analytics."
            );
        }

        const data = result.data;

        totalReports.textContent =
            data.totalReports ?? 0;

        criticalReports.textContent =
            data.criticalReports ?? 0;

        possibleDuplicates.textContent =
            data.possibleDuplicates ?? 0;

        document.getElementById(
            "pendingReports"
        ).textContent =
            data.pendingReports ?? 0;

        document.getElementById(
            "resolvedReports"
        ).textContent =
            data.resolvedReports ?? 0;

        renderAnalyticsBreakdown(
            "categoryAnalytics",
            data.categoryBreakdown
        );

        renderAnalyticsBreakdown(
            "statusAnalytics",
            data.statuses
        );

        renderAnalyticsBreakdown(
            "urgencyAnalytics",
            data.urgencyBreakdown
        );

    } catch (error) {
        console.error(
            "Analytics error:",
            error
        );
    }
}


function renderAnalyticsBreakdown(
    containerId,
    breakdown
) {

    const container =
        document.getElementById(
            containerId
        );

    if (!container) {
        return;
    }


    const entries =
        Object.entries(
            breakdown || {}
        );


    if (entries.length === 0) {

        container.innerHTML = `
            <p class="analytics-empty">
                No analytics data available.
            </p>
        `;

        return;
    }


    const maximumValue =
        Math.max(
            ...entries.map(
                ([, value]) => value
            ),
            1
        );


    container.innerHTML =
        entries
            .map(
                ([label, value]) => {

                    const percentage =
                        (
                            value /
                            maximumValue
                        ) * 100;


                    return `
                        <div class="analytics-row">

                            <div class="analytics-row-header">

                                <span>
                                    ${escapeHtml(
                                        formatStatus(label)
                                    )}
                                </span>

                                <strong>
                                    ${value}
                                </strong>

                            </div>


                            <div class="analytics-bar">

                                <div
                                    class="analytics-bar-fill"
                                    style="width: ${percentage}%"
                                ></div>

                            </div>

                        </div>
                    `;
                }
            )
            .join("");
}


async function loadReports() {
    reportList.innerHTML = `
        <p class="loading">
            Loading incidents...
        </p>
    `;

    try {
        const params = new URLSearchParams();

        params.set(
            "page_size",
            "20"
        );

        params.set(
            "ordering",
            orderingFilter.value
        );


        if (categoryFilter.value) {
            params.set(
                "category",
                categoryFilter.value
            );
        }


        if (urgencyFilter.value) {
            params.set(
                "urgency",
                urgencyFilter.value
            );
        }


        if (statusFilter.value) {
            params.set(
                "status",
                statusFilter.value
            );
        }


        const response = await fetch(
            `/api/reports?${params.toString()}`
        );


        const result = await response.json();


        if (
            !response.ok ||
            !result.results ||
            !result.results.success
        ) {
            throw new Error(
                "Failed to load reports."
            );
        }


        const reports =
            result.results.data || [];


        if (reports.length === 0) {

            loadedIncidents = [];

            reportList.innerHTML = `
                <p class="loading">
                    No incidents found.
                </p>
            `;

            return;
        }


        loadedIncidents =
            groupReportsByIncident(reports);


        reportList.innerHTML =
            loadedIncidents
                .map(createIncidentCard)
                .join("");


    } catch (error) {

        console.error(
            "Report loading error:",
            error
        );


        reportList.innerHTML = `
            <p class="loading">
                Unable to load incidents.
            </p>
        `;
    }
}


function groupReportsByIncident(reports) {
    const incidentMap = new Map();


    reports.forEach(report => {

        const incidentId =
            report.incidentId ??
            report.incident ??
            report.id;


        if (!incidentMap.has(incidentId)) {

            incidentMap.set(
                incidentId,
                []
            );
        }


        incidentMap
            .get(incidentId)
            .push(report);
    });


    return Array
        .from(incidentMap.entries())
        .map(
            ([incidentId, incidentReports]) => {

                const primaryReport =
                    selectPrimaryReport(
                        incidentReports
                    );


                return {
                    incidentId: incidentId,

                    reports: incidentReports,

                    primaryReport: primaryReport,

                    reportCount:
                        incidentReports.length
                };
            }
        );
}


function selectPrimaryReport(reports) {

    const nonDuplicateReport =
        reports.find(
            report =>
                !report.possibleDuplicate
        );


    if (nonDuplicateReport) {
        return nonDuplicateReport;
    }


    return reports[0];
}


function createIncidentCard(incident) {

    const report =
        incident.primaryReport;


    const urgencyClass =
        `badge-${report.urgency}`;


    const backendReportCount =
        report.incidentReportCount ?? 1;


    const reportCount =
        Math.max(
            incident.reportCount,
            backendReportCount
        );


    return `
        <article
            class="report-card incident-card"
            onclick="handleIncidentCardClick(
                event,
                '${incident.incidentId}'
            )"
        >

            <div class="report-top">

                <div>

                    <h3>
                        ${escapeHtml(report.category)}
                    </h3>


                    <p class="report-location">
                        ${escapeHtml(report.location)}
                    </p>

                </div>


                <span class="badge ${urgencyClass}">
                    ${escapeHtml(report.urgency)}
                </span>

            </div>


            <div class="incident-card-info">

                <strong>
                    ${reportCount}
                    ${
                        reportCount === 1
                            ? "Linked Report"
                            : "Linked Reports"
                    }
                </strong>


                <span>
                    Incident ID:
                    ${escapeHtml(
                        incident.incidentId
                    )}
                </span>

            </div>


            <p class="report-summary">
                ${escapeHtml(report.summary)}
            </p>


            <div class="report-action">

                <strong>
                    AI Suggested Action
                </strong>

                <br>

                ${escapeHtml(
                    report.suggestedAction ??
                    report.suggested_action
                )}

            </div>


            <div class="report-footer">

                <div class="report-meta">

                    <span>
                        Confidence:
                        ${report.confidence}
                    </span>


                    ${
                        reportCount > 1
                            ? `
                                <span class="incident-linked-label">
                                    Incident Cluster
                                </span>
                            `
                            : ""
                    }

                </div>


                <select
                    class="status-select"
                    onchange="updateIncidentStatus(
    '${incident.incidentId}',
    this.value
)"
                >

                    ${createStatusOptions(
                        report.status
                    )}

                </select>

            </div>

        </article>
    `;
}


function handleIncidentCardClick(
    event,
    incidentId
) {

    if (
        event.target.closest(
            ".status-select"
        )
    ) {
        return;
    }


    openIncidentModal(incidentId);
}


function createStatusOptions(
    currentStatus
) {

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
                ${
                    status === currentStatus
                        ? "selected"
                        : ""
                }
            >
                ${formatStatus(status)}
            </option>
        `)
        .join("");
}


function formatStatus(status) {

    if (!status) {
        return "-";
    }


    return status
        .replaceAll("_", " ")
        .replace(
            /\b\w/g,
            letter =>
                letter.toUpperCase()
        );
}


async function updateReportStatus(
    reportId,
    newStatus
) {

    try {

        const response = await fetch(
            `/api/reports/${reportId}/status`,
            {
                method: "PATCH",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    status: newStatus
                })
            }
        );


        const result =
            await response.json();


        if (!response.ok) {

            alert(
                result.message ||
                "Status update failed."
            );

            return;
        }


        await loadDashboard();


    } catch (error) {

        console.error(
            "Status update error:",
            error
        );


        alert(
            "Unable to update report status."
        );
    }
}

async function updateIncidentStatus(
    incidentId,
    newStatus
) {

    try {

        const response = await fetch(
            `/api/incidents/${incidentId}/status`,
            {
                method: "PATCH",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    status: newStatus
                })
            }
        );


        const result =
            await response.json();


        if (!response.ok) {

            alert(
                result.message ||
                "Incident status update failed."
            );

            return;
        }


        await loadDashboard();


    } catch (error) {

        console.error(
            "Incident status update error:",
            error
        );


        alert(
            "Unable to update incident status."
        );
    }
}


function escapeHtml(value) {

    const div =
        document.createElement("div");


    div.textContent =
        value ?? "";


    return div.innerHTML;
}


async function loadDashboard() {

    await Promise.all([
        loadAnalytics(),
        loadReports()
    ]);
}


function openIncidentModal(incidentId) {

    const modal =
        document.getElementById(
            "reportModal"
        );


    const incident =
        loadedIncidents.find(
            item =>
                String(item.incidentId) ===
                String(incidentId)
        );


    if (!incident) {

        alert(
            "Unable to locate incident details."
        );

        return;
    }


    const report =
        incident.primaryReport;


    const backendReportCount =
        report.incidentReportCount ?? 1;


    const reportCount =
        Math.max(
            incident.reportCount,
            backendReportCount
        );


    document.getElementById(
        "modalCategory"
    ).textContent =
        report.category ||
        "Unknown";


    document.getElementById(
        "modalUrgency"
    ).textContent =
        report.urgency ||
        "-";


    document.getElementById(
        "modalStatus"
    ).textContent =
        formatStatus(
            report.status
        );


    document.getElementById(
        "modalConfidence"
    ).textContent =
        report.confidence ?? "-";


    document.getElementById(
        "modalLocation"
    ).textContent =
        report.location || "-";


    document.getElementById(
        "modalSummary"
    ).textContent =
        report.summary || "-";


    document.getElementById(
        "modalSuggestedAction"
    ).textContent =
        report.suggestedAction ||
        report.suggested_action ||
        "-";


    document.getElementById(
        "modalIncidentCount"
    ).textContent =
        `${reportCount} ${
            reportCount === 1
                ? "report"
                : "reports"
        } linked to this incident`;


    document.getElementById(
        "modalIncidentId"
    ).textContent =
        incident.incidentId;


    renderLinkedReports(
        incident.reports
    );


    renderIncidentActivities(
        incident.reports
    );


    modal.classList.add(
        "active"
    );


    document.body.classList.add(
        "modal-open"
    );
}


function renderLinkedReports(reports) {

    const container =
        document.getElementById(
            "modalLinkedReports"
        );


    if (!reports.length) {

        container.innerHTML = `
            <p class="activity-empty">
                No linked reports found.
            </p>
        `;

        return;
    }


    container.innerHTML =
        reports
            .map(
                (report, index) => {

                    const similarity =
                        report.duplicateSimilarity ??
                        report.duplicate_similarity;


                    let duplicateHtml = "";


                    if (
                        report.possibleDuplicate ||
                        report.possible_duplicate
                    ) {

                        let similarityText = "";


                        if (
                            similarity !== null &&
                            similarity !== undefined
                        ) {

                            similarityText =
                                ` · Similarity: ${(
                                    similarity * 100
                                ).toFixed(2)}%`;
                        }


                        duplicateHtml = `
                            <div class="linked-report-duplicate">
                                Possible Duplicate
                                ${similarityText}
                            </div>
                        `;
                    }


                    return `
                        <div class="linked-report-card">

                            <div class="linked-report-header">

                                <strong>
                                    Report ${index + 1}
                                </strong>

                                ${
                                    index === 0 &&
                                    !report.possibleDuplicate
                                        ? `
                                            <span class="primary-report-label">
                                                Primary Report
                                            </span>
                                        `
                                        : ""
                                }

                            </div>


                            <div class="linked-report-person">

                                <div>

                                    <span>
                                        Reporter
                                    </span>

                                    <strong>
                                        ${escapeHtml(
                                            report.name ||
                                            "Anonymous"
                                        )}
                                    </strong>

                                </div>


                                <div>

                                    <span>
                                        Contact
                                    </span>

                                    <strong>
                                        ${escapeHtml(
                                            report.contact ||
                                            "Not provided"
                                        )}
                                    </strong>

                                </div>

                            </div>


                            <div class="linked-report-description">

                                <span>
                                    Original Description
                                </span>

                                <p>
                                    ${escapeHtml(
                                        report.description ||
                                        "-"
                                    )}
                                </p>

                            </div>


                            ${duplicateHtml}

                        </div>
                    `;
                }
            )
            .join("");
}


function renderIncidentActivities(reports) {

    const activityContainer =
        document.getElementById(
            "modalActivities"
        );


    const activities = [];


    reports.forEach(report => {

        const reportActivities =
            report.activities || [];


        reportActivities.forEach(
            activity => {

                activities.push({
                    ...activity,

                    reporter:
                        report.name ||
                        "Anonymous"
                });
            }
        );
    });


    activities.sort(
        (firstActivity, secondActivity) =>

            new Date(
                secondActivity.createdAt
            ) -

            new Date(
                firstActivity.createdAt
            )
    );


    if (activities.length === 0) {

        activityContainer.innerHTML = `
            <p class="activity-empty">
                No activity recorded.
            </p>
        `;

        return;
    }


    activityContainer.innerHTML =
        activities
            .map(activity => `

                <div class="activity-item">

                    <div class="activity-dot"></div>


                    <div class="activity-content">

                        <strong>
                            ${escapeHtml(
                                activity.actionDisplay
                            )}
                        </strong>


                        <p>
                            ${formatStatus(
                                activity.oldStatus
                            )}

                            →

                            ${formatStatus(
                                activity.newStatus
                            )}
                        </p>


                        <span>
                            Reporter:
                            ${escapeHtml(
                                activity.reporter
                            )}

                            ·

                            ${formatActivityTime(
                                activity.createdAt
                            )}
                        </span>

                    </div>

                </div>

            `)
            .join("");
}


function formatActivityTime(dateValue) {

    if (!dateValue) {
        return "-";
    }


    const date =
        new Date(dateValue);


    return date.toLocaleString();
}


function closeReportModal() {

    const modal =
        document.getElementById(
            "reportModal"
        );


    modal.classList.remove(
        "active"
    );


    document.body.classList.remove(
        "modal-open"
    );
}


refreshButton.addEventListener(
    "click",
    loadDashboard
);


[
    categoryFilter,
    urgencyFilter,
    statusFilter,
    orderingFilter

].forEach(filter => {

    filter.addEventListener(
        "change",
        loadReports
    );
});


document.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Escape") {

            closeReportModal();
        }
    }
);


const AUTO_REFRESH_INTERVAL =
    15000;


setInterval(
    async function () {

        const modal =
            document.getElementById(
                "reportModal"
            );


        if (
            modal.classList.contains(
                "active"
            )
        ) {
            return;
        }


        await loadDashboard();

    },

    AUTO_REFRESH_INTERVAL
);


loadDashboard();