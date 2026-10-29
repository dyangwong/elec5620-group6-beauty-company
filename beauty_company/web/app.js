"use strict";

const state = {actor: null, csrf: "", snapshot: null, view: "overview", busy: false, refreshVersion: 0};
const app = document.querySelector("#app");
const escapeHtml = value => String(value ?? "").replace(/[&<>"']/g, ch => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[ch]));
const e = escapeHtml;
const money = cents => new Intl.NumberFormat("en-AU", {style: "currency", currency: "AUD"}).format(cents / 100);
const label = value => String(value).toLowerCase().replaceAll("_", " ");
const modeLabel = () => state.snapshot?.mode.media === "TEMPLATE_VIDEO" ? `${state.snapshot.mode.mc} text · template video configured` : state.snapshot?.mode.ba === "LIVE" || state.snapshot?.mode.mc === "LIVE" ? `BA ${state.snapshot.mode.ba.toLowerCase()} · MC text ${state.snapshot.mode.mc.toLowerCase()} configured` : "Simulation mode";
const isFounder = () => state.actor?.role === "FOUNDER";
const records = kind => state.snapshot.records.filter(record => record.kind === kind);
const brand = () => '<div class="brand"><span class="brand-mark">b</span><div>Beauty Company<small>One founder. Connected expertise.</small></div></div>';

function badge(status) {
  const color = ["RESOLVED", "COMPLETED", "APPROVED", "DELIVERED", "AVAILABLE"].includes(status) ? "success"
    : ["REJECTED", "UNRESOLVED", "FAILED", "RECORDING_FAILED", "UNAVAILABLE"].includes(status) ? "danger"
    : ["REVIEW_PENDING", "PENDING", "AWAITING_CONFIRMATION", "AWAITING_APPROVAL", "RECONCILING"].includes(status) ? "pending" : "purple";
  return `<span class="badge ${color}">${e(label(status))}</span>`;
}

function empty(title, text, view = "", action = "") {
  return `<div class="empty"><div class="empty-icon">◇</div><h3>${e(title)}</h3><p>${e(text)}</p>${view ? `<button class="button secondary" data-view="${e(view)}">${e(action)}</button>` : ""}</div>`;
}

async function api(path, data) {
  const response = await fetch(path, {method: data === undefined ? "GET" : "POST", credentials: "same-origin",
    headers: data === undefined ? {} : {"Content-Type": "application/json", "X-CSRF-Token": state.csrf},
    body: data === undefined ? undefined : JSON.stringify(data)});
  const result = await response.json();
  if (!response.ok) throw new Error(result.error?.message || `Request failed (${response.status}).`);
  return result;
}

function toast(message, error = false) {
  const element = document.querySelector("#toast");
  element.textContent = message;
  element.className = `toast${error ? " error" : ""}`;
  element.hidden = false;
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => { element.hidden = true; }, error ? 9000 : 4500);
}

async function refresh() {
  const version = ++state.refreshVersion, actorId = state.actor?.id;
  const snapshot = await api("/api/snapshot");
  if (version !== state.refreshVersion || actorId !== state.actor?.id) return;
  state.snapshot = snapshot;
  state.actor = state.snapshot.actor;
  render();
}

function busyButtons(disabled) {
  document.querySelectorAll("button").forEach(button => {
    button.disabled = disabled && !["refresh", "ba-cancel", "mc-cancel"].includes(button.dataset.action);
  });
}

async function baControl(action, message) {
  // Refresh/cancel must stay usable while a separate model request is pending.
  try {
    await action();
    await refresh();
    if (message) toast(message);
  } catch (error) {
    let detail = error.message;
    try { await refresh(); } catch { detail += " Refresh before retrying."; }
    toast(detail, true);
  }
}

async function mutate(action, message, refreshOnError = false) {
  if (state.busy) return;
  state.busy = true;
  busyButtons(true);
  try {
    await action();
    if (state.actor) await refresh();
    else render();
    if (message) toast(message);
  } catch (error) {
    let detail = error.message;
    if (refreshOnError) {
      try { await refresh(); }
      catch { detail += " Workspace refresh failed; refresh before retrying."; }
    }
    toast(detail, true);
  } finally {
    state.busy = false;
    busyButtons(false);
  }
}

function loginView() {
  return `<main class="login"><section class="login-story">${brand()}<div class="login-copy"><div class="eyebrow">The founder-supervised company</div><h1>Small team.<br>Thoughtful beauty.<br><em>Visible decisions.</em></h1><p>A connected workspace for product advice, customer care and content — with a human in control of consequential decisions.</p><div class="role-chips"><span>Beauty Advisor</span><span>Customer Service</span><span>Marketing Content</span></div><div class="journey-mini"><b>BA</b><span></span><b>CS</b><span></span><b>MC</b><span></span><b>YOU</b></div></div><div class="login-note">ELEC5620 · Group 6 · Local prototype / 0.1</div></section><section class="login-form-wrap"><span class="eyebrow">Your local workspace</span><h2>Step inside the company.</h2><p>Explore the Customer or Founder experience using a fictional demo account.</p><form id="login-form"><div class="field"><label for="username">Workspace</label><select id="username" name="username"><option value="founder">Founder / Operator</option><option value="customer">Alex · Customer · ORD-1001</option><option value="customer-2">Sam · Customer · ORD-2001</option></select></div><div class="field"><label for="password">Demo password</label><input id="password" name="password" type="password" value="founder-demo" autocomplete="current-password" required><small id="credential-hint">Founder password: founder-demo</small></div><button class="button full" type="submit">Open demo workspace <span class="arrow">↗</span></button></form><div class="login-callout"><strong>Local prototype.</strong> BA and MC text modes are shown after sign-in. Media configuration is shown after sign-in. No real payment, shipment or public posting occurs.</div><p class="fineprint">These are shared local demo accounts, not personal accounts. All product and order data is synthetic.</p></section></main>`;
}

function navigation() {
  const pending = state.snapshot.approvals.filter(item => item.status === "PENDING").length;
  const items = isFounder()
    ? [["overview", "◫", "Overview"], ["requests", "⇄", "Customer requests"], ["approvals", "◇", "Review queue"], ["studio", "✧", "Content studio"], ["trace", "≋", "Activity trail"]]
    : [["overview", "◫", "Overview"], ["consult", "✧", "Product advice"], ["requests", "⇄", "After-sales care"], ["trace", "≋", "Activity trail"]];
  return items.map(([view, icon, text]) => `<button class="${state.view === view ? "active" : ""}" data-view="${view}" ${state.view === view ? 'aria-current="page"' : ""}><span class="nav-icon" aria-hidden="true">${icon}</span>${text}${view === "approvals" && pending ? `<span class="count">${pending}</span>` : ""}</button>`).join("");
}

function render() {
  if (!state.actor) { app.innerHTML = loginView(); return; }
  const titles = {overview: "Overview", consult: "Product advice", requests: "After-sales care", approvals: "Review queue", studio: "Content studio", trace: "Activity trail"};
  const date = new Intl.DateTimeFormat("en-AU", {day: "numeric", month: "short", timeZone: "Australia/Sydney"}).format(new Date());
  app.innerHTML = `<div class="shell"><aside class="sidebar">${brand()}<div class="nav-label">${isFounder() ? "FOUNDER WORKSPACE" : "CUSTOMER WORKSPACE"}</div><nav class="nav" aria-label="Workspace navigation">${navigation()}</nav><div class="sidebar-footer"><div class="mode-note"><div class="live-dot">${e(modeLabel())}</div><p>Fictional data. Media: ${e(state.snapshot.mode.media)}.<br>No real payments or public posting.</p></div><div class="profile"><span class="avatar">${isFounder() ? "F" : e(state.actor.name[0])}</span><div class="profile-text"><strong>${isFounder() ? "Founder / Operator" : e(state.actor.name.split(" · ")[0])}</strong><span>${isFounder() ? "Accountable human" : "Demo Customer"}</span></div><button class="logout" data-action="logout" aria-label="Sign out" title="Sign out">↪</button></div></div></aside><main class="main"><header class="topbar"><div class="crumb">Company workspace <span aria-hidden="true"> / </span><strong>${titles[state.view]}</strong></div><div class="topbar-right"><span class="small muted">${e(date)}</span><span class="pill sim">${e(modeLabel())}</span><button class="text-button" data-action="refresh" aria-label="Refresh workspace">↻ Refresh</button><button class="text-button" data-action="logout">Sign out</button></div></header><div class="content">${pageContent()}<p class="footer-note">A local proof of concept for the AI-Powered One-Person Beauty Commerce and Content Company.<br>BA: ${e(state.snapshot.mode.ba)} configured. MC text: ${e(state.snapshot.mode.mc)} configured. Media: ${e(state.snapshot.mode.media)}. Commerce: simulated. Live configuration does not prove model availability.</p></div></main></div>`;
  if (state.busy) busyButtons(true);
}

function heading(eyebrow, title, subtitle, action = "") {
  return `<div class="page-heading"><div><div class="eyebrow">${e(eyebrow)}</div><h1>${e(title)}</h1><p>${e(subtitle)}</p></div>${action ? `<div class="heading-actions">${action}</div>` : ""}</div>`;
}

function pageContent() {
  if (state.view === "overview") return overview();
  if (state.view === "consult") return consultation();
  if (state.view === "requests") return requestsView();
  if (state.view === "approvals") return approvalsView();
  if (state.view === "studio") return studio();
  return traceView();
}

function overview() {
  const pending = state.snapshot.approvals.filter(item => item.status === "PENDING").length;
  const active = records("CS").filter(item => !["RESOLVED", "REJECTED", "CANCELLED"].includes(item.status)).length;
  const resolved = records("CS").filter(item => item.status === "RESOLVED").length;
  const stats = isFounder() ? [["Awaiting your review", pending, "Exact action & revision", "◇"], ["Customer requests", active, "Open after-sales workflows", "⇄"], ["Content drafts", records("MC").length, "Text drafts · storyboard previews", "✧"], ["Recorded outcomes", resolved, "Simulated service results", "✓"]]
    : [["Consultations", records("BA").length, "Saved product advice", "✧"], ["Open requests", active, "Your after-sales workflows", "⇄"], ["Awaiting review", pending, "Founder decision pending", "◇"], ["Recorded outcomes", resolved, "Simulated service results", "✓"]];
  const recent = records("CS").slice(0, 3);
  const agents = [["BA", "Beauty Advisor", "Grounded product advice from catalogue & stock evidence.", "Business role"], ["CS", "Customer Service", "Policy-supported requests and confirmed outcomes.", "Business role"], ["MC", "Marketing Content", "Reviewable scripts, storyboards and draft media.", "Business role"], ["AP", "Approval & Governance", "Human decisions for the exact action and revision.", "Shared control"], ["CO", "Coordination & Recovery", "Minimal handoffs, visible failure and safe recovery.", "Shared control"]];
  return heading(isFounder() ? "THE FOUNDER'S DESK" : "YOUR BEAUTY WORKSPACE", isFounder() ? "A little oversight. A clearer company." : "Thoughtful advice, with a clear next step.", isFounder() ? "Review what needs you. Follow what your specialists are doing." : "Find a supported product match or follow your after-sales request.", `<button class="button" data-view="${isFounder() ? "approvals" : "consult"}">${isFounder() ? "Open review queue" : "Start a consultation"} <span>↗</span></button>`)
    + `<section class="hero"><div><div class="eyebrow">HOW THIS DEMO WORKS</div><h2>An exchange, with every decision visible.</h2><p>Customer request → Founder starts the handoff → supported advice → exact-scope review → Customer confirmation → simulated outcome.</p><button class="text-button" data-view="requests">Explore the after-sales workflow <span>↗</span></button></div><div class="flow" aria-label="Customer Service, Coordination, Beauty Advisor and human Approval"><div class="flow-node"><b>CS</b><span>Understand</span></div><i class="flow-line"></i><div class="flow-node"><b>CO</b><span>Connect</span></div><i class="flow-line"></i><div class="flow-node"><b>BA</b><span>Advise</span></div><i class="flow-line"></i><div class="flow-node"><b>AP</b><span>Review</span></div></div></section><div class="stats">${stats.map(([title, value, note, icon]) => `<div class="stat"><div class="stat-top">${title}<span class="stat-icon">${icon}</span></div><strong>${value}</strong><small>${note}</small></div>`).join("")}</div><div class="grid-two"><section class="panel"><div class="panel-head"><div><h2>${isFounder() ? "Requests to follow" : "Your recent requests"}</h2><p>Live records from this local workspace</p></div><button class="text-button" data-view="requests">View all ↗</button></div>${recent.length ? recent.map(item => `<div class="item-row"><div class="agent-symbol cs">CS</div><div class="item-main"><strong>${e(item.payload.orderId)} · Exchange request</strong><small>${e(item.id)} · Revision ${item.revision}</small></div>${badge(item.status)}</div>`).join("") : empty("No requests yet", isFounder() ? "Sign in as a Customer to create a request, then return here to start its handoff." : "Your demo order is ready when you want to explore an exchange.", isFounder() ? "" : "requests", "Explore after-sales care")}</section><section class="panel"><div class="panel-head"><div><h2>Connected capabilities</h2><p>Three business roles, two shared controls</p></div><span class="badge">${e(modeLabel())}</span></div><div class="agent-list">${agents.map(([code, title, description, type]) => `<div class="item-row"><div class="agent-symbol ${code.toLowerCase()}">${code}</div><div class="item-main"><strong>${title}</strong><small>${description}</small></div><span class="badge">${type}</span></div>`).join("")}</div></section></div>`;
}

function needsFields(prefix, values = {}) {
  return `<div class="field wide"><label for="${prefix}-message">What would you like help with?</label><textarea id="${prefix}-message" name="message" required maxlength="2000" placeholder="Tell us what you need and what matters to you.">${e(values.message || "I would like a fragrance-free moisturiser for dry skin.")}</textarea></div><div class="field"><label for="${prefix}-concern">Product need</label><select id="${prefix}-concern" name="concern"><option value="HYDRATION" ${values.concern !== "CLEANSING" ? "selected" : ""}>Hydration / dry skin</option><option value="CLEANSING" ${values.concern === "CLEANSING" ? "selected" : ""}>Gentle cleansing</option></select></div><div class="field"><label for="${prefix}-budget">Budget · AUD</label><input id="${prefix}-budget" name="budget" type="number" min="0.01" max="10000" step="0.01" value="${e(values.budget === undefined ? 60 : values.budget / 100)}" required></div><div class="field wide"><label class="checkbox"><input name="fragranceFree" type="checkbox" ${values.fragranceFree !== false ? "checked" : ""}>Fragrance-free is required</label><small>These explicit constraints drive the evidence-based match. This version does not infer arbitrary needs from natural language.</small></div>`;
}

function productsView() {
  return `<div class="product-grid">${state.snapshot.products.map(product => `<article class="product"><div class="product-art ${e(product.tone)}" aria-hidden="true"><div class="bottle"></div></div><h3>${e(product.name)}</h3><p>${e(product.facts[0])}</p><div class="price">${money(product.price)}</div>${badge(product.availability)}</article>`).join("")}</div>`;
}

function adviceView(result) {
  if (!result) return "";
  if (!result.product) return `<div class="notice">${e(result.message)}</div>`;
  return `<div class="recommendation"><strong>${e(result.product.name)} · ${money(result.product.price)}</strong><ul>${result.reasons.map(reason => `<li>${e(reason)}</li>`).join("")}</ul></div><div class="evidence">Evidence: ${e(result.evidence.catalogueRef)}<br>Stock: ${e(result.evidence.availability)} · observed ${e(new Date(result.evidence.inventoryObservation).toLocaleTimeString("en-AU"))}<br>${result.simulated === false ? "Live BA recommendation" : "Mock recommendation"} · No purchase is authorised by this advice.</div>`;
}

function needsConversation(item) {
  const p = item.payload, n = p.proposedNeeds;
  const mode = p.simulated ? "Mock needs interpretation" : "Model needs interpretation";
  const summary = n ? `<div class="evidence"><strong>Interpreted needs · awaiting your confirmation</strong><br>Product need: ${e(n.concern ? label(n.concern) : "Not stated")}<br>Budget: ${n.budget === null ? "Not stated" : money(n.budget * 100)}<br>Fragrance-free: ${n.fragranceFree === null ? "Not stated" : n.fragranceFree ? "Required" : "Not required"}<details><summary>Quoted sources from your messages</summary>${Object.entries(n.sources).filter(([, quote]) => quote).map(([key, quote]) => `<p>${e(key)}: <q>${e(quote)}</q></p>`).join("")}</details></div>` : "";
  const questions = p.questions?.length ? `<div class="notice"><strong>Please clarify</strong><ul>${p.questions.map(q => `<li>${e(q)}</li>`).join("")}</ul></div>` : "";
  const confirm = item.status === "CLARIFYING" && p.needsReady ? `<form data-form="ba-confirm-needs" data-id="${e(item.id)}" data-revision="${item.revision}"><div class="form-grid"><div class="field"><label for="need-${e(item.id)}">Confirm product need</label><select id="need-${e(item.id)}" name="concern" required><option value="HYDRATION" ${n.concern === "HYDRATION" ? "selected" : ""}>Hydration / dry skin</option><option value="CLEANSING" ${n.concern === "CLEANSING" ? "selected" : ""}>Gentle cleansing</option></select></div><div class="field"><label for="budget-${e(item.id)}">Confirm maximum budget · AUD</label><input id="budget-${e(item.id)}" name="budget" type="number" min="0.01" max="10000" step="0.01" value="${e(n.budget)}" required></div><div class="field"><label for="fragrance-${e(item.id)}">Confirm fragrance preference</label><select id="fragrance-${e(item.id)}" name="fragranceFree" required><option value="true" ${n.fragranceFree ? "selected" : ""}>Fragrance-free required</option><option value="false" ${!n.fragranceFree ? "selected" : ""}>Fragrance acceptable</option></select></div></div><p>Review and correct these conditions. No product has been recommended yet.</p><button class="button" type="submit">Confirm needs & find a match ↗</button></form>` : "";
  const pending = p.pendingOutcome?.revision === item.revision;
  const canCancel = ["ACTIVE", "CLARIFYING", "INCOMPLETE"].includes(item.status);
  const answer = ["CLARIFYING", "INCOMPLETE"].includes(item.status) && !pending && p.errorCode !== "MEDICAL_SCOPE" ? `<form data-form="ba-clarify" data-id="${e(item.id)}" data-revision="${item.revision}"><div class="field"><label for="answer-${e(item.id)}">Your answer or correction</label><textarea id="answer-${e(item.id)}" name="message" maxlength="2000" required placeholder="For example: My budget is AUD 60 and fragrance-free is required."></textarea></div><button class="button secondary" type="submit">Update this consultation ↗</button></form>` : "";
  const revise = item.status !== "CANCELLED" ? `<details><summary>Replace the full request</summary><form data-form="ba-revise" data-id="${e(item.id)}" data-revision="${item.revision}"><div class="field"><label for="replace-${e(item.id)}">Replacement request</label><textarea id="replace-${e(item.id)}" name="message" maxlength="2000" required placeholder="State all current needs, budget and fragrance preference."></textarea></div><p class="small muted">This replaces the current scope. Former advice stays historical; missing conditions will be asked again.</p><button class="button secondary" type="submit">Save replacement request ↗</button></form></details>` : "";
  const controls = `<div class="row-actions">${pending && canCancel ? `<button class="button" data-action="ba-recover" data-id="${e(item.id)}" data-revision="${item.revision}">Recover saved result ↗</button>` : ""}${!pending && ["ACTIVE", "INCOMPLETE"].includes(item.status) && p.errorCode !== "MEDICAL_SCOPE" ? `<button class="button secondary" data-action="ba-retry" data-id="${e(item.id)}" data-revision="${item.revision}">Retry this attempt ↗</button>` : ""}${canCancel ? `<button class="button secondary" data-action="ba-cancel" data-id="${e(item.id)}" data-revision="${item.revision}">Cancel consultation</button>` : ""}</div>`;
  const history = p.history?.length ? `<details><summary>Previous revisions · not current advice</summary>${p.history.map(prior => `<div class="evidence">Revision ${e(prior.revision)} · ${e(label(prior.status))}${prior.messages ? `<br>${prior.messages.map(e).join("<br>")}` : ""}${prior.result?.product ? `<br>Historical recommendation: ${e(prior.result.product.name)}. Recheck required for any current advice.` : ""}</div>`).join("")}</details>` : "";
  return `<article class="record-card"><div class="record-head"><div><span class="mono">${e(item.id)} · Revision ${item.revision}</span><h3>${e(p.messages[0])}</h3></div>${badge(item.status)}</div><p class="small muted">${e(mode)} · ${item.status === "CANCELLED" ? "Cancelled; no current advice applies." : p.needsConfirmed ? "Needs explicitly confirmed by Customer." : "Hypotheses require Customer confirmation."}</p><details><summary>Your conversation</summary>${p.messages.map(text => `<p>${e(text)}</p>`).join("")}</details>${item.status === "CLARIFYING" ? summary : ""}${questions}${p.message ? `<p>${e(p.message)}</p>` : ""}${item.status === "ACTIVE" ? '<p>Processing or interrupted. Refresh to inspect the saved revision. Cancellation suppresses the reply; an in-flight model request may still finish.</p>' : ""}${pending ? '<div class="notice">A draft is saved, but no final result is recorded. Recovery rechecks the saved scope and evidence without calling the model.</div>' : ""}${adviceView(p.result)}${confirm}${answer}${controls}${!pending && ["ACTIVE", "INCOMPLETE"].includes(item.status) && p.errorCode !== "MEDICAL_SCOPE" ? '<p class="small muted">Retry starts a new revision and may call the model again. It discards any still-running attempt and requires fresh needs confirmation.</p>' : ""}${revise}${history}</article>`;
}

function consultation() {
  return heading("BEAUTY ADVISOR", "Advice with something behind it.", "Recommendations use saved product facts, explicit constraints and known stock.")
    + `<div class="grid-two"><section class="panel"><div class="panel-head"><h2>Start a consultation</h2><span class="badge">${state.snapshot.mode.ba === "LIVE" ? "LIVE configured" : "MOCK"} BA</span></div><form id="ba-intake-form"><div class="field"><label for="ba-natural-message">Tell us what you need</label><textarea id="ba-natural-message" name="message" required maxlength="2000" placeholder="Describe your product need. We will ask about missing conditions."></textarea></div><div class="form-footer"><p>No guessed budget or fragrance preference. Review interpreted needs before advice.</p><button class="button" type="submit">Understand my needs ↗</button></div></form><details><summary>Use explicit structured fields (existing mode)</summary><form id="consult-form"><div class="form-grid">${needsFields("consult")}</div><div class="form-footer"><p>Advice only. No order, payment or medical diagnosis.</p><button class="button" type="submit">Find a supported match ↗</button></div></form></details></section><section class="panel"><div class="panel-head"><div><h2>Demo catalogue</h2><p>Synthetic products · current local stock</p></div></div>${productsView()}</section></div><section class="panel"><div class="panel-head"><h2>Your consultations</h2></div>${records("BA").map(item => item.payload.naturalNeeds ? needsConversation(item) : `<article class="record-card"><div class="record-head"><div><span class="mono">${e(item.id)}</span><h3>${e(item.payload.needs?.message || "Clarification needed")}</h3></div>${badge(item.status)}</div>${adviceView(item.payload.result)}${item.payload.message ? `<p>${e(item.payload.message)}</p>` : ""}</article>`).join("") || empty("No consultations yet", "Your saved advice and evidence references will appear here.")}</section>`;
}

function requestsView() {
  const list = records("CS");
  const eligibleOrders = state.snapshot.orders.filter(order => order.status === "DELIVERED" && !list.some(item => item.payload.orderId === order.id && !["REJECTED", "CANCELLED"].includes(item.status)));
  const create = !isFounder() && eligibleOrders.length ? `<section class="panel"><div class="panel-head"><div><h2>Request an exchange</h2><p>A declared demo policy routes every exchange for Founder review.</p></div><span class="badge">SIMULATED SERVICE</span></div><form id="exchange-form"><div class="form-grid"><div class="field wide"><label for="orderId">Your order</label><select id="orderId" name="orderId">${eligibleOrders.map(order => `<option value="${e(order.id)}">${e(order.id)} · ${e(label(order.status))}</option>`).join("")}</select></div>${needsFields("exchange")}</div><div class="form-footer"><p>No real refund, payment or shipment occurs.</p><button class="button" type="submit">Submit exchange request ↗</button></div></form></section>` : (!isFounder() ? '<div class="notice">Your demo order already has an active or recorded exchange. Follow the existing request below.</div>' : "");
  return heading("CUSTOMER SERVICE & COORDINATION", "Care that keeps its promises.", isFounder() ? "Initiate authorised handoffs. Approval and execution remain separate." : "Track the proposal, Founder review and your final confirmation.") + create
    + `<section class="panel"><div class="panel-head"><h2>${isFounder() ? "Customer requests" : "Your requests"}</h2><span class="small muted">${list.length} recorded</span></div>${list.map(requestCard).join("") || empty("No exchange requests yet", isFounder() ? "Create a request in the Customer workspace, then return to initiate coordination." : "Submit the form above to begin the demo workflow.")}</section>`;
}

function requestCard(item) {
  const payload = item.payload;
  const blocked = payload.evidenceOutcome;
  const evidenceNotice = blocked ? `<div class="notice"><strong>${e(label(blocked.code))}</strong><br>${e(blocked.reason)}<br>No exchange was executed for this blocked assessment.${blocked.policyRefs?.length ? `<br>Permitted policy references: ${blocked.policyRefs.map(e).join(" · ")}` : ""}<br>Required evidence must be refreshed by an authorised source. Then reassess this request with the current needs.</div>` : "";
  let actions = "";
  if (isFounder() && item.status === "ASSESSING") actions = `<button class="button" data-action="coordinate" data-id="${e(item.id)}">Start advice handoff ↗</button>`;
  if (isFounder() && item.status === "REVIEW_PENDING") actions = '<button class="button secondary" data-view="approvals">Open exact-scope review ↗</button>';
  if (!isFounder() && item.status === "AWAITING_CONFIRMATION") actions = `<button class="button" data-action="confirm" data-id="${e(item.id)}" data-revision="${item.revision}">${payload.decision === "APPROVE" ? "Confirm simulated exchange" : "Confirm proposal & request review"} ↗</button>`;
  if (!isFounder() && ["RECONCILING", "RECORDING_FAILED", "EXECUTING"].includes(item.status)) actions = `<button class="button" data-action="reconcile" data-id="${e(item.id)}">Query existing action outcome ↗</button>`;
  const revision = !isFounder() && !["RESOLVED", "EXECUTING", "RECONCILING", "RECORDING_FAILED", "CANCELLED"].includes(item.status)
    ? `<details><summary>${blocked ? "Reassess with corrected needs or refreshed evidence" : "Correct the needs and request a new proposal"}</summary><form data-form="exchange-revise" data-id="${e(item.id)}" data-revision="${item.revision}"><div class="form-grid">${needsFields(`rev-${item.id}`, payload.needs || {})}</div><div class="form-footer"><p>Reassessment uses server-side evidence. Changing the context invalidates previous confirmation and approval.</p><button class="button secondary" type="submit">${blocked ? "Reassess current request" : "Save revised needs"}</button></div></form></details>` : "";
  return `<article class="record-card"><div class="record-head"><div><span class="mono">${e(item.id)} · Revision ${item.revision}</span><h3>${e(payload.orderId)} · Exchange request</h3></div>${badge(item.status)}</div><p>${e(payload.needs?.message || "The request needs correction before advice can proceed.")}</p>${payload.advice && !blocked ? adviceView(payload.advice) : ""}${evidenceNotice}${!blocked ? `<p class="small muted">${e(payload.note || "Review the current proposal and confirm the exact action.")}</p>` : ""}${payload.result ? `<div class="evidence">${e(payload.result.outcome)}<br>Service reference: ${e(payload.result.serviceRef)}<br>${e(payload.result.remainingSteps)}</div>` : ""}<div class="review-meta">${payload.actionRef ? `<span>Action: <span class="mono">${e(payload.actionRef)}</span></span>` : ""}${payload.approvalId ? `<span>Review: <span class="mono">${e(payload.approvalId)}</span></span>` : ""}</div><div class="row-actions">${actions}</div>${revision}</article>`;
}

function approvalOutcome(review, origin) {
  if (review.status === "RECORDING_FAILED" && !review.decision_id) {
    const intent = review.intent;
    const current = origin?.revision === review.revision && origin?.payload.approvalId === review.id;
    const recoverable = isFounder() && current && intent?.founder_id === state.actor.id
      && ["PROPOSED", "RECORDING_FAILED"].includes(intent.status);
    return `<div class="evidence">The decision could not be recorded. No approval was delivered and no business action was executed.${intent ? `<br>Saved intention (not a committed decision): <strong>${e(label(intent.kind))}</strong><br>Saved reason: ${e(intent.reason)}` : ""}<br>No applicable committed decision.</div>${recoverable ? `<div class="row-actions"><button class="button secondary" data-action="recover-decision" data-id="${e(review.id)}" data-revision="${review.revision}">Recover saved decision</button></div><p class="small muted">Restore the saved decision for this exact scope. Recovery does not execute an exchange or publish content.</p>` : `<p class="small muted">${current ? "Recovery requires the original authorised decision maker and a saved intention." : "The proposal has changed. Fresh review is required; this saved intention cannot be recovered."}</p>`}`;
  }
  const fallback = review.status === "SUPERSEDED" ? "This review was superseded by a changed context."
    : review.decision_id ? "Decision recorded for this exact scope." : "No decision has been committed.";
  return `<div class="evidence">${e(review.reason || fallback)}<br>${review.decision_id ? `Committed decision: ${e(review.decision_id)} · Delivery: ${e(review.delivery)}` : "No applicable committed decision."}</div>${review.delivery === "FAILED" ? `<div class="row-actions"><button class="button secondary" data-action="redeliver" data-id="${e(review.id)}">Redeliver the same decision</button></div>` : ""}`;
}

function approvalsView() {
  const reviews = state.snapshot.approvals;
  return heading("HUMAN APPROVAL & GOVERNANCE", "Your decision. This exact scope.", "A committed approval permits re-evaluation. It does not execute an exchange or publish content.")
    + `<div class="notice">Review the action, evidence and revision before deciding. A changed proposal needs fresh approval.</div><section class="panel"><div class="panel-head"><h2>Review requests</h2><span class="small muted">${reviews.filter(item => item.status === "PENDING").length} awaiting decision</span></div>${reviews.map(review => {
      const origin = state.snapshot.records.find(item => item.id === review.origin_id);
      const source = review.evidence.productEvidence;
      const evidence = source
        ? `Policy fixture: ${e(review.evidence.policyRef)}<br>Catalogue source: ${e(source.catalogueRef)}<br>Customer constraints: ${e(label(source.constraints.concern))}, budget ${money(source.constraints.budget)}, ${source.constraints.fragranceFree ? "fragrance-free required" : "fragrance-free not required"}.`
        : `Catalogue source: ${e(review.evidence.catalogueRef)}<br>Supported facts: ${e((review.evidence.facts || []).join(" · "))}`;
      return `<article class="review-card"><div class="record-head"><div><span class="mono">${e(review.id)} · Revision ${review.revision}</span><h3>${review.origin_role === "CS" ? "Simulated customer exchange" : review.action.mediaKind === "TEMPLATE_VIDEO" ? "Text + template video draft" : review.action.textMode === "LIVE" ? "Live text draft · mock media" : "Mock marketing draft"}</h3></div>${badge(review.status)}</div><div class="scope">${review.origin_role === "CS" ? `Order <strong>${e(review.action.orderId)}</strong> → replacement <strong>${e(review.action.productId)}</strong>` : `Draft <strong>${e(review.action.draftId)}</strong> · revision <strong>${review.revision}</strong>`}<br>Origin: <span class="mono">${e(review.origin_id)}</span></div>${origin?.payload.advice ? adviceView(origin.payload.advice) : ""}${review.action.mediaSha256 ? `<p class="small muted">Template MP4 SHA-256: ${e(review.action.mediaSha256)}</p>` : ""}${origin?.kind === "MC" ? (origin.revision === review.revision ? campaignPreview(origin.payload) : `<div class="notice">The campaign now has a different revision. This review cannot approve the current draft.</div>`) : ""}<div class="evidence">${evidence}</div>${review.status === "PENDING" ? `<form data-form="review" data-id="${e(review.id)}" data-revision="${review.revision}"><div class="field"><label for="reason-${e(review.id)}">Your reason</label><textarea id="reason-${e(review.id)}" name="reason" maxlength="1000" placeholder="Explain your decision for this exact action and revision." required></textarea></div><div class="row-actions"><button class="button" type="button" data-action="decide" data-decision="APPROVE">Approve exact scope</button><button class="button secondary" type="button" data-action="decide" data-decision="REQUEST_REVISION">Request revision</button><button class="button danger" type="button" data-action="decide" data-decision="REJECT">Reject</button></div></form>` : approvalOutcome(review, origin)}</article>`;
    }).join("") || empty("Your review queue is clear", "Exchange proposals and text/storyboard drafts will appear here when submitted.")}</section>`;
}

function campaignFields(prefix, values = {}) {
  return `<div class="field"><label for="${prefix}-product">Authorised product</label><select id="${prefix}-product" name="productId">${state.snapshot.products.map(product => `<option value="${e(product.id)}" ${(values.product?.id || values.productId) === product.id ? "selected" : ""}>${e(product.name)} · ${e(product.id)}</option>`).join("")}</select></div><div class="field"><label for="${prefix}-brief">Campaign brief</label><textarea id="${prefix}-brief" name="brief" required maxlength="2000" placeholder="Describe the campaign objective and creative direction.">${e(values.brief || "Introduce a calm, simple daily hydration routine.")}</textarea><small>${state.snapshot.mode.mc === "LIVE" ? "The model selects catalogue facts, a visual style and a featured fact from your brief. Product wording stays catalogue-literal." : "The mock uses catalogue facts only; creative direction is stored with the fixture."}</small></div>`;
}

function campaignPreview(payload) {
  if (payload.failure) return `<div class="notice">${e(payload.failure.reason)}<br>No review-ready text or media is available for this revision.</div>`;
  if (!payload.script) return `<div class="notice">No saved text or media is available for this revision. Generation may be in progress or final recording may have failed. Refresh to check the current status.</div>`;
  return `<p class="small muted">${payload.textSimulated === false ? "Live model text plan · catalogue-literal product wording" : "Mock text generation"}${payload.textPlan ? `<br>Proposed style: ${e(label(payload.textPlan.style))} · Brief reference: <q>${e(payload.textPlan.briefRef)}</q>` : ""}</p><p class="script">${e(payload.script)}</p><p class="small muted">${e(payload.media?.label)}</p>`;
}

function campaignControls(item) {
  const p = item.payload, rev = item.revision, id = e(item.id);
  const active = ["DRAFTING", "GENERATING", "RECORDING_FAILED", "GENERATION_FAILED", "INCOMPLETE", "CONTENT_REJECTED", "REVIEW_PENDING", "REVISION_REQUIRED"].includes(item.status);
  const interrupted = ["DRAFTING", "GENERATING", "RECORDING_FAILED", "GENERATION_FAILED", "INCOMPLETE"].includes(item.status);
  const pending = p.pendingGeneration;
  const notice = item.status === "CANCELLED" ? "Cancelled. Late output is suppressed. Start a new campaign to continue."
    : pending ? `A generation draft is stored (${pending.textSimulated === false ? "live" : "mock"} text; ${pending.mediaSimulated === false ? "template video" : "mock media"}). Recover it without generating again. It is not review-ready yet.`
    : ["DRAFTING", "GENERATING"].includes(item.status) ? "Generation may still be running or may have been interrupted; this status alone cannot identify a stopped worker. Refresh first. Explicit retry starts a new revision and supersedes any late reply."
    : interrupted ? "No saved generation is available. Restore the service or correct the request before an explicit retry. Retry starts a new revision and may call the generators again."
    : "";
  return `${notice ? `<div class="notice">${e(notice)}</div>` : ""}<div class="row-actions">${pending && interrupted ? `<button class="button secondary" data-action="mc-recover" data-id="${id}" data-revision="${rev}">Recover saved generation</button>` : ""}${!pending && interrupted ? `<button class="button secondary" data-action="mc-retry" data-id="${id}" data-revision="${rev}">Retry generation as new revision</button>` : ""}${active ? `<button class="button secondary" data-action="mc-cancel" data-id="${id}" data-revision="${rev}">Cancel this campaign</button>` : ""}</div>`;
}

function campaignCard(item) {
  const payload = item.payload;
  const failed = Boolean(payload.failure);
  const media = payload.media;
  return `<article class="record-card"><div class="record-head"><div><span class="mono">${e(item.id)} · Revision ${item.revision}</span><h3>${e(payload.product?.name || payload.productId || "Campaign draft")}</h3></div>${badge(item.status)}</div><p>${e(payload.brief)}</p>${item.status === "CANCELLED" ? "" : campaignPreview(payload)}${campaignControls(item)}${!failed && media?.kind === "TEMPLATE_VIDEO" ? `<video controls preload="metadata" width="360" aria-label="Template video draft revision ${item.revision}" src="/api/campaigns/${encodeURIComponent(item.id)}/media/${item.revision}"></video><p><a class="button secondary" download="${e(item.id)}-r${item.revision}.mp4" href="/api/campaigns/${encodeURIComponent(item.id)}/media/${item.revision}">Download draft MP4</a></p><p class="small muted">Template composition, no video model or audio. Download is an internal draft preview, not publication. SHA-256: ${e(media.sha256)}</p>` : ""}${!failed && media ? `<div class="storyboard">${media.frames.map(frame => `<div class="shot"><small>SHOT ${frame.shot} · ${e(frame.duration)}</small><strong>${e(frame.caption)}</strong><span>${e(frame.direction)}</span></div>`).join("")}</div>` : ""}${payload.approvalId ? `<div class="evidence">Source: ${e(payload.evidence?.catalogueRef)}<br>Review: ${e(payload.approvalId)}<br>Approval covers this exact draft revision. ${media?.kind === "TEMPLATE_VIDEO" ? "Review binds this MP4 hash; no publication occurs." : "Media remains a storyboard placeholder; no publication occurs."}</div><div class="row-actions"><button class="button secondary" data-view="approvals">Open review queue ↗</button></div>` : `<div class="evidence">No approval request is recorded for this revision.</div>`}${item.status !== "CANCELLED" ? `<details><summary>Revise this draft with fresh review</summary><form data-form="campaign-revise" data-id="${e(item.id)}" data-revision="${item.revision}"><div class="form-grid">${campaignFields(`rev-${item.id}`, payload)}</div><div class="form-footer"><p>The new revision inherits no approval.</p><button class="button secondary" type="submit">Create revised draft</button></div></form></details>` : ""}</article>`;
}

function studio() {
  return heading("MARKETING CONTENT", "Good stories start with supported facts.", "Prepare a text draft and storyboard, then review the exact revision. Media is explicitly labelled below.")
    + `<section class="panel"><div class="panel-head"><h2>Start a campaign draft</h2><span class="badge">${state.snapshot.mode.media === "TEMPLATE_VIDEO" ? `${state.snapshot.mode.mc} TEXT · TEMPLATE MP4` : state.snapshot.mode.mc === "LIVE" ? "LIVE TEXT MODEL · MOCK MEDIA" : "MOCK MODEL & MEDIA"}</span></div><form id="campaign-form"><div class="form-grid">${campaignFields("campaign")}</div><div class="form-footer"><p>${state.snapshot.mode.media === "TEMPLATE_VIDEO" ? "Optional template MP4 rendering enabled. No video model, audio or public posting." : "Storyboard placeholder only. No video file or public post is generated."}</p><button class="button" type="submit">${state.snapshot.mode.media === "TEMPLATE_VIDEO" ? "Create video draft" : state.snapshot.mode.mc === "LIVE" ? "Create text draft" : "Create mock draft"} ↗</button></div></form></section><section class="panel"><div class="panel-head"><h2>Campaign drafts</h2></div>${records("MC").map(campaignCard).join("") || empty("A blank canvas, with clear boundaries", "Create a draft to see its script, storyboard, sources and review history.")}</section>`;
}

function traceView() {
  const tools = isFounder() ? `<section class="panel"><div class="panel-head"><div><h2>Simulation controls</h2><p>Inject one failure into the next applicable operation.</p></div></div><form id="fault-form" class="simulation-tools"><select name="fault" aria-label="Failure fixture"><option value="none">Normal operation</option><option value="after_sales_timeout">After-sales timeout after execution</option><option value="outcome_recording">Outcome recording failure</option><option value="approval_delivery">Committed decision delivery failure</option><option value="approval_recording">Decision recording failure (no approval)</option><option value="ba_recording">BA final advice save failure (draft retained)</option><option value="mc_recording">MC final generation save failure (draft retained)</option></select><button class="button secondary" type="submit">Apply fixture</button><p class="small muted">Currently armed: ${e(state.snapshot.faults.join(", ") || "none")}</p></form></section>` : "";
  return heading("COORDINATION & RECOVERY", "Follow the work, not just the answer.", "Recorded events distinguish handoffs, committed decisions, execution and recovery.") + tools
    + `<section class="panel"><div class="panel-head"><h2>Recorded activity</h2><span class="small muted">Newest first · up to 150 events</span></div><div class="trace-list">${state.snapshot.events.map(event => `<article class="trace-event"><div class="agent-symbol ${event.role.toLowerCase()}">${e(event.role)}</div><div><h3>${e(label(event.event))}</h3><p class="mono">${e(event.entity_id)}</p><details><summary>Inspect recorded context</summary><div class="trace-detail">${e(JSON.stringify(event.detail))}</div></details></div><time datetime="${e(event.created)}">${e(new Date(event.created).toLocaleTimeString("en-AU"))}</time></article>`).join("") || empty("No activity has been recorded", "Events appear when you use a workflow. No development history is fabricated.")}</div></section>`;
}

function formNeeds(form) {
  const values = new FormData(form);
  return {message: values.get("message"), concern: values.get("concern"), budget: Number(values.get("budget")), fragranceFree: values.get("fragranceFree") === "on"};
}

document.addEventListener("change", event => {
  if (event.target.id === "username") {
    const password = event.target.value === "founder" ? "founder-demo" : "customer-demo";
    document.querySelector("#password").value = password;
    document.querySelector("#credential-hint").textContent = `Demo password: ${password}`;
  }
});

document.addEventListener("submit", event => {
  const form = event.target;
  event.preventDefault();
  if (!form.reportValidity()) return;
  const values = new FormData(form);
  if (form.id === "login-form") {
    mutate(async () => {
      const result = await api("/api/login", {username: values.get("username"), password: values.get("password")});
      state.actor = result.actor; state.csrf = result.csrf; state.view = "overview";
    });
  } else if (form.id === "ba-intake-form") {
    mutate(() => api("/api/consultations/intake", {message: values.get("message")}), "Needs interpretation saved. Review the questions and current status.", true);
  } else if (form.dataset.form === "ba-clarify") {
    mutate(() => api(`/api/consultations/${encodeURIComponent(form.dataset.id)}/clarify`, {message: values.get("message"), contextRevision: Number(form.dataset.revision)}), "Consultation updated. Review the interpreted conditions before confirming.", true);
  } else if (form.dataset.form === "ba-confirm-needs") {
    mutate(() => api(`/api/consultations/${encodeURIComponent(form.dataset.id)}/confirm-needs`, {contextRevision: Number(form.dataset.revision), concern: values.get("concern"), budget: Number(values.get("budget")), fragranceFree: values.get("fragranceFree") === "true"}), "Confirmed consultation saved. Check whether advice completed.", true);
  } else if (form.dataset.form === "ba-revise") {
    mutate(() => api(`/api/consultations/${encodeURIComponent(form.dataset.id)}/revise`, {message: values.get("message"), contextRevision: Number(form.dataset.revision)}), "Replacement saved. Review and confirm the new conditions.", true);
  } else if (form.id === "consult-form") {
    mutate(() => api("/api/consultations", formNeeds(form)), "Consultation recorded. Review the supported result below.");
  } else if (form.id === "exchange-form") {
    mutate(() => api("/api/after-sales", {...formNeeds(form), orderId: values.get("orderId")}), "Request assessment saved. Review the recorded status and next step below.", true);
  } else if (form.dataset.form === "exchange-revise") {
    mutate(() => api(`/api/after-sales/${encodeURIComponent(form.dataset.id)}/revise`, {...formNeeds(form), contextRevision: Number(form.dataset.revision)}), "Request reassessed. Review the current status; changed proposals need fresh confirmation and review.", true);
  } else if (form.id === "campaign-form" || form.dataset.form === "campaign-revise") {
    const path = form.id === "campaign-form" ? "/api/campaigns" : `/api/campaigns/${encodeURIComponent(form.dataset.id)}/revise`;
    const body = {brief: values.get("brief"), productId: values.get("productId")};
    if (form.dataset.form === "campaign-revise") body.contextRevision = Number(form.dataset.revision);
    mutate(() => api(path, body), "Draft generation recorded. Check its status and exact-revision review below.", true);
  } else if (form.id === "fault-form") {
    mutate(() => api("/api/demo/fault", {fault: values.get("fault")}), "Simulation fixture updated.");
  }
});

document.addEventListener("click", event => {
  const button = event.target.closest("button");
  if (!button || (state.busy && !["refresh", "ba-cancel", "mc-cancel"].includes(button.dataset.action))) return;
  if (button.dataset.view) { state.view = button.dataset.view; render(); window.scrollTo(0, 0); return; }
  const action = button.dataset.action;
  const id = encodeURIComponent(button.dataset.id || "");
  if (action === "refresh") baControl(async () => {}, "Workspace refreshed.");
  if (action === "logout") {
    mutate(async () => {
      await api("/api/logout", {});
      state.actor = null; state.csrf = ""; state.snapshot = null;
    }).then(() => { if (!state.actor) render(); });
  }
  if (action === "ba-cancel") baControl(() => api(`/api/consultations/${id}/cancel`, {contextRevision: Number(button.dataset.revision)}), "Cancellation saved. Late replies will be discarded; start a new consultation to continue.");
  if (action === "ba-recover") mutate(() => api(`/api/consultations/${id}/recover`, {contextRevision: Number(button.dataset.revision)}), "Saved result checked and recorded without repeating inference. Review its actual status.", true);
  if (action === "ba-retry") mutate(() => api(`/api/consultations/${id}/retry`, {contextRevision: Number(button.dataset.revision)}), "New attempt saved. Review the current conditions before confirming.", true);
  if (action === "mc-cancel") baControl(() => api(`/api/campaigns/${id}/cancel`, {contextRevision: Number(button.dataset.revision)}), "Cancellation saved. Late replies will be suppressed; a running provider may continue consuming resources.");
  if (action === "mc-recover") mutate(() => api(`/api/campaigns/${id}/recover`, {contextRevision: Number(button.dataset.revision)}), "Saved generation checked without calling generators. Review the resulting status; no approval or publication occurred.", true);
  if (action === "mc-retry") mutate(() => api(`/api/campaigns/${id}/retry`, {contextRevision: Number(button.dataset.revision)}), "Explicit new generation attempt recorded. Check this new revision and review status.", true);
  if (action === "coordinate") mutate(() => api(`/api/after-sales/${id}/coordinate`, {}), "Request checked. Review its current status and any required evidence.", true);
  if (action === "confirm") mutate(() => api(`/api/after-sales/${id}/confirm`, {contextRevision: Number(button.dataset.revision)}), "Current confirmation recorded. Check the resulting status.", true);
  if (action === "reconcile") mutate(() => api(`/api/after-sales/${id}/reconcile`, {}), "Existing action queried without repeat execution.");
  if (action === "redeliver") mutate(() => api(`/api/approvals/${id}/deliver`, {}), "The same committed decision was redelivered.");
  if (action === "recover-decision") mutate(() => api(`/api/approvals/${id}/recover`, {contextRevision: Number(button.dataset.revision)}), "Saved decision recovered. Check delivery status; no business action was executed by recovery.", true);
  if (action === "decide") {
    const form = button.closest("form");
    if (!form.reportValidity()) return;
    const reason = new FormData(form).get("reason");
    mutate(() => api(`/api/approvals/${encodeURIComponent(form.dataset.id)}/decide`, {decision: button.dataset.decision, contextRevision: Number(form.dataset.revision), reason}), "Decision committed. Review delivery status; no business action was executed by approval.", true);
  }
});

async function start() {
  try {
    const session = await api("/api/session");
    state.actor = session.actor; state.csrf = session.csrf;
    await refresh();
  } catch (error) {
    state.actor = null;
    render();
    if (!error.message.includes("Sign in") && !error.message.includes("expired")) toast(error.message, true);
  }
}

start();
