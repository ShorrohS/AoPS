# Module 12.5 — Ethics and Safety in AI Systems

---

## The Problem

> A hiring algorithm trained on historical data learns to discriminate.
> A content recommendation system optimises engagement — and radicalises users.
> A self-driving car must decide who to harm in an unavoidable crash.
> A large language model confidently states false information.
>
> These are not hypothetical future problems.
> They are happening now, in systems deployed at scale.
>
> Building AI systems responsibly requires understanding
> not just the technical mechanisms but the ethical frameworks,
> failure modes, and safety techniques that prevent harm.

---

## The Story

### From Science Fiction to Policy

The ethics of artificial intelligence has been discussed since the technology was theoretical. Isaac Asimov's Three Laws of Robotics (1942) were the first popular framing — and Asimov's stories systematically showed why rule-based ethics fails in complex situations.

Real concerns emerged as AI systems moved from research to deployment:
- **2014**: Microsoft's Tay chatbot learned to generate hate speech within 24 hours of deployment
- **2016**: ProPublica reported that COMPAS (a recidivism prediction system) showed racial bias in US courts
- **2019**: Amazon scrapped an AI recruiting tool that discriminated against women (trained on historical hiring data that was male-dominated)
- **2022**: ChatGPT demonstrated that large language models could produce fluent, confident, incorrect text — "hallucination" — at scale
- **2023–2024**: Regulatory responses — EU AI Act, US Executive Order on AI — attempted to create frameworks for accountability

The technical AI safety field grew from concerns about existential risk. **Nick Bostrom's** *Superintelligence* (2014) and work at organisations like MIRI (Machine Intelligence Research Institute) and later Anthropic focused on alignment: how do you ensure an AI system pursues the goals its creators intended, not some proxy that diverges catastrophically?

---

## The Concept

### Bias and Fairness

**What is bias in ML?** A model trained on biased data learns biased patterns.

```python
# Simplified example
# Historical data: women hired at lower rates (due to past discrimination)
# Model trained on this data: predicts women as lower probability hires
# Outcome: perpetuates and entrenches the historical bias
```

**Sources of bias:**
- **Historical bias**: data reflects past discrimination
- **Representation bias**: certain groups are underrepresented in training data
- **Measurement bias**: the variable being predicted is a proxy for something else
- **Feedback loops**: biased predictions → biased outcomes → biased future training data

**Fairness metrics** (often incompatible with each other):
- **Demographic parity**: equal positive prediction rates across groups
- **Equal opportunity**: equal true positive rates across groups
- **Predictive parity**: equal precision across groups
- **Individual fairness**: similar individuals treated similarly

**Impossibility results**: it is mathematically impossible to satisfy all fairness criteria simultaneously when base rates differ between groups. Any choice of fairness definition encodes a value judgment — there is no purely technical solution to what is fundamentally a societal question.

### Explainability and Interpretability

**The black box problem**: deep neural networks make decisions through millions of learned parameters. Even the system's creators cannot fully explain why it made a specific decision.

**Why it matters**: in high-stakes domains (medical diagnosis, loan decisions, criminal justice), decision subjects have a right to an explanation. The EU GDPR includes a "right to explanation" for automated decisions.

**Techniques:**
- **LIME** (Local Interpretable Model-Agnostic Explanations): approximate the model locally with a simpler interpretable model
- **SHAP** (SHapley Additive exPlanations): use Shapley values (from game theory) to attribute each feature's contribution to a prediction
- **Attention visualisation**: in transformer models, attention weights show which input tokens influenced the output
- **Gradient-based saliency**: compute the gradient of the output with respect to inputs to identify which inputs most affected the decision

```python
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test, feature_names=feature_names)
```

### Hallucination and Truthfulness

**Hallucination**: a language model confidently states false information. This is not a bug in the traditional sense — it is an emergent property of how LLMs work:

- LLMs are trained to predict likely next tokens, not to retrieve facts from a verified database
- Fluent, confident-sounding text and accurate text are statistically correlated but not identical
- The model has no internal "truth check" — it cannot distinguish what it knows from what it is confabulating

**Mitigation techniques:**
- **Retrieval-Augmented Generation (RAG)**: ground LLM responses in retrieved documents (Module 12.3)
- **Calibration**: train models to express uncertainty when appropriate
- **Constitutional AI** (Anthropic): train models using AI feedback on their own outputs against a set of principles
- **Human feedback (RLHF)**: fine-tune models on human ratings of response quality

### Alignment: The Core Problem

**The alignment problem**: how do you specify what you want an AI system to do, precisely enough that a system optimising for that specification actually does what you intended?

Classic examples:
- "Make users happy" → system learns to addict users to endless scroll
- "Get a high score in this game" → agent discovers an exploit that earns points without playing the game as intended
- "Reduce hospital wait times" → system discharges sick patients early

**Reward hacking**: any learnable proxy metric can be gamed if the system is optimising it hard enough.

**RLHF (Reinforcement Learning from Human Feedback)**: a leading approach to alignment. Train a reward model from human preference comparisons, then use RL to fine-tune the LLM to produce responses that the reward model rates highly. Used to train GPT-4, Claude, and Gemini.

The fundamental challenge: the reward model itself may have biases, blind spots, or specifications that diverge from true human values at the margin. Scalable oversight — how to supervise a system smarter than yourself — is an open research problem.

### Privacy and Data

**Training data privacy concerns:**
- Models can **memorise** training data, including personal information. LLMs can be prompted to reveal training data examples — including private information, copyrighted text, or PII.
- **Membership inference attacks**: determine whether a specific example was in the training set.
- **Differential privacy**: add calibrated noise to training or outputs to provide mathematical privacy guarantees (Laplace mechanism, Gaussian mechanism). At the cost of some model quality.

**Copyright and consent:**
- Training on web-scraped data involves text, images, and code for which creators did not give permission
- Multiple ongoing lawsuits (NYT vs OpenAI, Getty Images vs Stability AI, GitHub Copilot lawsuits)
- Technical and legal resolution is evolving rapidly

### AI Safety Frameworks

**Red-teaming**: systematically attempt to elicit harmful outputs from a model. Developed in security research, now standard practice before LLM deployment.

**Responsible disclosure**: when vulnerabilities are found in AI systems, how should they be reported? The same principles as software security but with less established norms.

**Model cards**: documentation accompanying ML models describing training data, evaluation metrics, known limitations, intended use cases, and out-of-scope uses. Introduced by Google researchers (Timnit Gebru et al., 2018).

**Staged deployment**: release models gradually (to researchers, then limited users, then generally) to identify failure modes before broad exposure.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Bias Audit**
- A loan approval model with demographic features
- Compute fairness metrics: demographic parity, equal opportunity, predictive parity
- See that optimising for one metric degrades others

**Tool 2 — SHAP Explanation**
- A model predicts loan approval
- Explain one prediction: which features contributed how much?
- Interpret: "this application was rejected primarily because income < threshold, partially offset by long credit history"

**Tool 3 — Red Teaming Exercise**
- A simulated chatbot with safety guidelines
- Attempt various prompt injections and adversarial inputs
- See which succeed, which fail, and why

---

## Going Deeper

**AI governance and regulation**: the EU AI Act (2024) creates a risk-based framework: high-risk applications (medical, criminal justice, employment) require conformity assessments, transparency, and human oversight. Prohibited applications include: social scoring, real-time facial recognition in public spaces. Understanding the technical implications of compliance — what does it mean to document "training data characteristics" or provide "meaningful human oversight" for a production ML system — is a growing area of applied AI engineering.

**AI consciousness and moral status**: the question of whether AI systems can suffer or have interests is philosophically unresolved but increasingly practically relevant. As AI systems become more capable and exhibit more human-like behaviour, questions about their moral status will become urgent. Serious philosophers (David Chalmers, Nick Bostrom) and AI researchers (Geoffrey Hinton post-Google) engage with this seriously.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Audit a given ML model for demographic disparities (compute precision and recall separately for two groups), write a model card for a fictitious image classifier (what information should it contain?), propose a mitigation for each of three named AI failure modes (hallucination, reward hacking, training data bias), and explain why "just remove the protected attribute" does not eliminate discrimination in practice.
