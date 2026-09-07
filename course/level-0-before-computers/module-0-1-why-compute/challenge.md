# Challenge 0.1 — The Cost of Human Computation

**Type:** Calculation + reasoning  
**Estimated time:** 20–30 minutes  
**Tools needed:** Pen and paper (or a calculator — ironic, we know)

---

## Setup

The 1880 US Census counted approximately **50,000,000 people**. Each person's record included 5 data fields: name, age, occupation, birthplace, and family size.

A trained human "computer" in 1880 could process (read, tally, and record) roughly **500 records per day**, working an 8-hour day.

The Hollerith tabulating machine (1890) could process roughly **65 cards per minute**, running 8 hours a day.

---

## Questions

### Part A — Human Cost

1. How many **person-days** of work would it take to process all 50 million census records by hand?

2. If the government employed **500 clerks** working simultaneously, how many **calendar days** would the job take?

3. Convert that to **years**. Does this match the historical 8-year figure? If not, what might explain the gap?

---

### Part B — Machine Cost

4. How many **cards per day** can the Hollerith machine process (cards/min × 60 min/hr × 8 hrs)?

5. How many **days** would it take to process all 50 million records with **one machine**?

6. The 1890 Census used approximately **100 Hollerith machines** simultaneously. How many days did it actually take?

7. The historical record says the 1890 Census was tabulated in **6 weeks**. Does your calculation agree? Show the math.

---

### Part C — The Leap

8. What is the **speedup factor** — how many times faster was the Hollerith machine approach vs the 500-clerk approach?

9. In your own words (2–3 sentences): why does this speedup matter beyond just saving time? Think about accuracy, cost, and what new possibilities it opened up.

---

## Rubric

| Part | Points | What we're looking for |
|------|--------|------------------------|
| A1 | 10 | Correct division: 50,000,000 ÷ 500 |
| A2 | 10 | Correct division by 500 clerks |
| A3 | 15 | Correct year conversion + honest analysis of the gap |
| B4 | 10 | Correct multiplication: 65 × 60 × 8 |
| B5 | 10 | Correct division of 50M by daily rate |
| B6 | 10 | Correct division by 100 machines |
| B7 | 15 | Comparison to 6-week historical figure |
| C8 | 10 | Speedup ratio calculated correctly |
| C9 | 10 | Thoughtful reasoning about implications |

**Total: 100 points**

---

## Hints

<details>
<summary>Hint 1 — Part A1</summary>
Person-days = total records ÷ records per person per day
</details>

<details>
<summary>Hint 2 — Part B4</summary>
Don't forget to convert: the machine rate is per minute, but you want per day.
</details>

<details>
<summary>Hint 3 — Part A3 gap</summary>
The 8 years wasn't just counting — it included compilation, error correction, typesetting, and publication. Pure counting was faster; the bottleneck was everything around it.
</details>

---

## Solution

*(Attempt all parts before expanding)*

<details>
<summary>Full Solution</summary>

**A1:** 50,000,000 ÷ 500 = **100,000 person-days**

**A2:** 100,000 ÷ 500 clerks = **200 calendar days** ≈ 0.55 years just for processing

**A3:** 0.55 years for raw counting. The 8-year figure includes the full pipeline: data collection in the field, transport, verification, tabulation, error resolution, compilation, and printing. The bottleneck was the whole system, not just counting speed.

**B4:** 65 cards/min × 60 min/hr × 8 hrs = **31,200 cards per day**

**B5:** 50,000,000 ÷ 31,200 = **~1,603 days** for one machine

**B6:** 1,603 ÷ 100 machines = **~16 days**

**B7:** 16 days ≈ 2.3 weeks. Historical record says 6 weeks. The extra time covers setup, card punching, verification passes, and final tabulation — not just machine reading. The calculation confirms the order of magnitude.

**C8:** Human approach: 200 days for 500 clerks. Machine approach: ~16 days for 100 machines.  
Speedup ≈ 200/16 = **~12.5×** on calendar time. But the machine approach used fewer workers and ran more reliably.

**C9 (example):** The speedup didn't just save time — it made the data *usable*. Results delivered in 6 weeks could influence policy within that Congress. Results delivered in 8 years were already stale. Automation didn't just accelerate counting; it made accurate, timely large-scale data collection possible for the first time.

</details>
