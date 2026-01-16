# OCR Neural Network - Data Flow & Architecture Guide

This guide explains how data flows through the OCR application, from drawing on the canvas to training and testing the neural network.

## Table of Contents
- [Overview](#overview)
- [Data Structure](#data-structure)
- [Front-End: Canvas to Array](#front-end-canvas-to-array)
- [Training Flow](#training-flow)
- [Testing/Prediction Flow](#testingprediction-flow)
- [Neural Network Architecture](#neural-network-architecture)
- [API Communication](#api-communication)

---

## Overview

The application allows users to draw digits (0-9) on a canvas, which are converted into numerical data and sent to a neural network for training or prediction.

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   User Draws    │   -->   │  Convert to      │   -->   │  Neural Network │
│   on Canvas     │         │  Array (784)     │         │  Processes      │
│   (280x280px)   │         │  28x28 grid      │         │  & Learns       │
└─────────────────┘         └──────────────────┘         └─────────────────┘
```

---

## Data Structure

### Canvas Representation
The drawing canvas is **280x280 pixels**, divided into a **28x28 grid** of squares:
- Each square is **10x10 pixels**
- This creates **784 total squares** (28 × 28 = 784)
- Each square represents **one input** to the neural network

### The Data Array
```javascript
// Initial state: all squares are empty (0)
data = [0, 0, 0, 0, ..., 0]  // 784 elements

// After drawing, filled squares become 1
data = [0, 1, 1, 0, ..., 1]  // 784 elements (0s and 1s)
```

### Visual Representation
```
Canvas (280x280px)                    Data Array (784 elements)
┌─────────────────┐                   
│ □ □ □ □ □ □ ... │                   [0, 0, 0, 0, 0, 0, ...,
│ □ ■ ■ ■ □ □ ... │  ──────────>      0, 1, 1, 1, 0, 0, ...,
│ □ ■ □ ■ □ □ ... │    Convert        0, 1, 0, 1, 0, 0, ...,
│ □ ■ ■ ■ □ □ ... │                   0, 1, 1, 1, 0, 0, ...,
│ □ □ □ □ □ □ ... │                   ... (784 total)]
│      ...        │
└─────────────────┘
  28x28 grid
```

---

## Front-End: Canvas to Array

### Step-by-Step Process

**1. User Draws on Canvas**
```javascript
// When user clicks and drags on the canvas
handleMouseDown(event) -> fillSquare(x, y)
```

**2. Calculate Grid Position**
```javascript
// Convert mouse coordinates to grid position
const xPixel = Math.floor(x / PIXEL_WIDTH)  // Which column (0-27)
const yPixel = Math.floor(y / PIXEL_WIDTH)  // Which row (0-27)
```

**3. Calculate Array Index**
```javascript
// Convert 2D grid position to 1D array index
const index = ((xPixel - 1) * TRANSLATED_WIDTH + yPixel) - 1

// Example: Square at position (5, 3)
// index = ((5-1) * 28 + 3) - 1 = 114
// So data[114] = 1
```

**4. Update Array and Canvas**
```javascript
data[index] = 1  // Mark this square as filled
// Visual feedback: paint the square white on the canvas
```

### Index Mapping Example
```
Grid Position (x, y)  →  Array Index  →  Data Value
┌──────────────────────────────────────────────────┐
│ (0, 0)           →    0           →    0 or 1   │
│ (0, 1)           →    1           →    0 or 1   │
│ (0, 2)           →    2           →    0 or 1   │
│ ...                                              │
│ (1, 0)           →    28          →    0 or 1   │
│ (1, 1)           →    29          →    0 or 1   │
│ ...                                              │
│ (27, 27)         →    783         →    0 or 1   │
└──────────────────────────────────────────────────┘
```

---

## Training Flow

### Complete Training Process

```
┌──────────────────────────────────────────────────────────────┐
│                        TRAINING FLOW                          │
└──────────────────────────────────────────────────────────────┘

1. USER INTERACTION
   ┌────────────┐
   │ Draw digit │  User draws a "5" on canvas
   │ Enter "5"  │  User enters the label
   └─────┬──────┘
         │
         v
2. BATCH COLLECTION (Front-End)
   ┌─────────────────────────────────────┐
   │ Add to trainArray:                  │
   │ {                                   │
   │   y0: [0,1,1,0,1,...],  // 784 nums │
   │   label: 5               // 0-9     │
   │ }                                   │
   └─────────────┬───────────────────────┘
                 │ Repeat 3 times (BATCH_SIZE)
                 v
3. SEND TO SERVER
   ┌─────────────────────────────────────┐
   │ POST /api/train                     │
   │ {                                   │
   │   trainArray: [                     │
   │     { y0: [...], label: 5 },        │
   │     { y0: [...], label: 7 },        │
   │     { y0: [...], label: 2 }         │
   │   ]                                 │
   │ }                                   │
   └─────────────┬───────────────────────┘
                 │
                 v
4. NEURAL NETWORK TRAINING (Back-End)
   ┌─────────────────────────────────────┐
   │ For each sample:                    │
   │                                     │
   │ a) Forward Propagation              │
   │    Input (784) → Hidden (28) → Out (10) │
   │                                     │
   │ b) Calculate Error                  │
   │    Expected: [0,0,0,0,0,1,0,0,0,0]  │
   │    Actual:   [0.1,0.2,...,0.8,...]  │
   │    Error = Expected - Actual        │
   │                                     │
   │ c) Backpropagation                  │
   │    Adjust weights to reduce error   │
   │                                     │
   │ d) Update All Weights               │
   │    theta1, theta2, biases           │
   └─────────────┬───────────────────────┘
                 │
                 v
5. SAVE WEIGHTS
   ┌─────────────────────────────────────┐
   │ Save to: ocr_neural_network.json    │
   │ - theta1 (784→28 weights)           │
   │ - theta2 (28→10 weights)            │
   │ - input_layer_bias                  │
   │ - hidden_layer_bias                 │
   └─────────────┬───────────────────────┘
                 │
                 v
6. RESPONSE TO CLIENT
   ┌─────────────────────────────────────┐
   │ { success: true, message: "..." }   │
   │ Display: ✓ Trained with 3 samples!  │
   └─────────────────────────────────────┘
```

### Training Data Structure Example
```javascript
// What gets sent to the server
{
  "trainArray": [
    {
      "y0": [0, 0, 0, 1, 1, 1, 0, ...],  // 784 values (0 or 1)
      "label": 5                          // The digit you drew
    },
    {
      "y0": [1, 1, 0, 0, 0, 1, 1, ...],  // 784 values
      "label": 7
    },
    {
      "y0": [0, 1, 1, 1, 0, 0, 1, ...],  // 784 values
      "label": 2
    }
  ]
}
```

---

## Testing/Prediction Flow

### Complete Testing Process

```
┌──────────────────────────────────────────────────────────────┐
│                    TESTING/PREDICTION FLOW                    │
└──────────────────────────────────────────────────────────────┘

1. USER DRAWS
   ┌────────────┐
   │ Draw digit │  User draws a digit (no label needed)
   └─────┬──────┘
         │
         v
2. SEND TO SERVER
   ┌─────────────────────────────────────┐
   │ POST /api/predict                   │
   │ {                                   │
   │   image: [0,1,1,0,1,...]  // 784    │
   │ }                                   │
   └─────────────┬───────────────────────┘
                 │
                 v
3. NEURAL NETWORK PREDICTION (Back-End)
   ┌─────────────────────────────────────┐
   │ Load existing weights from file     │
   │                                     │
   │ Forward Propagation:                │
   │                                     │
   │ Input Layer (784 neurons)           │
   │    ↓ [weights: theta1]              │
   │ Hidden Layer (28 neurons)           │
   │    ↓ [activation: sigmoid]          │
   │ Output Layer (10 neurons)           │
   │    ↓ [weights: theta2]              │
   │ Final Output:                       │
   │ [0.05, 0.02, 0.91, 0.04, ...]       │
   │   ↑              ↑                  │
   │   0              2 ← Highest value! │
   │                                     │
   │ Prediction: 2                       │
   └─────────────┬───────────────────────┘
                 │
                 v
4. RESPONSE TO CLIENT
   ┌─────────────────────────────────────┐
   │ {                                   │
   │   type: "test",                     │
   │   result: 2                         │
   │ }                                   │
   │ Display: 🎯 Network predicts: '2'   │
   └─────────────────────────────────────┘
```

### Prediction Data Structure Example
```javascript
// What gets sent to the server
{
  "image": [0, 0, 0, 1, 1, 1, 0, ...]  // 784 values (0 or 1)
}

// What comes back
{
  "type": "test",
  "result": 7  // The predicted digit
}
```

---

## Neural Network Architecture

### Network Structure

```
┌────────────────────────────────────────────────────────────────┐
│                    3-LAYER NEURAL NETWORK                      │
└────────────────────────────────────────────────────────────────┘

INPUT LAYER (784 neurons)
    Each neuron represents one square from the 28x28 grid
    Values: 0 (empty) or 1 (filled)
    
    neuron_0  ─┐
    neuron_1  ─┤
    neuron_2  ─┤
       ...     │
    neuron_783─┘
                │ theta1 weights (784 × 28 = 21,952 connections)
                │ + input_layer_bias
                v
HIDDEN LAYER (28 neurons)
    Learns patterns and features from the input
    Uses sigmoid activation function
    
    neuron_0  ─┐
    neuron_1  ─┤
    neuron_2  ─┤
       ...     │
    neuron_27 ─┘
                │ theta2 weights (28 × 10 = 280 connections)
                │ + hidden_layer_bias
                v
OUTPUT LAYER (10 neurons)
    Each neuron represents a digit (0-9)
    Highest value = predicted digit
    
    neuron_0 = 0.05  ← Probability it's "0"
    neuron_1 = 0.03  ← Probability it's "1"
    neuron_2 = 0.91  ← Probability it's "2" ★ WINNER!
    neuron_3 = 0.04  ← Probability it's "3"
       ...
    neuron_9 = 0.02  ← Probability it's "9"
```

### How Learning Works

**Forward Propagation (Making a Prediction)**
```
Input → [Multiply by weights] → Apply sigmoid → Hidden Layer
Hidden → [Multiply by weights] → Apply sigmoid → Output
```

**Backpropagation (Learning from Mistakes)**
```
1. Calculate Error
   Expected: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]  ← Should be "2"
   Actual:   [0.1, 0.2, 0.5, 0.1, ...]       ← Predicted "2" with 0.5
   Error = Expected - Actual = [−0.1, −0.2, 0.5, −0.1, ...]

2. Adjust Weights
   weights_new = weights_old + (LEARNING_RATE × error × input)
   - If error is positive: increase weight
   - If error is negative: decrease weight
   - LEARNING_RATE = 0.1 (how fast we learn)

3. Propagate Error Backwards
   - Calculate how much each hidden neuron contributed to error
   - Adjust theta1 weights accordingly
   - Update biases
```

### Activation Function (Sigmoid)

```
sigmoid(x) = 1 / (1 + e^(-x))

Graph:
  1.0 ─────────────────────
      |           .──────
      |        .─'
  0.5 |      ─'
      |   .─'
      | ─'
  0.0 ─────────────────────
     -6    -3    0    3    6

Purpose: Converts any input to a value between 0 and 1
```

---

## API Communication

### Endpoints

#### POST `/train`
Train the neural network with provided training data.

**Training Request:**
```json
{
  "trainArray": [
    {
      "y0": [0, 1, 1, 0, ...],  // 784 numbers
      "label": 5                 // 0-9
    }
  ]
}
```

**Training Response:**
```json
{
  "success": true,
  "message": "Training completed successfully"
}
```

#### POST `/predict`
Make a prediction using the trained neural network.

**Prediction Request:**
```json
{
  "image": [0, 1, 1, 0, ...]  // 784 numbers
}
```

**Prediction Response:**
```json
{
  "type": "test",
  "result": 7  // Predicted digit
}
```

#### POST `/optimize`
Finds the optimal number of hidden nodes for the neural network.

**Optimization Request:**
```json
{
  "trainingData": [
    {"y0": [0, 1, 1, ...], "label": 5},
    {"y0": [1, 0, 1, ...], "label": 7},
    ...
  ],
  "testData": [
    {"y0": [0, 1, 0, ...], "label": 2},
    ...
  ],
  "minNodes": 5,       // Optional, default: 5
  "maxNodes": 50,      // Optional, default: 50
  "step": 5            // Optional, default: 5
}
```

**Optimization Response:**
```json
{
  "results": [
    {"hiddenNodes": 20, "accuracy": 0.95},
    {"hiddenNodes": 25, "accuracy": 0.94},
    {"hiddenNodes": 15, "accuracy": 0.93}
  ],
  "optimal": {"hiddenNodes": 20, "accuracy": 0.95},
  "message": "Optimization completed. Tested 9 configurations."
}
```

**How it works:**
1. Tests multiple network configurations (5, 10, 15, 20... hidden nodes)
2. Trains each configuration with your training data
3. Tests each configuration against your test data (100 runs per config)
4. Returns results sorted by accuracy (best first)
5. Recommends the optimal configuration

This helps you find the best network architecture for your specific dataset!

### Data Validation

The server validates all incoming data:
- ✓ Array must have exactly **784 elements**
- ✓ All values must be **numeric** (0 or 1)
- ✓ Labels must be **integers 0-9**
- ✓ No NaN, Infinity, or undefined values

---

## Key Concepts Explained

### Why 784 Elements?
- Canvas: 280px × 280px
- Grid: 28 × 28 squares
- Result: **28 × 28 = 784 data points**

### Why Binary (0 or 1)?
- **0** = Square is empty (black)
- **1** = Square is filled (white/drawn)
- Simple binary input is easier for neural network to learn

### Why 28 Hidden Neurons?
- Too few: Network can't learn complex patterns
- Too many: Network might memorize instead of generalize
- **28** is a good balance for this task (found through testing)
- **Use the `/optimize` endpoint** to find the optimal number for your specific data!

### Why Batch Size of 3?
- Training one sample at a time is less stable
- Training many samples at once is slower
- **Batch of 3** provides quick feedback while maintaining stability

### What Gets Saved?
```
ocr_neural_network.json
├── theta1: 21,952 weights (784 → 28)
├── theta2: 280 weights (28 → 10)
├── input_layer_bias: 28 values
└── hidden_layer_bias: 10 values
```
These weights represent everything the network has learned!

---

## Example: Drawing a "2"

```
Step 1: User draws on canvas
┌─────────────┐
│ □□□□□□□□□□ │
│ □■■■■■■□□□ │   Drawing
│ □□□□□□■□□□ │     ↓
│ □□□■■■□□□□ │   Generates data array
│ □■■■□□□□□□ │
│ □■■■■■■□□□ │
│ □□□□□□□□□□ │
└─────────────┘

Step 2: Convert to array
data = [0,0,0,0,0,0,0,0,0,0,
        0,1,1,1,1,1,1,0,0,0,
        0,0,0,0,0,0,1,0,0,0,
        0,0,0,1,1,1,0,0,0,0,
        0,1,1,1,0,0,0,0,0,0,
        0,1,1,1,1,1,1,0,0,0,
        ... ] // 784 total

Step 3: Send to server with label
{ y0: data, label: 2 }

Step 4: Network learns
"When I see this pattern → output '2' with high confidence"
```

---

## Troubleshooting

### Common Issues

**Q: Why do predictions start inaccurate?**
- A: Network needs training! Train 3-5 examples of **each digit** (0-9)

**Q: Why does it sometimes predict wrong?**
- A: More training data needed, or drawings are too different from training samples

**Q: What if I draw too small/large?**
- A: Try to use most of the canvas for best results

**Q: Do I need to clear data between sessions?**
- A: No! Training data is saved to `ocr_neural_network.json` and persists

---

## Summary

1. **Draw** on 280x280 canvas → **784 binary values** (28×28 grid)
2. **Training**: Send `[{y0: array, label: digit}]` → Network adjusts weights
3. **Testing**: Send `{image: array}` → Network returns predicted digit
4. **Learning**: Backpropagation adjusts 22,232 weights to minimize errors
5. **Persistence**: All learned weights saved to JSON file

The more you train with varied examples, the smarter the network becomes! 🧠✨
