/**
 * Generates synthetic digit patterns (0-9) that resemble handwritten digits
 * Each digit has a base template with randomization for variety
 */

const GRID_SIZE = 28

// Helper to set a pixel in the grid
const setPixel = (grid, x, y, value = 1) => {
  if (x >= 0 && x < GRID_SIZE && y >= 0 && y < GRID_SIZE) {
    grid[y * GRID_SIZE + x] = value
  }
}

// Draw a line between two points
const drawLine = (grid, x1, y1, x2, y2, thickness = 1) => {
  const dx = Math.abs(x2 - x1)
  const dy = Math.abs(y2 - y1)
  const sx = x1 < x2 ? 1 : -1
  const sy = y1 < y2 ? 1 : -1
  let err = dx - dy

  while (true) {
    // Draw with minimal thickness for better visibility (2x2 instead of 3x3)
    setPixel(grid, x1, y1, 1)
    if (thickness >= 1) {
      setPixel(grid, x1 + 1, y1, 1)
      setPixel(grid, x1, y1 + 1, 1)
      setPixel(grid, x1 + 1, y1 + 1, 1)
    }

    if (x1 === x2 && y1 === y2) break
    const e2 = 2 * err
    if (e2 > -dy) {
      err -= dy
      x1 += sx
    }
    if (e2 < dx) {
      err += dx
      y1 += sy
    }
  }
}

// Draw a circle (or arc)
const drawArc = (grid, cx, cy, radius, startAngle, endAngle, thickness = 1) => {
  // Balance between smoothness and performance - 30 steps for smooth arcs
  const steps = Math.min(30, Math.max(20, Math.ceil(radius * 3)))
  const angleStep = (endAngle - startAngle) / steps
  
  for (let i = 0; i <= steps; i++) {
    const angle = startAngle + i * angleStep
    const x = Math.round(cx + radius * Math.cos(angle))
    const y = Math.round(cy + radius * Math.sin(angle))
    
    // Draw with minimal thickness (2x2 instead of 3x3)
    setPixel(grid, x, y, 1)
    if (thickness >= 1) {
      setPixel(grid, x + 1, y, 1)
      setPixel(grid, x, y + 1, 1)
      setPixel(grid, x + 1, y + 1, 1)
    }
  }
}

// Fill gaps in lines to ensure smooth connectivity (optimized)
const fillGaps = (grid) => {
  const filled = [...grid]
  
  // Only check pixels adjacent to existing pixels (much faster)
  const toCheck = new Set()
  for (let i = 0; i < grid.length; i++) {
    if (grid[i] > 0) {
      // Add adjacent empty pixels to check list
      const y = Math.floor(i / GRID_SIZE)
      const x = i % GRID_SIZE
      for (let dy = -1; dy <= 1; dy++) {
        for (let dx = -1; dx <= 1; dx++) {
          const ny = y + dy
          const nx = x + dx
          if (ny >= 0 && ny < GRID_SIZE && nx >= 0 && nx < GRID_SIZE) {
            const idx = ny * GRID_SIZE + nx
            if (grid[idx] === 0) toCheck.add(idx)
          }
        }
      }
    }
  }
  
  // Check only the candidate pixels
  toCheck.forEach(idx => {
    const y = Math.floor(idx / GRID_SIZE)
    const x = idx % GRID_SIZE
    
    // Check 4-connectivity (just horizontal/vertical is enough)
    const left = x > 0 ? filled[idx - 1] : 0
    const right = x < GRID_SIZE - 1 ? filled[idx + 1] : 0
    const top = y > 0 ? filled[idx - GRID_SIZE] : 0
    const bottom = y < GRID_SIZE - 1 ? filled[idx + GRID_SIZE] : 0
    
    // Fill gap if pixels on opposite sides
    if ((left > 0 && right > 0) || (top > 0 && bottom > 0)) {
      filled[idx] = 1
    }
  })
  
  return filled
}

// Fast in-place gap filling - mutates array directly, no allocations
const fillGapsInPlace = (grid) => {
  // Check all interior pixels (not just every other one)
  for (let y = 1; y < GRID_SIZE - 1; y++) {
    for (let x = 1; x < GRID_SIZE - 1; x++) {
      const idx = y * GRID_SIZE + x
      
      // Skip if already filled
      if (grid[idx] !== 0) continue
      
      // Only check direct horizontal neighbors (fastest)
      const left = grid[idx - 1]
      const right = grid[idx + 1]
      
      // Fill horizontal gaps only
      if (left > 0 && right > 0) {
        grid[idx] = 1
      }
    }
  }
}

// Add random noise/variation to make digits look more natural
const addVariation = (grid, intensity = 0.1) => {
  // No post-processing - return grid as-is
  // The arc/line drawing with proper steps is sufficient
  return grid
}

// Digit pattern generators
const digitGenerators = {
  0: () => {
    const grid = Array(784).fill(0)
    
    // Simple oval - just draw vertical oval with proper proportions
    // Draw full circle for horizontal, stretch vertically with lines
    drawArc(grid, 14, 8, 7, 0, Math.PI * 2, 1)
    drawArc(grid, 14, 20, 7, 0, Math.PI * 2, 1)
    drawLine(grid, 7, 8, 7, 20, 1)
    drawLine(grid, 21, 8, 21, 20, 1)
    
    return grid
  },

  1: () => {
    const grid = Array(784).fill(0)
    const x = 14 + Math.round((Math.random() - 0.5) * 2)
    const topY = 4 + Math.round(Math.random() * 2)
    const bottomY = 24
    
    // Vertical line
    drawLine(grid, x, topY, x, bottomY, 1)
    // Top angle
    drawLine(grid, x - 2, topY + 2, x, topY, 1)
    
    return grid
  },

  2: () => {
    const grid = Array(784).fill(0)
    
    // Top curve
    drawArc(grid, 14, 8, 7, -Math.PI/2, Math.PI/2, 1)
    // Diagonal
    drawLine(grid, 21, 11, 7, 21, 1)
    // Bottom line
    drawLine(grid, 7, 24, 21, 24, 1)
    
    return grid
  },

  3: () => {
    const grid = Array(784).fill(0)
    
    // Top curve
    drawArc(grid, 11, 8, 7, -Math.PI/2, Math.PI/2, 1)
    // Bottom curve
    drawArc(grid, 11, 20, 7, -Math.PI/2, Math.PI/2, 1)
    // Middle line
    drawLine(grid, 11, 14, 18, 14, 1)
    
    return grid
  },

  4: () => {
    const grid = Array(784).fill(0)
    
    // Vertical line
    drawLine(grid, 17, 6, 17, 24, 1)
    // Diagonal
    drawLine(grid, 8, 17, 17, 6, 1)
    // Horizontal
    drawLine(grid, 8, 17, 21, 17, 1)
    
    return grid
  },

  5: () => {
    const grid = Array(784).fill(0)
    
    // Top horizontal
    drawLine(grid, 8, 6, 20, 6, 1)
    // Left vertical (top half)
    drawLine(grid, 8, 6, 8, 14, 1)
    // Middle horizontal
    drawLine(grid, 8, 14, 17, 14, 1)
    // Bottom curve
    drawArc(grid, 11, 20, 7, -Math.PI/2, Math.PI/2, 1)
    
    return grid
  },

  6: () => {
    const grid = Array(784).fill(0)
    
    // Small simple hook at top
    drawLine(grid, 14, 6, 10, 8, 1)
    // Vertical line down left side
    drawLine(grid, 10, 8, 10, 19, 1)
    // Bottom circle
    drawArc(grid, 14, 19, 6, 0, Math.PI * 2, 1)
    
    return grid
  },

  7: () => {
    const grid = Array(784).fill(0)
    
    // Top horizontal
    drawLine(grid, 7, 6, 21, 6, 1)
    // Diagonal down
    drawLine(grid, 21, 6, 11, 24, 1)
    
    return grid
  },

  8: () => {
    const grid = Array(784).fill(0)
    
    // Top circle (smaller)
    drawArc(grid, 14, 9, 5, 0, Math.PI * 2, 1)
    // Bottom circle (larger) - overlaps slightly for smooth connection
    drawArc(grid, 14, 19, 7, 0, Math.PI * 2, 1)
    
    return grid
  },

  9: () => {
    const grid = Array(784).fill(0)
    
    // Top circle
    drawArc(grid, 14, 9, 6, 0, Math.PI * 2, 1)
    // Tangent line from right side of circle down
    drawLine(grid, 20, 9, 16, 24, 1)
    
    return grid
  }
}

/**
 * Generate a random digit pattern
 * @param {number} digit - The digit to generate (0-9), or random if not specified
 * @returns {Object} - { y0: Array(784), label: number }
 */
export const generateDigitPattern = (digit = null) => {
  // Select random digit if not specified
  const selectedDigit = digit !== null ? digit : Math.floor(Math.random() * 10)
  
  // Generate base pattern
  let grid = digitGenerators[selectedDigit]()
  
  // Add variation for realism
  grid = addVariation(grid, 0.15)
  
  return {
    y0: grid,
    label: selectedDigit
  }
}

/**
 * Generate multiple random digit patterns
 * @param {number} count - Number of patterns to generate
 * @returns {Array} - Array of { y0, label } objects
 */
export const generateDigitBatch = (count = 10) => {
  const patterns = []
  for (let i = 0; i < count; i++) {
    patterns.push(generateDigitPattern())
  }
  return patterns
}
