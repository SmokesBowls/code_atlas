// Code Atlas Report Viewer - Frontend Javascript

document.addEventListener("DOMContentLoaded", () => {
    fetchReport();
});

async function fetchReport() {
    try {
        const response = await fetch("/api/report");
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const report = await response.json();
        
        if (report.error) {
            renderErrorPage(report.error);
            return;
        }
        
        renderReport(report);
    } catch (err) {
        renderErrorPage(`Failed to load report from server: ${err.message}`);
    }
}

function renderErrorPage(message) {
    const container = document.querySelector(".app-container");
    container.innerHTML = `
        <div class="panel" style="border-color: var(--color-gap); background-color: rgba(218, 54, 51, 0.05);">
            <h2 style="color: #ff7b72;">⚠️ Error Loading Code Atlas Report</h2>
            <p class="section-desc" style="color: var(--text-primary); margin-top: 12px; font-size: 14px;">
                ${message}
            </p>
            <p style="margin-top: 16px; font-size: 12px; color: var(--text-secondary);">
                Please verify that the server started successfully and the selected report JSON file exists and contains valid JSON metadata.
            </p>
        </div>
    `;
}

function renderReport(report) {
    // 1. Render Provenance & Header
    const provDiv = document.getElementById("provenance");
    const scannedAt = report.scanned_at ? new Date(report.scanned_at).toLocaleString() : "Unknown";
    const reportPath = report.viewer_provenance ? report.viewer_provenance.report_path : "Unknown";
    provDiv.innerHTML = `
        <p><strong>Project:</strong> ${report.project_name || "Unknown"}</p>
        <p><strong>Report:</strong> ${reportPath}</p>
        <p><strong>Scanned At:</strong> ${scannedAt}</p>
    `;

    // (Old top download buttons removed)

    // 2. Metadata Totals
    const files = report.files || {};
    const parseErrors = report.parse_errors || [];
    const entrypoints = Object.keys(files).filter(k => files[k].is_entrypoint);

    document.getElementById("total-files").textContent = Object.keys(files).length;
    document.getElementById("total-errors").textContent = parseErrors.length;
    document.getElementById("entrypoints-list").textContent = entrypoints.length > 0 ? entrypoints.join(", ") : "None";

    // 3. Status Distribution
    const statusCounts = {
        likely_active: 0,
        stubbed: 0,
        orphaned: 0,
        dormant: 0,
        unresolved: 0
    };
    
    Object.values(files).forEach(f => {
        const statusVal = f.status && f.status.status ? f.status.status : "unresolved";
        if (statusCounts[statusVal] !== undefined) {
            statusCounts[statusVal]++;
        } else {
            statusCounts.unresolved++;
        }
    });

    const statusCountsDiv = document.getElementById("status-counts");
    statusCountsDiv.innerHTML = "";
    
    const statusesToRender = [
        { key: "likely_active", label: "Likely Active (Static reachability)" },
        { key: "stubbed", label: "Stubbed" },
        { key: "orphaned", label: "Orphaned" },
        { key: "dormant", label: "Dormant" },
        { key: "unresolved", label: "Unresolved" }
    ];

    statusesToRender.forEach(s => {
        const row = document.createElement("div");
        row.className = "status-row";
        row.innerHTML = `
            <span class="status-label">
                <span class="status-dot dot-${s.key}"></span>
                ${s.label}
            </span>
            <span class="status-count">${statusCounts[s.key]}</span>
        `;
        statusCountsDiv.appendChild(row);
    });

    // Add explicit runtime active indicator (which is locked/unsupported at 0)
    const runtimeActiveRow = document.createElement("div");
    runtimeActiveRow.className = "status-row";
    runtimeActiveRow.innerHTML = `
        <span class="status-label" style="opacity: 0.6;">
            <span class="status-dot dot-active"></span>
            Active (Runtime-confirmed)
        </span>
        <span class="status-count" style="opacity: 0.6;">0</span>
    `;
    statusCountsDiv.appendChild(runtimeActiveRow);

    // 4. Parse Errors & Gaps Table
    const gapsBody = document.getElementById("gaps-table-body");
    gapsBody.innerHTML = "";
    
    if (parseErrors.length === 0) {
        gapsBody.innerHTML = `
            <tr>
                <td colspan="3" style="text-align: center; color: var(--text-secondary); font-style: italic;">
                    No parse errors or unresolved gaps detected.
                </td>
            </tr>
        `;
    } else {
        parseErrors.forEach(pe => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><code>${pe.filepath}</code></td>
                <td><span class="claim-badge badge-gap">gap</span> ${pe.error}</td>
                <td><span style="text-transform: capitalize;">${pe.confidence || "high"}</span></td>
            `;
            gapsBody.appendChild(tr);
        });
    }

    // 5. Ranked Next Files to Inspect Table (Advisory)
    const rankingsBody = document.getElementById("rankings-table-body");
    rankingsBody.innerHTML = "";
    const rankings = report.next_files_to_inspect || [];

    if (rankings.length === 0) {
        rankingsBody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align: center; color: var(--text-secondary); font-style: italic;">
                    No next files prioritization generated.
                </td>
            </tr>
        `;
    } else {
        rankings.forEach((item, index) => {
            const reasonsHtml = item.reasons.map(r => `<code>${r}</code>`).join(" ");
            const evidenceHtml = item.evidence.map(e => `<li>${e}</li>`).join("");
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td style="font-weight: 600; text-align: center;">${index + 1}</td>
                <td><code>${item.filepath}</code></td>
                <td><strong style="color: var(--color-advisory);">${item.score}</strong></td>
                <td>${reasonsHtml}</td>
                <td><ul style="padding-left: 16px; font-size: 12px; color: var(--text-secondary);">${evidenceHtml}</ul></td>
            `;
            rankingsBody.appendChild(tr);
        });
    }

    // 6. Candidate Subsystem Groups (Inferred)
    const subsystemsContainer = document.getElementById("subsystems-container");
    subsystemsContainer.innerHTML = "";
    const groups = report.candidate_subsystem_groups || [];

    if (groups.length === 0) {
        subsystemsContainer.innerHTML = `
            <div style="color: var(--text-secondary); font-style: italic; text-align: center; padding: 12px;">
                No candidate subsystem groups detected.
            </div>
        `;
    } else {
        // Sort groups for display by member count or name
        const sortedGroups = [...groups].sort((a, b) => a.name.localeCompare(b.name));
        sortedGroups.forEach(g => {
            const isAmbig = g.structurally_ambiguous;
            const evidenceHtml = g.evidence.map(ev => `<li>${ev}</li>`).join("");
            const basisHtml = g.grouping_basis.map(b => `<code>${b}</code>`).join(" ");
            
            const card = document.createElement("div");
            card.className = `subsystem-card ${isAmbig ? "ambiguous" : ""}`;
            card.innerHTML = `
                <div class="subsystem-header">
                    <span class="subsystem-title">
                        ${g.name}
                        ${isAmbig ? '<span class="claim-badge badge-gap">Ambiguous</span>' : ""}
                        <span class="claim-badge badge-inferred">Inferred Candidate</span>
                    </span>
                    <span class="subsystem-meta">Confidence: <strong>${g.confidence}</strong></span>
                </div>
                <div class="subsystem-body">
                    <div class="subsystem-files">
                        <h4>Member Files (${g.member_files.length})</h4>
                        <ul class="file-list">
                            ${g.member_files.map(f => `<li>• <code>${f}</code></li>`).join("")}
                        </ul>
                    </div>
                    <div class="subsystem-details">
                        <h4>Details & Dependencies</h4>
                        <p><strong>Grouping Basis:</strong> ${basisHtml}</p>
                        <p><strong>Internal Links:</strong> <code>${g.internal_edge_count || 0}</code></p>
                        <p><strong>External Links:</strong> <code>${g.external_edge_count || 0}</code></p>
                        <h4 style="margin-top: 10px; font-size: 11px;">Inbound Interfaces (${g.inbound_interface_files.length})</h4>
                        <ul class="file-list" style="margin-bottom: 8px;">
                            ${g.inbound_interface_files.length > 0 
                                ? g.inbound_interface_files.map(f => `<li><code>${f}</code></li>`).join("") 
                                : '<li style="color: var(--text-secondary); font-style: italic;">None</li>'}
                        </ul>
                        <h4 style="font-size: 11px;">Outbound Interfaces (${g.outbound_interface_files.length})</h4>
                        <ul class="file-list">
                            ${g.outbound_interface_files.length > 0 
                                ? g.outbound_interface_files.map(f => `<li><code>${f}</code></li>`).join("") 
                                : '<li style="color: var(--text-secondary); font-style: italic;">None</li>'}
                        </ul>
                    </div>
                </div>
                <div style="margin-top: 16px; border-top: 1px dashed var(--border-color); padding-top: 10px;">
                    <h4 style="font-size: 12px; margin-bottom: 4px; color: var(--text-secondary); text-transform: uppercase;">Evidence Log</h4>
                    <ul style="padding-left: 16px; font-size: 12px; color: var(--text-secondary);">${evidenceHtml}</ul>
                </div>
            `;
            subsystemsContainer.appendChild(card);
        });
    }

    // 7. Static Dependency Routes (Inferred)
    const routesContainer = document.getElementById("routes-container");
    routesContainer.innerHTML = "";
    const routes = report.routes || [];

    if (routes.length === 0) {
        routesContainer.innerHTML = `
            <div style="color: var(--text-secondary); font-style: italic; text-align: center; padding: 12px;">
                No static dependency routes resolved.
            </div>
        `;
    } else {
        routes.forEach(r => {
            const card = document.createElement("div");
            card.className = "route-card";
            card.innerHTML = `
                <div class="route-header">
                    <span class="route-title">
                        Static Route from: <code>${r.entrypoint}</code>
                        <span class="claim-badge badge-inferred">Static dependency route</span>
                    </span>
                    <span class="route-meta">Confidence: <strong>${r.confidence}</strong></span>
                </div>
                <div class="route-flow">
                    ${r.route_files.map((file, idx) => {
                        const isEntry = file === r.entrypoint;
                        let tagsHtml = "";
                        
                        // Check boundary crossing
                        const crossing = r.boundary_crossings.find(bc => bc.file === file);
                        if (crossing) {
                            tagsHtml += `<span class="boundary-cross-tag">Boundary: ${crossing.from} ➔ ${crossing.to}</span> `;
                        }
                        
                        // Check stub or error status
                        if (r.stubbed_files.includes(file)) {
                            tagsHtml += `<span class="stub-tag">STUB</span> `;
                        }
                        if (r.parse_error_files.includes(file)) {
                            tagsHtml += `<span class="parse-error-tag">PARSE ERROR</span> `;
                        }
                        if (r.unresolved_files.includes(file)) {
                            tagsHtml += `<span class="parse-error-tag">UNRESOLVED</span> `;
                        }

                        return `
                            <div class="flow-node ${isEntry ? "entrypoint" : ""}">
                                <span class="node-name">${file} ${isEntry ? '<strong>(Entry)</strong>' : ""}</span>
                                <span class="node-dash"></span>
                                <div class="node-flags">
                                    ${tagsHtml}
                                </div>
                            </div>
                        `;
                    }).join("")}
                </div>
                <div style="margin-top: 16px; border-top: 1px dashed var(--border-color); padding-top: 10px; font-size: 13px;">
                    <p>🎯 <strong>Advisory Next Inspection Step:</strong> <code>${r.next_file_to_inspect_in_route || "None"}</code></p>
                </div>
            `;
            routesContainer.appendChild(card);
        });
     }

    // 8. Wire up new payload card viewing & downloading handlers
    const prov = report.viewer_provenance || {};
    
    if (prov.has_ai_json) {
        document.getElementById("card-ai-json").style.display = "flex";
    } else {
        document.getElementById("card-ai-json").style.display = "none";
    }
    
    if (prov.has_ai_markdown) {
        document.getElementById("card-ai-md").style.display = "flex";
    } else {
        document.getElementById("card-ai-md").style.display = "none";
    }
    
    const codeBlock = document.getElementById("payload-code-block");
    const viewerTitle = document.getElementById("payload-viewer-title");
    const copyBtn = document.getElementById("btn-copy-payload");
    
    const showPayloadContent = (title, text) => {
        viewerTitle.textContent = `Payload Content Viewer: ${title}`;
        codeBlock.textContent = text;
        copyBtn.style.display = "block";
        
        copyBtn.onclick = async () => {
            try {
                await navigator.clipboard.writeText(text);
                const originalText = copyBtn.textContent;
                copyBtn.textContent = "Copied!";
                setTimeout(() => { copyBtn.textContent = originalText; }, 2000);
            } catch (err) {
                alert("Failed to copy content: " + err);
            }
        };
    };

    const viewButtons = document.querySelectorAll("#payloads-section .view-btn");
    const downloadButtons = document.querySelectorAll("#payloads-section .download-btn");
    
    viewButtons.forEach(btn => {
        btn.onclick = async () => {
            const type = btn.getAttribute("data-payload");
            codeBlock.textContent = "Loading payload content...";
            copyBtn.style.display = "none";
            
            try {
                if (type === "json") {
                    const cleanReport = { ...report };
                    delete cleanReport.viewer_provenance;
                    showPayloadContent("Standard Report (JSON)", JSON.stringify(cleanReport, null, 2));
                } else if (type === "markdown") {
                    const res = await fetch("/api/report/markdown");
                    if (!res.ok) throw new Error("File not found on server.");
                    const text = await res.text();
                    showPayloadContent("Standard Report (Markdown)", text);
                } else if (type === "ai-json") {
                    const res = await fetch("/api/report/ai_json");
                    if (!res.ok) throw new Error("File not found on server.");
                    const text = await res.text();
                    const parsed = JSON.parse(text);
                    showPayloadContent("AI Architecture (JSON)", JSON.stringify(parsed, null, 2));
                } else if (type === "ai-md") {
                    const res = await fetch("/api/report/ai_markdown");
                    if (!res.ok) throw new Error("File not found on server.");
                    const text = await res.text();
                    showPayloadContent("AI Architecture (Markdown)", text);
                }
            } catch (err) {
                showPayloadContent("Error Loading Payload", `Error: ${err.message}`);
            }
        };
    });
    
    downloadButtons.forEach(btn => {
        btn.onclick = () => {
            const type = btn.getAttribute("data-payload");
            if (type === "json") {
                const cleanReport = { ...report };
                delete cleanReport.viewer_provenance;
                const blob = new Blob([JSON.stringify(cleanReport, null, 2)], { type: "application/json" });
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = report.project_name ? `${report.project_name}_report.json` : "report.json";
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            } else if (type === "markdown") {
                window.location.href = "/api/report/markdown";
            } else if (type === "ai-json") {
                window.location.href = "/api/report/ai_json";
            } else if (type === "ai-md") {
                window.location.href = "/api/report/ai_markdown";
            }
        };
    });
    
    document.getElementById("btn-download-combined").onclick = () => {
        window.location.href = "/api/report/all_payloads";
    };

    // 9. Render Payload Handoff Diagnostics (Milestone 9)
    const connectedContainer = document.getElementById("connected-handoffs-container");
    const likelyContainer = document.getElementById("likely-handoffs-container");
    const unresolvedRoutesContainer = document.getElementById("unresolved-routes-container");
    const producerContainer = document.getElementById("producer-outputs-container");
    const consumerContainer = document.getElementById("consumer-inputs-container");
    
    connectedContainer.innerHTML = "";
    likelyContainer.innerHTML = "";
    unresolvedRoutesContainer.innerHTML = "";
    producerContainer.innerHTML = "";
    consumerContainer.innerHTML = "";
    
    const handoffs = report.payload_handoffs || [];
    const unresolved = report.unresolved_payload_routes || [];
    
    function getHandoffCardHtml(h) {
        const statusClass = h.route_status === "connected" 
            ? "badge-status-full" 
            : h.route_status === "connected_partial"
            ? "badge-status-partial"
            : h.route_status === "likely_connected" 
            ? "badge-status-partial" 
            : h.route_status === "ambiguous_consumer"
            ? "badge-status-partial"
            : "badge-status-unused";
            
        const statusLabel = h.route_status === "connected"
            ? "Connected (Fully Consumed)"
            : h.route_status === "connected_partial"
            ? "Connected (Partially Consumed)"
            : h.route_status === "connected_unused"
            ? "Connected (Unused)"
            : h.route_status === "likely_connected"
            ? "Likely Connected"
            : h.route_status === "ambiguous_consumer"
            ? "Ambiguous Consumer"
            : "Unused";
            
        const claimBadge = `<span class="claim-badge badge-${h.claim_type || 'confirmed'}">${h.claim_type || 'confirmed'}</span>`;
        const crossBadge = h.consumers[0] && h.producer.component !== h.consumers[0].component
            ? `<span class="claim-badge badge-cross-boundary">Cross-Boundary</span>` 
            : "";
            
        const shape = h.observed_shape || {};
        const keysHtml = (shape.keys || []).map(k => {
            const utilized = (shape.utilized_keys || []).includes(k);
            const color = utilized ? "#39db64" : "#f85149";
            const icon = utilized ? "✓" : "✗";
            return `<code style="color: ${color}; margin-right: 8px;">${icon} ${k}</code>`;
        }).join(" ");
        
        const evidenceHtml = (h.evidence || []).map(e => `<li>${e}</li>`).join("");
        const limitationsHtml = (h.limitations || []).map(l => `<li>${l}</li>`).join("");
        
        const consumersHtml = h.consumers.map(c => `
            <div class="flow-actor">
                <h4>Consumer</h4>
                <p><strong>File:</strong> <code>${c.file}</code></p>
                <p><strong>Function:</strong> <code>${c.function}()</code></p>
                <p><strong>Component:</strong> <code>${c.component}</code></p>
                <p><strong>Detail:</strong> ${c.evidence || 'N/A'}</p>
            </div>
        `).join('<div class="flow-connector">➔</div>');
        
        return `
            <div class="handoff-card">
                <div class="handoff-header">
                    <span class="handoff-title">
                        Candidate: <code>${h.observed_name || "dict"}</code>
                        ${claimBadge}
                        ${crossBadge}
                    </span>
                    <span class="claim-badge ${statusClass}">${statusLabel}</span>
                </div>
                <div class="handoff-flow-container">
                    <div class="flow-actor">
                        <h4>Producer</h4>
                        <p><strong>File:</strong> <code>${h.producer.file}</code></p>
                        <p><strong>Function:</strong> <code>${h.producer.function}()</code></p>
                        <p><strong>Component:</strong> <code>${h.producer.component}</code></p>
                    </div>
                    <div class="flow-connector">➔</div>
                    ${consumersHtml}
                </div>
                <div style="margin-top: 12px; font-size: 13px;">
                    <p style="margin-bottom: 6px;"><strong>Keys Utilization Map:</strong></p>
                    <div style="background-color: #0d1117; border: 1px solid var(--border-color); border-radius: 4px; padding: 8px;">
                        ${keysHtml || '<span style="color: var(--text-secondary); font-style: italic;">No key metadata available</span>'}
                    </div>
                </div>
                <div style="margin-top: 12px; border-top: 1px dashed var(--border-color); padding-top: 10px; font-size: 12px; color: var(--text-secondary); display: flex; gap: 24px;">
                    <div style="flex: 1;">
                        <strong>Diagnostic Evidence:</strong>
                        <ul style="padding-left: 16px; margin-top: 4px;">
                            ${evidenceHtml}
                        </ul>
                    </div>
                    <div style="flex: 1;">
                        <strong>Analysis Limitations:</strong>
                        <ul style="padding-left: 16px; margin-top: 4px;">
                            ${limitationsHtml}
                        </ul>
                    </div>
                </div>
            </div>
        `;
    }
    
    let hasConnected = false;
    let hasLikely = false;
    
    handoffs.forEach(h => {
        const html = getHandoffCardHtml(h);
        if (h.route_status.startsWith("connected")) {
            connectedContainer.innerHTML += html;
            hasConnected = true;
        } else if (h.route_status === "likely_connected" || h.route_status === "ambiguous_consumer") {
            likelyContainer.innerHTML += html;
            hasLikely = true;
        }
    });
    
    if (!hasConnected) {
        connectedContainer.innerHTML = `<div style="color: var(--text-secondary); font-style: italic; padding: 12px;">No confirmed connected handoffs in scope.</div>`;
    }
    if (!hasLikely) {
        likelyContainer.innerHTML = `<div style="color: var(--text-secondary); font-style: italic; padding: 12px;">No likely connected handoffs in scope.</div>`;
    }
    
    let hasUnresolved = false;
    let hasProducerOnly = false;
    let hasConsumerOnly = false;
    
    unresolved.forEach(un => {
        const claimBadge = `<span class="claim-badge badge-${un.claim_type || 'gap'}">${un.claim_type || 'gap'}</span>`;
        const evidenceHtml = (un.evidence || []).map(e => `<li>${e}</li>`).join("");
        
        let detailsHtml = "";
        let headerLabel = "";
        
        if (un.status === "producer_only") {
            headerLabel = "Producer Only Output";
            detailsHtml = `
                <p><strong>Producer File:</strong> <code>${un.producer.file}</code></p>
                <p><strong>Producer Function:</strong> <code>${un.producer.function}()</code></p>
                <p><strong>Component:</strong> <code>${un.producer.component}</code></p>
                <p><strong>Unresolved Reason:</strong> <code style="color: #f85149;">${un.reason}</code></p>
            `;
        } else {
            headerLabel = "Consumer Only Input";
            detailsHtml = `
                <p><strong>Consumer File:</strong> <code>${un.consumer.file}</code></p>
                <p><strong>Consumer Function:</strong> <code>${un.consumer.function}()</code></p>
                <p><strong>Component:</strong> <code>${un.consumer.component}</code></p>
                <p><strong>Unresolved Reason:</strong> <code style="color: #f85149;">${un.reason}</code></p>
            `;
        }
        
        const cardHtml = `
            <div class="unresolved-card">
                <div class="unresolved-header">
                    <span style="font-weight: 600; color: var(--text-primary);">
                        Unresolved Endpoint: <code>${un.payload_candidate_id.replace("unresolved_prod_", "").replace("unresolved_cons_", "")}</code>
                        ${claimBadge}
                    </span>
                </div>
                <div style="font-size: 13px; margin-top: 8px;">
                    ${detailsHtml}
                </div>
                <div style="margin-top: 12px; font-size: 12px; color: var(--text-secondary);">
                    <strong>Diagnostic Evidence:</strong>
                    <ul style="padding-left: 16px; margin-top: 4px;">
                        ${evidenceHtml}
                    </ul>
                </div>
            </div>
        `;
        
        if (un.status === "producer_only") {
            producerContainer.innerHTML += cardHtml;
            hasProducerOnly = true;
        } else if (un.status === "consumer_only") {
            consumerContainer.innerHTML += cardHtml;
            hasConsumerOnly = true;
        } else {
            unresolvedRoutesContainer.innerHTML += cardHtml;
            hasUnresolved = true;
        }
    });
    
    if (!hasUnresolved) {
        unresolvedRoutesContainer.innerHTML = `<div style="color: var(--text-secondary); font-style: italic; padding: 12px;">No generic unresolved routes.</div>`;
    }
    if (!hasProducerOnly) {
        producerContainer.innerHTML = `<div style="color: var(--text-secondary); font-style: italic; padding: 12px;">No producer-only outputs.</div>`;
    }
    if (!hasConsumerOnly) {
        consumerContainer.innerHTML = `<div style="color: var(--text-secondary); font-style: italic; padding: 12px;">No consumer-only inputs.</div>`;
    }
}
