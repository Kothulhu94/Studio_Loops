const els = {
  modelLine: document.querySelector("#modelLine"),
  koboldBadge: document.querySelector("#koboldBadge"),
  updatedAt: document.querySelector("#updatedAt"),
  koboldStatus: document.querySelector("#koboldStatus"),
  loopStatus: document.querySelector("#loopStatus"),
  stageStatus: document.querySelector("#stageStatus"),
  centralPath: document.querySelector("#centralPath"),
  generationPath: document.querySelector("#generationPath"),
  currentPrompt: document.querySelector("#currentPrompt"),
  currentResponse: document.querySelector("#currentResponse"),
  promptMeta: document.querySelector("#promptMeta"),
  responseMeta: document.querySelector("#responseMeta"),
  historyCount: document.querySelector("#historyCount"),
  historyList: document.querySelector("#historyList"),
  koboldLog: document.querySelector("#koboldLog"),
  centralLog: document.querySelector("#centralLog"),
  commandSelect: document.querySelector("#commandSelect"),
  commandState: document.querySelector("#commandState"),
  taskInput: document.querySelector("#taskInput"),
  runCommand: document.querySelector("#runCommand"),
  killLoop: document.querySelector("#killLoop"),
  stopModel: document.querySelector("#stopModel"),
  autoScroll: document.querySelector("#autoScroll"),
  refreshNow: document.querySelector("#refreshNow"),
  lastBatchTokens: document.querySelector("#lastBatchTokens"),
  tokensPerSec: document.querySelector("#tokensPerSec"),
  diagnosticSummary: document.querySelector("#diagnosticSummary"),
  diagnosticList: document.querySelector("#diagnosticList"),
  performanceList: document.querySelector("#performanceList"),
  performanceAverages: document.querySelector("#performanceAverages"),
  kvList: document.querySelector("#kvList"),
  kvStatus: document.querySelector("#kvStatus"),
};

let commandMap = {};

function text(value, fallback = "--") {
  if (value === null || value === undefined || value === "") return fallback;
  if (typeof value === "string") return value;
  return JSON.stringify(value, null, 2);
}

function short(value, length = 96) {
  const out = text(value, "");
  return out.length > length ? `${out.slice(0, length)}...` : out;
}

function showBadge(ok) {
  els.koboldBadge.className = ok ? "badge badgeGood" : "badge badgeBad";
  els.koboldBadge.textContent = ok ? "Kobold online" : "Kobold offline";
}

function renderHistory(history) {
  els.historyCount.textContent = String(history.length);
  els.historyList.innerHTML = "";
  if (!history.length) {
    const empty = document.createElement("p");
    empty.className = "empty";
    empty.textContent = "No generations captured yet.";
    els.historyList.appendChild(empty);
    return;
  }

  for (const item of [...history].reverse()) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "historyItem";
    const prompt = item.prompt_text || item.prompt || "";
    const response = item.response || "";
    const time = document.createElement("span");
    time.className = "historyTime";
    time.textContent = text(item.timestamp, "unknown time");
    const title = document.createElement("strong");
    title.textContent = short(prompt, 90) || "Prompt captured";
    const body = document.createElement("span");
    body.textContent = short(response, 140) || "No response text";
    button.append(time, title, body);
    button.addEventListener("click", () => {
      els.currentPrompt.textContent = text(prompt, "No prompt captured.");
      els.currentResponse.textContent = text(response, "No response captured.");
      els.promptMeta.textContent = text(item.prompt_path || item.source, "");
      els.responseMeta.textContent = text(item.response_path || item.timestamp, "");
    });
    els.historyList.appendChild(button);
  }
}

function renderPerformance(history) {
  const statsItems = history.filter(item => item.prompt_tokens || item.tps);
  els.performanceList.innerHTML = "";

  if (!statsItems.length) {
    const tr = document.createElement("tr");
    tr.innerHTML = '<td colspan="4" class="empty">No performance data captured yet.</td>';
    els.performanceList.appendChild(tr);
    els.performanceAverages.textContent = "-- avg tokens | -- avg t/s";
    return;
  }

  let totalTokens = 0;
  let totalTps = 0;
  let count = statsItems.length;

  for (const item of [...statsItems].reverse()) {
    const tr = document.createElement("tr");
    
    const timeTd = document.createElement("td");
    timeTd.textContent = text(item.timestamp, "unknown").split('T')[1] || text(item.timestamp, "unknown");
    
    const tokensTd = document.createElement("td");
    const combined = (item.prompt_tokens || 0) + (item.completion_tokens || 0);
    tokensTd.textContent = combined || "--";
    totalTokens += combined;

    const tpsTd = document.createElement("td");
    tpsTd.textContent = item.tps ? `${item.tps} t/s` : "--";
    totalTps += (item.tps || 0);

    const durTd = document.createElement("td");
    durTd.textContent = item.duration ? `${item.duration.toFixed(1)}s` : "--";

    tr.append(timeTd, tokensTd, tpsTd, durTd);
    els.performanceList.appendChild(tr);
  }

  const avgTokens = Math.round(totalTokens / count);
  const avgTps = (totalTps / count).toFixed(2);
  els.performanceAverages.textContent = `${avgTokens} avg tokens | ${avgTps} avg t/s`;
}

function renderKV(events) {
  els.kvList.innerHTML = "";
  if (!events || !events.length) {
    const empty = document.createElement("p");
    empty.className = "empty";
    empty.textContent = "Waiting for KV cache activity...";
    els.kvList.appendChild(empty);
    els.kvStatus.textContent = "Idle";
    return;
  }

  els.kvStatus.textContent = `${events.length} recent events`;

  for (const event of [...events].reverse()) {
    const div = document.createElement("div");
    div.className = `kvItem kv-${event.type}`;
    
    const label = document.createElement("strong");
    label.textContent = event.type.replace("_", " ").toUpperCase();
    
    const info = document.createElement("span");
    info.textContent = event.text;
    
    div.append(label, info);
    els.kvList.appendChild(div);
  }
}

function render(snapshot) {
  const central = snapshot.central_state || {};
  const agent = snapshot.agent_state || {};
  const kobold = snapshot.kobold || {};
  const current = snapshot.current || {};
  const running = Boolean(snapshot.orchestrator?.running);
  const modelLabel = central.model_label || "KoboldCPP";

  els.modelLine.textContent = `${modelLabel}${central.model_path ? ` - ${central.model_path}` : ""}`;
  els.updatedAt.textContent = snapshot.generated_at || "--";
  showBadge(Boolean(kobold.reachable));
  els.koboldStatus.textContent = kobold.reachable
    ? `Online at ${kobold.base_url}`
    : `Offline at ${kobold.base_url || "127.0.0.1:5001"}`;
  els.loopStatus.textContent = `${text(agent.status, "idle")}${agent.active ? " (active)" : ""}`;
  if (snapshot.orchestrator?.process_dead) {
    els.loopStatus.textContent += " - stalled (crashed?)";
    els.loopStatus.className = "stalledText";
  } else {
    els.loopStatus.className = "";
  }
  els.stageStatus.textContent = text(agent.current_stage || agent.feature_slug);
  els.centralPath.textContent = snapshot.paths?.central_log || "--";
  els.generationPath.textContent = snapshot.paths?.generations || "--";
  els.commandState.textContent = running ? "Running" : "Idle";
  els.commandState.className = running ? "muted runningText" : "muted";

  els.currentPrompt.textContent = text(current.prompt_text || current.prompt, "No prompt captured yet.");
  els.currentResponse.textContent = text(current.response, "No response captured yet.");
  els.promptMeta.textContent = text(current.prompt_path || current.source, "");
  els.responseMeta.textContent = text(current.response_path || current.timestamp, "");

  els.koboldLog.textContent = snapshot.logs?.kobold || "No KoboldCPP output captured yet.";
  els.centralLog.textContent = snapshot.logs?.central || "No Loop_Central commands yet.";

  // Stats
  const stats = central.last_stats || current || {};
  if (stats.prompt_tokens) {
    els.lastBatchTokens.textContent = `${stats.prompt_tokens} tokens`;
  } else {
    els.lastBatchTokens.textContent = "--";
  }

  if (stats.tps) {
    els.tokensPerSec.textContent = `${stats.tps} t/s`;
  } else {
    els.tokensPerSec.textContent = "--";
  }

  if (els.autoScroll.checked) {
    els.koboldLog.scrollTop = els.koboldLog.scrollHeight;
    els.centralLog.scrollTop = els.centralLog.scrollHeight;
  }

  renderHistory(snapshot.history || []);
  renderPerformance(snapshot.history || []);
  renderKV(snapshot.kv_events || []);
}

function renderDiagnostics(report) {
  if (!report || !report.checks) return;
  
  els.diagnosticSummary.textContent = report.summary || "Complete";
  els.diagnosticSummary.className = report.summary === "System Healthy" ? "badge badgeGood" : "badge badgeBad";
  
  els.diagnosticList.innerHTML = "";
  for (const check of report.checks) {
    const li = document.createElement("li");
    li.className = `diagItem diag-${check.status.toLowerCase()}`;
    
    const name = document.createElement("strong");
    name.textContent = check.name;
    
    const msg = document.createElement("span");
    msg.textContent = check.message;
    
    li.append(name, msg);
    els.diagnosticList.appendChild(li);
  }
}

async function loadCommands() {
  const response = await fetch("/api/orchestrator/commands", { cache: "no-store" });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const data = await response.json();
  commandMap = data.commands || {};
  els.commandSelect.innerHTML = "";
  for (const [value, spec] of Object.entries(commandMap)) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = spec.label || value;
    els.commandSelect.appendChild(option);
  }
  if (commandMap.continue) {
    els.commandSelect.value = "continue";
  }
}

function payloadFor(command) {
  const mode = commandMap[command]?.payload || "none";
  if (mode === "none") return "";
  return els.taskInput.value.trim();
}

async function sendCommand(command) {
  if (command === "reset" && !confirm("Reset Studio Loop state and generated artifacts?")) return;
  const payload = payloadFor(command);
  const mode = commandMap[command]?.payload || "none";
  if (mode !== "none" && !payload) {
    els.commandState.textContent = "Input required";
    return;
  }
  els.commandState.textContent = "Starting";
  const response = await fetch("/api/orchestrator/command", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ command, payload }),
  });
  const result = await response.json();
  if (!response.ok || !result.ok) {
    els.commandState.textContent = result.error || `HTTP ${response.status}`;
    return;
  }
  els.commandState.textContent = `Started ${command}`;
  refresh();
}

async function killLoop() {
  if (!confirm("Kill the active Studio Loop command?")) return;
  els.commandState.textContent = "Killing";
  const response = await fetch("/api/orchestrator/stop", { method: "POST" });
  const result = await response.json();
  els.commandState.textContent = result.ok ? "Loop stopped" : result.error || "Kill failed";
  refresh();
}

async function stopModel() {
  if (!confirm("Stop the running KoboldCPP model process?")) return;
  els.commandState.textContent = "Stopping model";
  const response = await fetch("/api/model/stop", { method: "POST" });
  const result = await response.json();
  els.commandState.textContent = result.ok ? "Model stopped" : result.error || "Stop failed";
  refresh();
}

async function refresh() {
  try {
    const [snapResp, diagResp] = await Promise.all([
        fetch("/api/snapshot", { cache: "no-store" }),
        fetch("/api/diagnostics", { cache: "no-store" })
    ]);
    
    if (!snapResp.ok) throw new Error(`Snapshot HTTP ${snapResp.status}`);
    render(await snapResp.json());
    
    if (diagResp.ok) {
        renderDiagnostics(await diagResp.json());
    }
  } catch (error) {
    console.error("Refresh error:", error);
    els.updatedAt.textContent = `UI refresh failed: ${error.message}`;
    showBadge(false);
  }
}

els.refreshNow.addEventListener("click", refresh);
els.runCommand.addEventListener("click", () => sendCommand(els.commandSelect.value));
els.killLoop.addEventListener("click", killLoop);
els.stopModel.addEventListener("click", stopModel);
document.querySelectorAll("[data-command]").forEach((button) => {
  button.addEventListener("click", () => sendCommand(button.dataset.command));
});

loadCommands().catch((error) => {
  els.commandState.textContent = `Commands unavailable: ${error.message}`;
});
refresh();
setInterval(refresh, 2000);
