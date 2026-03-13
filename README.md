# 🧠 Global Mental Health Crisis — Interactive Data Dashboard

**Live App → [https://mental-health-trends-analyzer.streamlit.app/]

An interactive data storytelling dashboard that explores the global mental health crisis across 40 countries — and reflects it back to you personally through an AI-powered mirror.

---

## What It Does

Most mental health dashboards show you data. This one tells a story — and then turns the lens on you.

**Act I — The World Map**
Interactive choropleth across 40 countries. Toggle between depression prevalence, suicide rates, psychiatrist access, and treatment gap. Real WHO & IHME data, not estimates.

**Act II — Mental Health Inequality Index (MHII)**
An original composite metric built for this dashboard. Combines psychiatrist access (40%), treatment gap (30%), government mental health spending (20%), and suicide rate (10%) into a single country-level score. Ranked bar chart + country deep-dive with all raw metrics.

**Act III — Country Deep Dive**
Select any country — get a full profile: MHII rank, depression rate, suicide rate, psychiatrists per 100k, treatment gap. For the US, this expands to a state-level choropleth (CDC PLACES 2023) + age group trend lines from 2011–2021.

**Act IV — The Personal Mirror**
The differentiator. Fill out 6 questions about your actual life — workload, sleep, finances, social support, coping style, pressure sources. The app:
- Computes your stress profile score and visualizes it on a radar chart vs. the average
- Estimates what % of people with your profile report frequent mental distress
- Sends your profile + dynamically selected data context to **Llama 3.3 70B via Groq**
- Returns a 3-part analysis: the hidden pattern in your inputs, a mirror moment connecting your experience to real data, and one non-obvious lever specific to your constraints

The AI is explicitly prompted to avoid generic wellness advice and to reason about the *combination* of your inputs — not each one in isolation.

---

## Data Sources

All data is real. No fabrications.

| Dataset | Source | Coverage |
|---|---|---|
| Depression & anxiety prevalence | IHME Global Burden of Disease 2019 (Lancet Psychiatry 2022) | 40 countries |
| Suicide rates | WHO GHO API (MH_12), age-standardized, 2019 | 40 countries |
| Psychiatrists per 100k | WHO GHO API (MH_6), most recent available | 40 countries |
| Mental health spending | WHO Mental Health Atlas 2020 | 40 countries |
| Treatment gap | WHO World Mental Health Report 2022 | 40 countries |
| US state distress rates | CDC PLACES 2023, frequent mental distress, age-adjusted | 48 states |
| US age group trends | America's Health Rankings Mental & Behavioral Health Data Brief 2023 (BRFSS) | 2011–2021 |

---

## Tech Stack

- **Frontend/App:** Streamlit
- **Data:** Pandas, NumPy
- **Visualizations:** Plotly (choropleth maps, radar charts, bar charts, trend lines)
- **AI:** Groq API — Llama 3.3 70B Versatile
- **Deployment:** Streamlit Cloud

---

## Original Analysis

The **Mental Health Inequality Index (MHII)** is an original composite metric developed for this project. It measures not just how prevalent mental illness is in a country, but how well that country *responds* to it. The methodology:

```
MHII = (psychiatrists_score × 0.40) + 
       (inverse_treatment_gap × 0.30) + 
       (mh_spending_score × 0.20) + 
       (inverse_suicide_rate × 0.10)
```

All components normalized 0–100 before weighting. Higher score = better mental health infrastructure and response.

---

## Running Locally

```bash
git clone https://github.com/preiyalthakkar3007/mental-health-trends-analyzer
cd mental-health-trends-analyzer
pip install -r requirements.txt
```

Set your Groq API key (free at [console.groq.com](https://console.groq.com)):
```bash
# Windows PowerShell
$env:GROQ_API_KEY = "your_key_here"

# Mac/Linux
export GROQ_API_KEY="your_key_here"
```

```bash
streamlit run app.py
```

The Personal Mirror feature requires a Groq API key. All other features work without it.

---

## Key Design Decisions

**Why Groq instead of OpenAI?** Free tier is generous enough for a portfolio project, and Llama 3.3 70B produces sharp enough output for this use case.

**Why coping-style-specific prompt branches?** A single generic prompt produces similar analyses regardless of inputs. By branching on coping archetype (push through / distract / shut down / talk / situational), the entire framing changes — different mechanism identified, different mirror angle, different lever.

**Why dynamic context injection?** Instead of sending the same 5 data bullets to everyone, the app only injects data points relevant to that person's specific profile combination. Someone with financial stress gets the financial stress mechanism. Someone with weak social support gets the co-regulation data point.

---

## Disclaimer

This tool is for informational and educational purposes only. It does not constitute medical advice or clinical assessment.

If you're in crisis: **988 Lifeline** (call/text 988) · **Crisis Text Line** (text HOME to 741741)

---

Built by [Preiyal Thakkar](https://github.com/preiyalthakkar3007)