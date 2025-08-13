import time
import math
from datetime import datetime
import io
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

# ---------------------- Page Setup ----------------------
st.set_page_config(
    page_title="AWS Architecture Design Using Agentic AI (GDPR/NIS2 aware)",
    page_icon="🛡️",
    layout="wide"
)

# --------------- Minimal CSS for nicer look -------------
st.markdown("""
<style>
.small-muted {color:#6b7280; font-size:0.9rem;}
.badge      {display:inline-block; padding:6px 10px; border-radius:12px; background:#eef2ff; color:#3730a3; margin-right:6px;}
.card {background:#ffffff; border:1px solid #e5e7eb; border-radius:14px; padding:16px; box-shadow:0 2px 8px rgba(0,0,0,0.04);}
.section-title {font-weight:700; font-size:1.2rem; margin:0 0 6px 0;}
.hint {background:#fff7ed; border:1px dashed #fdba74; padding:8px 12px; border-radius:10px;}
.cta {background:#fee2e2; color:#991b1b; padding:10px 12px; border-radius:10px; display:inline-block; font-weight:700;}
.kpi {background:#f8fafc; border:1px solid #e2e8f0; padding:10px 12px; border-radius:12px;}
hr {border:0; border-top:1px solid #e5e7eb;}
</style>
""", unsafe_allow_html=True)

# ------------------ Language Toggle ---------------------
lang = st.sidebar.selectbox("Language / Sprache", ["English", "Deutsch"])

# ------------------ Reset / New Architecture ------------
if st.sidebar.button("🔄 New Architecture / Neu laden"):
    st.experimental_rerun()

# ------------------ Header / Title ----------------------
st.markdown("<h1>🏗️ AWS Architecture Design Using Agentic AI</h1>", unsafe_allow_html=True)
st.caption("Free, open-source MVP • No external APIs • Built for 2030–2050 skills • GDPR/NIS2-aware")

# ------------------ Radar Inputs ------------------------
st.markdown("### 🎯 Design Priorities (adjust sliders)")
c1, c2, c3 = st.columns([1,1,1])
with c1:
    latency = st.slider("Latency", 0, 100, 60, help="Lower latency = faster response")
    load = st.slider("Load Balancing", 0, 100, 70, help="Traffic distribution & HA")
with c2:
    cost = st.slider("Cloud Cost", 0, 100, 50, help="Budget sensitivity / cost control")
    perf = st.slider("Performance", 0, 100, 75, help="Throughput, compute efficiency")
with c3:
    security = st.slider("Security", 0, 100, 85, help="Zero-trust, encryption, IAM")
    scale = st.slider("Scalability", 0, 100, 80, help="Auto-scale, burst traffic")

# Draw a single, Streamlit-safe radar plot (matplotlib)
def plot_radar(values, labels, title="Design Radar"):
    N = len(values)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    values = values + values[:1]
    angles = angles + angles[:1]

    fig = plt.figure(figsize=(4.5,4.5))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.15)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=9)
    ax.set_title(title, y=1.1, fontsize=12)
    ax.set_rmax(100)
    return fig

radar_labels = ["Latency","Load Bal.","Cost","Performance","Security","Scalability"]
radar_vals = [latency, load, cost, perf, security, scale]
rc1, rc2 = st.columns([1,1.6])
with rc1:
    st.pyplot(plot_radar(radar_vals, radar_labels, "Design Radar"))
with rc2:
    st.markdown("""
<div class="card">
  <div class="section-title">📝 Instructions</div>
  <div>Type your Use Case / RFP / Epic user story, then click <b>Run Agentic Design</b>.<br>
  You can download a <b>Tutorial</b> and a <b>Technical Design Document</b>, and refresh to design another architecture.</div>
</div>
""", unsafe_allow_html=True)

# ------------------ Focus & Input -----------------------
focus = st.selectbox(
    "Architecture Focus (choose one)",
    [
        "E-commerce (web & APIs)",
        "Real-time analytics pipeline",
        "IoT ingest + stream processing",
        "ML inference service",
        "Zero-trust microservices",
        "Data lakehouse ETL/ELT"
    ]
)

use_case = st.text_area("Type or Paste Use Case / RFP / Epic user story", height=130,
                        placeholder="Example: Build a global e-commerce checkout API with <200ms latency, PCI and GDPR compliance, daily analytics, and 10x traffic bursts.")

# ------------------ Agent Simulation --------------------
# Four human-like roles, thinking with elapsed seconds
agents = [
    ("Data Architect Sophia",    "Designs data flows, storage, ETL/ELT, and analytics."),
    ("Security Architect Emilia","Applies zero-trust, IAM, IAM boundaries, encryption, and compliance controls."),
    ("Solution Architect Kumar", "Assembles AWS components into a scalable, reliable blueprint."),
    ("AI Architect Amit",        "Adds ML/GenAI add-ons where useful, within free/open-source limits.")
]

def agent_reasoning(agent_name, brief, scores, context):
    # Lightweight deterministic "thinking"
    # returns a few bullet lines
    lat, lb, cst, prf, sec, scl = scores
    obs = []
    if sec >= 80:
        obs.append("Prioritize IAM least-privilege, KMS encryption, and private networking.")
    if scl >= 75:
        obs.append("Add auto-scaling groups and managed queues to handle bursts.")
    if lat >= 70:
        obs.append("Place compute close to users and cache aggressively.")
    if cst <= 50:
        obs.append("Prefer serverless and spot options to reduce spend.")
    if "IoT" in context or "sensor" in context.lower() or "stream" in context.lower():
        obs.append("Use streaming ingestion with schema-on-read and time-series buckets.")
    if "analytics" in context.lower():
        obs.append("Add batch + streaming analytics paths with cost-aware storage tiers.")
    if "ml" in context.lower() or "ai" in context.lower():
        obs.append("Containerize inference and isolate GPU/CPU pools for cost control.")
    if not obs:
        obs.append("Balance tradeoffs using managed services and clear SLOs.")
    # limit to 3 lines
    return obs[:3]

def build_architecture(focus, scores):
    lat, lb, cst, prf, sec, scl = scores
    # Simple deterministic component pick based on sliders + focus
    base = ["Route53", "CloudFront", "ALB"]
    compute = "AWS Fargate (ECS)" if prf>=70 else "AWS Lambda"
    db = "Amazon Aurora (PostgreSQL)" if prf>=70 and sec>=70 else "Amazon RDS (PostgreSQL)"
    cache = "Amazon ElastiCache (Redis)" if lat>=60 else "Local in-memory cache"
    queue = "Amazon SQS" if scl>=70 else "None"
    stream = "Amazon Kinesis" if ("IoT" in focus or "analytics" in focus.lower() or "stream" in focus.lower()) else "None"
    storage = "Amazon S3 (Encrypted, private)" 
    sec_stack = ["AWS IAM", "AWS KMS", "AWS WAF", "Security Groups", "VPC Private Subnets"]

    # GDPR/NIS2 hints
    compliance = ["Data minimization", "Encryption at rest & transit", "Regional data residency options", "Audit logs (CloudTrail)"]

    return {
        "entry": base,
        "compute": compute,
        "db": db,
        "cache": cache,
        "queue": queue,
        "stream": stream,
        "storage": storage,
        "security": sec_stack,
        "compliance": compliance
    }

def draw_architecture_graph(arch):
    G = nx.DiGraph()
    # nodes
    for n in arch["entry"]:
        G.add_node(n)
    G.add_node(arch["compute"])
    G.add_node(arch["db"])
    G.add_node(arch["cache"])
    if arch["queue"]!="None": G.add_node(arch["queue"])
    if arch["stream"]!="None": G.add_node(arch["stream"])
    G.add_node(arch["storage"])
    # edges
    G.add_edge("Route53", "CloudFront")
    G.add_edge("CloudFront", "ALB")
    G.add_edge("ALB", arch["compute"])
    G.add_edge(arch["compute"], arch["db"])
    G.add_edge(arch["compute"], arch["cache"])
    if arch["queue"]!="None":
        G.add_edge(arch["compute"], arch["queue"])
    if arch["stream"]!="None":
        G.add_edge(arch["compute"], arch["stream"])
    if arch["stream"]!="None":
        G.add_edge(arch["stream"], arch["storage"])
    else:
        G.add_edge(arch["compute"], arch["storage"])

    pos = nx.spring_layout(G, seed=7, k=1.1)
    fig, ax = plt.subplots(figsize=(7,5))
    nx.draw_networkx_nodes(G, pos, node_size=900, node_color="#e0f2fe", edgecolors="#0284c7", linewidths=1.5, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold", ax=ax)
    nx.draw_networkx_edges(G, pos, width=1.5, arrows=True, arrowstyle="-|>", ax=ax)
    ax.set_title("Proposed Architecture", fontsize=12)
    ax.axis("off")
    return fig

def explain_architecture_text(focus, scores, arch):
    # Template-based NLP explanation (5–10 lines), no external model
    lat, lb, cst, prf, sec, scl = scores
    lines = []
    lines.append(f"This design targets: {focus}.")
    lines.append(f"Traffic enters via {', '.join(arch['entry'])}, then flows to {arch['compute']} for stateless compute.")
    if arch["cache"] != "Local in-memory cache":
        lines.append(f"Hot paths are accelerated using {arch['cache']} to reduce latency.")
    lines.append(f"Stateful data persists in {arch['db']} with {arch['storage']} for objects/logs.")
    if arch["queue"]!="None":
        lines.append(f"Decoupling with {arch['queue']} helps absorb spikes and improve reliability.")
    if arch["stream"]!="None":
        lines.append(f"Real-time events stream through {arch['stream']} enabling near real-time analytics.")
    lines.append("Security is enforced with IAM least-privilege, KMS encryption, WAF, and private subnets.")
    lines.append("GDPR/NIS2 considerations: data minimization, regional data residency, and full audit logging.")
    lines.append(f"The sliders guided trade-offs (latency {lat}, load {lb}, cost {cst}, performance {prf}, security {sec}, scale {scl}).")
    return "\n".join(lines[:9])

def risk_score(scores):
    # Higher security & scalability reduce risk; high latency need also affects risk
    lat, lb, cst, prf, sec, scl = scores
    base = 70 - (sec*0.25 + scl*0.15) + (100-lb)*0.1 + (100-prf)*0.1 + (lat*0.05) + (cst*0.05)
    return max(0, min(100, round(base, 1)))

def find_compliance_gaps(arch):
    gaps = []
    if "WAF" not in " ".join(arch["security"]):
        gaps.append("Add WAF for L7 filtering.")
    gaps.append("Ensure DPIA where required and document lawful basis for processing.")
    gaps.append("Formalize data retention & deletion schedules per GDPR Art. 5(1)(e).")
    return gaps

# ------------------ Action Button -----------------------
run = st.button("🤖 Run Agentic Design")

# ------------------ Main Flow ---------------------------
if run:
    st.markdown("### 🧠 Agentic Reasoning")
    scores = [latency, load, cost, perf, security, scale]

    # Show each agent's thinking with seconds
    cols = st.columns(4)
    reasoning_log = []
    for i, (name, role) in enumerate(agents):
        with cols[i]:
            with st.expander(f"{name} — thinking...", expanded=True):
                start = time.time()
                st.write(f"**Role:** {role}")
                thoughts = agent_reasoning(name, role, scores, use_case + " " + focus)
                # simulate progressive thinking
                for idx, t in enumerate(thoughts, start=1):
                    time.sleep(0.6)
                    st.write(f"- {t}")
                    elapsed = time.time() - start
                    st.caption(f"Elapsed: {elapsed:.1f} sec")
                reasoning_log.append((name, thoughts))

    # Build architecture from sliders + focus
    arch = build_architecture(focus, scores)

    # KPIs
    st.markdown("### 📊 Quick Checks")
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f"<div class='kpi'><b>Risk Score</b><br><span class='small-muted'>{risk_score(scores)}/100 (lower is better)</span></div>", unsafe_allow_html=True)
    with k2:
        st.markdown(f"<div class='kpi'><b>Primary Compute</b><br><span class='small-muted'>{arch['compute']}</span></div>", unsafe_allow_html=True)
    with k3:
        st.markdown(f"<div class='kpi'><b>Data Store</b><br><span class='small-muted'>{arch['db']}</span></div>", unsafe_allow_html=True)

    # Compliance gaps
    st.markdown("### ⚖️ Compliance Gap Finder (GDPR/NIS2)")
    gaps = find_compliance_gaps(arch)
    if gaps:
        for g in gaps:
            st.markdown(f"- {g}")
    else:
        st.markdown("- No obvious gaps found in this MVP template.")

    # ---------------- Proposed Architecture (Always Visible) ----------------
    st.markdown("### 🏗️ Proposed Architecture (Always Visible)")
    fig = draw_architecture_graph(arch)
    st.pyplot(fig)

    # ------ 5–10 line automatic explanation (template-NLP, no external API) ------
    st.markdown("#### 🧾 Architecture Explanation (Auto-generated)")
    st.markdown(explain_architecture_text(focus, scores, arch))

    # ---------------- Downloadable Docs ----------------
    st.markdown("### ⤵️ Downloads")
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    tutorial_text = f"""TUTORIAL — How to Build This Architecture (Generated)
Time: {ts}

1) DNS & Edge: Configure Route53 -> CloudFront for global entry and caching.
2) Ingress: Route from CloudFront to ALB with WAF enabled.
3) Compute: Deploy {'Fargate (ECS) services' if 'Fargate' in arch['compute'] else 'Lambda functions'} with stateless design.
4) State: Use {arch['db']} for OLTP; {arch['storage']} for objects, logs, and backups.
5) Caching: {arch['cache']} for hot keys and session tokens.
6) Decoupling: {arch['queue']} for async jobs and spikes.
7) Streaming: {arch['stream']} for real-time events (if applicable).
8) Security: IAM least-privilege, KMS encryption, security groups, private subnets.
9) Observability: CloudWatch metrics/logs + alarms; structured app logs.
10) Compliance: Data minimization, regional residency, audit trails (CloudTrail).
"""

    tdd_text = f"""TECHNICAL DESIGN DOCUMENT (Generated)
Time: {ts}

Focus: {focus}
Primary Compute: {arch['compute']}
Data Store: {arch['db']}
Cache: {arch['cache']}
Queue: {arch['queue']}
Stream: {arch['stream']}
Object Storage: {arch['storage']}
Ingress: {', '.join(arch['entry'])}

Non-Functional:
- Performance target guided by sliders (latency={latency}, performance={perf})
- Resilience via load balancing={load}, decoupling={arch['queue']}
- Scalability target={scale}
- Security baseline={', '.join(arch['security'])}
- Compliance: {', '.join(arch['compliance'])}

Sequence (high-level):
1) Client -> Route53 -> CloudFront -> ALB
2) ALB -> {arch['compute']}
3) App -> {arch['db']} (R/W), {arch['cache']} (hot path)
4) App -> {('Stream: ' + arch['stream']) if arch['stream']!='None' else 'Optional stream: None'}
5) Data -> {arch['storage']} for objects/logs
"""

    st.download_button("📥 Download Tutorial (.txt)", data=tutorial_text, file_name="tutorial.txt")
    st.download_button("📥 Download Technical Design Doc (.txt)", data=tdd_text, file_name="technical_design_doc.txt")

    # ---------------- How to Use (bottom) ----------------
    st.markdown("---")
    st.markdown("## 📚 How to Use (Step-by-step)")
    howto_steps = [
        "Set your design priorities with the sliders (latency, load balancing, cost, performance, security, scalability).",
        "Choose an Architecture Focus from the dropdown.",
        "Paste or type your Use Case / RFP / Epic user story in the big text box.",
        "Click **Run Agentic Design** to start.",
        "Watch four agents think like humans; you can see seconds elapsed per agent.",
        "Review the Risk Score, primary compute choice, and data store choice.",
        "Check the Compliance Gap Finder for GDPR/NIS2 hints.",
        "Scroll to **Proposed Architecture** to view the diagram.",
        "Read the auto-generated **Architecture Explanation** for a quick summary.",
        "Download the Tutorial and Technical Design Document if needed.",
        "Click **New Architecture** in the sidebar to reset and design another.",
        "Iterate and tweak sliders to see trade-off impacts.",
        "Use the diagram as a starting blueprint for real delivery.",
        "Share your Streamlit app URL on your resume.",
        "This MVP avoids paid APIs and heavy dependencies, suitable for free hosting."
    ]
    # Display steps in two columns with numbered bullets and soft styling
    left, right = st.columns(2)
    half = math.ceil(len(howto_steps)/2)
    with left:
        for i, s in enumerate(howto_steps[:half], start=1):
            st.markdown(f"<div class='hint'><b>Step {i}:</b> {s}</div>", unsafe_allow_html=True)
    with right:
        for i, s in enumerate(howto_steps[half:], start=half+1):
            st.markdown(f"<div class='hint'><b>Step {i}:</b> {s}</div>", unsafe_allow_html=True)

else:
    st.markdown("<div class='badge'>Tip</div> Adjust the sliders, choose a focus, paste your use case, then hit <b>Run Agentic Design</b>.", unsafe_allow_html=True)
