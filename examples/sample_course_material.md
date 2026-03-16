# Chapter 1: The Perceptron and Linear Models

*Sample course material for demonstrating Socrates-7. Based on standard deep learning introductory content.*

---

## 1.1 The Perceptron

A perceptron is the simplest possible neural network: a single neuron that computes a weighted sum of its inputs and passes the result through an activation function.

Given inputs $x_1, x_2, \ldots, x_n$ and weights $w_1, w_2, \ldots, w_n$, the perceptron computes:

$$z = \sum_{i=1}^{n} w_i x_i + b$$

where $b$ is the bias term. The output is then:

$$y = f(z)$$

where $f$ is the activation function. In the original perceptron, $f$ is the step function:

$$f(z) = \begin{cases} 1 & \text{if } z \geq 0 \\ 0 & \text{if } z < 0 \end{cases}$$

### Decision Boundaries

A single perceptron with two inputs defines a linear decision boundary — a line in 2D (or a hyperplane in higher dimensions). The equation $w_1 x_1 + w_2 x_2 + b = 0$ defines this boundary. Points on one side are classified as 1; points on the other side as 0.

The weight vector $\mathbf{w} = (w_1, w_2)$ is perpendicular to the decision boundary and points toward the positive region. The bias $b$ shifts the boundary away from the origin.

---

## 1.2 The XOR Problem

A single perceptron cannot solve the XOR (exclusive or) problem. XOR is defined as:

| $x_1$ | $x_2$ | XOR |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

No single line can separate the positive examples $(0,1)$ and $(1,0)$ from the negative examples $(0,0)$ and $(1,1)$. This is because XOR is not linearly separable.

### The Multi-Layer Solution

XOR can be solved by combining two perceptrons in a hidden layer with a third perceptron in the output layer. The key insight: the hidden layer transforms the input space into a new representation where the classes become linearly separable.

For example, one hidden neuron can compute $h_1 = (x_1 \text{ AND NOT } x_2)$ and another can compute $h_2 = (x_2 \text{ AND NOT } x_1)$. The output neuron then computes $y = (h_1 \text{ OR } h_2)$, which is exactly XOR.

---

## 1.3 Activation Functions

The step function used in the original perceptron has a critical flaw: it is not differentiable, which means we cannot use gradient-based optimization to train it.

### Sigmoid

The sigmoid function provides a smooth, differentiable alternative:

$$\sigma(x) = \frac{1}{1 + e^{-x}}$$

Properties:
- Output range: $(0, 1)$ — bounded, preventing explosion
- Smooth and differentiable everywhere
- Derivative: $\sigma'(x) = \sigma(x)(1 - \sigma(x))$

**Limitation:** For very large or very small inputs, the gradient approaches zero (the "vanishing gradient problem"). This makes training deep networks with sigmoid activations difficult.

### ReLU

The Rectified Linear Unit is the most common modern activation:

$$\text{ReLU}(x) = \max(0, x)$$

Properties:
- Output range: $[0, \infty)$
- Computationally cheap
- Does not saturate for positive inputs (no vanishing gradient for $x > 0$)
- Not differentiable at $x = 0$ (but this is handled in practice)

**Limitation:** "Dead neurons" — if a neuron's input is always negative, its gradient is always zero, and it stops learning entirely.
