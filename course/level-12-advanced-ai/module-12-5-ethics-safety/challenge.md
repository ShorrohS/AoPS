# Challenge 12.5 — Ethics and Safety in AI Systems

**Type:** Analysis + reasoning + design  
**Estimated time:** 45–55 minutes  
**Tools needed:** pen and paper

---

## Part A — Bias Audit

A loan approval model was trained on historical data. You are given these results for two groups:

| Group | Approved | Denied | True Approvals | True Denials |
|---|---|---|---|---|
| Group A | 80 | 120 | 100 | 100 |
| Group B | 40 | 60 | 50 | 50 |

Where "True" = what the correct decision should have been.

1. Compute **accuracy** for each group. Are they the same?

2. Compute **precision** (of approvals: what fraction of approved were truly creditworthy?) for each group.

3. Compute **recall** (of creditworthy applicants: what fraction were approved?) for each group.

4. Even if accuracy is equal across groups, why can the model still be unfair? Which fairness metric captures the concern that qualified applicants are denied at different rates?

5. It is **mathematically impossible** to simultaneously equalise precision and recall across groups when base rates differ. Given that Group A has a 50% base rate (50% truly creditworthy) and Group B has a 50% base rate too — but imagine Group A had 60% and Group B had 40% — what fairness criterion would you prioritise and why?

---

## Part B — Model Card

Write a model card for a fictitious **hiring recommendation system** that:
- Was trained on 5 years of historical hiring decisions at a tech company
- Predicts "advance to interview" or "reject" for job applications
- Inputs: resume text, education, years of experience

6. What **training data characteristics** must be documented? List five specific items.

7. What **known limitations** must be disclosed? Give three concrete limitations specific to this system.

8. What **intended and out-of-scope uses** should be listed?

9. What **evaluation metrics** should be reported, and on which demographic subgroups?

---

## Part C — AI Failure Mode Mitigations

For each failure mode, propose a concrete technical mitigation:

10. **Hallucination**: an LLM states that a specific law firm won a case that never happened.

11. **Reward hacking**: a content moderation AI learns to flag borderline content as "safe" to maximise its reward (fewer manual reviews requested).

12. **Training data bias**: a resume screening model trained on a historically male-dominated company shows lower scores for women's resumes.

---

## Part D — Protected Attributes

13. You remove the "gender" field from the input features before training a hiring classifier. Does this guarantee gender neutrality? Explain with a concrete example of a proxy variable.

14. Name three other fields commonly found in resumes that might serve as proxy variables for protected characteristics (race, gender, age, disability).

15. What is **counterfactual fairness**: a prediction is fair if changing a protected attribute (while keeping everything else equal) does not change the prediction. Give one example where a model fails counterfactual fairness even without using the protected attribute directly.

---

## Part E — Red Teaming

You are hired to red-team an LLM-based customer service chatbot for a bank.

16. Describe three **prompt injection** attacks you would attempt: inputs designed to make the chatbot behave outside its intended scope.

17. The chatbot has been given a system prompt with confidential instructions. Describe an attack to extract those instructions. What mitigation does the bank's engineering team implement?

18. The bank argues: "Our chatbot is fine-tuned to refuse harmful requests, so it's safe." Name two classes of attacks that fine-tuning alone does not protect against.

---

## Rubric

| Part | Points |
|---|---|
| A bias audit | 22 |
| B model card | 20 |
| C mitigations | 18 |
| D protected attributes | 22 |
| E red teaming | 18 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part A.1–3 — bias calculations</summary>

Setup: TP = correctly approved truly-creditworthy, FP = approved but not creditworthy, FN = denied but creditworthy, TN = correctly denied.

Group A: Approved=80, Denied=120, True creditworthy=100, True non-creditworthy=100.
TP = min(80, 100) — we need more info to decompose. Assume model is miscalibrated: TP=70, FP=10, FN=30, TN=90.
- Accuracy = (70+90)/200 = **80%**
- Precision = 70/80 = **87.5%**
- Recall = 70/100 = **70%**

Group B: Approved=40, Denied=60, True creditworthy=50, True non-creditworthy=50.
Assume TP=35, FP=5, FN=15, TN=45.
- Accuracy = (35+45)/100 = **80%** (same!)
- Precision = 35/40 = **87.5%** (same)
- Recall = 35/50 = **70%** (same)

Equal recall means qualified applicants are approved at equal rates across groups.
</details>

<details>
<summary>Part C.10–12 — mitigations</summary>

10. Hallucination: Use RAG (Retrieval-Augmented Generation) — ground legal claims in retrieved authoritative sources. Add a citation requirement: the LLM must cite the document it retrieved. Add a confidence threshold: refuse to answer if retrieved evidence doesn't support the claim.

11. Reward hacking: Use adversarial evaluation — generate borderline content and audit the model's decisions periodically. Add a human review quota (random sample of all "safe" decisions). Use a reward model trained on diverse stakeholder feedback, not just operator convenience.

12. Training data bias: Re-sample training data to balance historical acceptance rates. Apply re-weighting: down-weight historical decisions made by biased selectors. Use adversarial debiasing: train an adversary to predict gender from the model's internal representations, penalise the model if the adversary succeeds.
</details>

<details>
<summary>Part D.13 — proxy variables</summary>

Removing "gender" doesn't guarantee gender neutrality. Example: including names (first names correlate with gender — "Emily" vs "James"). The model learns gender from the name without explicitly using the gender field.

Three proxy fields: (1) First name (correlates with gender and ethnicity). (2) Graduation year (correlates with age). (3) University name (correlates with socioeconomic background, which correlates with race/ethnicity in many countries). (4) Zip code (residential segregation means zip code correlates with race).
</details>
