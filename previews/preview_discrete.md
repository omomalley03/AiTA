# Lecture Preview: Discrete Categorical Distribution
**Lecturer:** Carl Edward Rasmussen | **Date:** November 11th, 2016

⸻

## Big Picture Motivation

This lecture extends our understanding from **binary random variables** to **multiple discrete outcomes**. Just as we moved from single coin flips (Bernoulli) to counting heads in multiple flips (Binomial), we now generalize to scenarios with more than two possible outcomes—like rolling a die or counting word frequencies in text.

⸻

## Part 1: The Multinomial Distribution

### Intuition
Imagine rolling a fair die n = 60 times and recording how often each face appears. The multinomial distribution tells us the probability of observing any particular combination of counts.

### Mathematical Formulation
For a discrete random variable X that can take one of m values x₁, ..., xₘ:
- Let kᵢ = number of times X = xᵢ was observed in n trials
- Let πᵢ = P(X = xᵢ) be the probability of outcome i

**Constraints:**
- Σᵢ₌₁ᵐ kᵢ = n (counts must sum to total trials)
- Σᵢ₌₁ᵐ πᵢ = 1 (probabilities must sum to 1)

**The Multinomial Distribution:**
$$p(k | \pi, n) = \frac{n!}{k_1! k_2! \cdots k_m!} \prod_{i=1}^{m} \pi_i^{k_i}$$

**Key observations:**
- The multinomial coefficient n!/(k₁!k₂!...kₘ!) generalizes the binomial coefficient C(n,k)
- We can write p(k | π) since n is redundant (determined by the kᵢ values)

### The Categorical Distribution
The **categorical distribution** is the single-trial special case:
$$p(X = x_i | \pi) = \pi_i$$

This is the generalization of the Bernoulli distribution from 2 outcomes to m outcomes.

⸻

## Part 2: The Dirichlet Distribution

### Why Do We Need It?
Just as the Beta distribution provides a prior over the parameter p of a Bernoulli/Binomial, the **Dirichlet distribution** provides a prior over the probability vector π of a categorical/multinomial.

### Geometric Intuition
The probability vector π = [π₁, ..., πₘ] lives on the **(m-1)-dimensional simplex**—the space of all valid probability distributions over m outcomes. For m = 3, this is a triangle; for m = 4, a tetrahedron.

### Mathematical Formulation
$$\text{Dir}(\pi | \alpha_1, ..., \alpha_m) = \frac{\Gamma(\sum_{i=1}^{m} \alpha_i)}{\prod_{i=1}^{m} \Gamma(\alpha_i)} \prod_{i=1}^{m} \pi_i^{\alpha_i - 1} = \frac{1}{B(\alpha)} \prod_{i=1}^{m} \pi_i^{\alpha_i - 1}$$

**Where:**
- α = [α₁, ..., αₘ] are the **shape parameters**
- B(α) is the **multivariate beta function** (normalization constant)
- E(πⱼ) = αⱼ / Σᵢαᵢ is the mean of the j-th component

⸻

## Part 3: The Symmetric Dirichlet Distribution

### Definition
When all shape parameters are equal (αᵢ = α for all i), we get the **symmetric Dirichlet distribution**.

### The Concentration Parameter α
The single parameter α controls the "concentration" of probability mass:

| α value | Behavior |
|---------|----------|
| α < 1 (e.g., 0.1) | Sparse distributions—probability concentrated on few outcomes |
| α = 1 | Uniform distribution over the simplex |
| α > 1 (e.g., 10) | Concentrated near uniform—all πᵢ ≈ 1/m |

### Sampling Code (MATLAB)
```matlab
w = randg(alpha, D, 1);
bar(w / sum(w));
```

⸻

## Application Example: Word Counts in Text

A practical application is the **bag-of-words model** for text documents:
- Each document is represented by word frequency counts
- The multinomial distribution models the probability of observing a particular word count vector
- The Dirichlet distribution can serve as a prior over topic-word distributions

This forms the foundation for models like **Latent Dirichlet Allocation (LDA)** for topic modeling.

⸻

## Summary of Key Relationships

| Binary Case | Multi-outcome Generalization |
|-------------|-----------------------------|
| Bernoulli | Categorical |
| Binomial | Multinomial |
| Beta | Dirichlet |

The Dirichlet is a "probability distribution over probability distributions"—it tells us how likely different probability vectors π are before we observe any data.