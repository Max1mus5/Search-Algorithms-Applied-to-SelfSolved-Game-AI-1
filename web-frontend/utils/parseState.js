/**
 * Parse initial state input from user
 * @param {string} text - Input text containing the puzzle state
 * @returns {Object} - {ok: boolean, state?: Array, error?: string}
 */
export function parseInitialState(text) {
  // accepts 3 lines or space-separated 9 numbers
  if (!text || !text.trim()) {
    return { ok: false, error: "Empty input" };
  }
  
  const parts = text.trim().split(/\s+/).map((t) => t.trim()).filter(Boolean);
  
  if (parts.length !== 9) {
    return { ok: false, error: "Input must contain exactly 9 numbers (0-8)" };
  }
  
  const nums = parts.map((p) => Number(p));
  
  if (nums.some((n) => Number.isNaN(n) || n < 0 || n > 8)) {
    return { ok: false, error: "Numbers must be integers between 0 and 8" };
  }
  
  const sorted = [...nums].sort((a,b) => a-b);
  for (let i = 0; i <= 8; i++) {
    if (sorted[i] !== i) {
      return { ok: false, error: "Numbers must contain all digits 0..8 exactly once" };
    }
  }
  
  // return matrix 3x3
  const matrix = [nums.slice(0,3), nums.slice(3,6), nums.slice(6,9)];
  return { ok: true, state: matrix };
}

/**
 * Check if a puzzle state is solvable
 * @param {Array<Array<number>>} matrix - 3x3 puzzle state
 * @returns {boolean} - true if solvable
 */
export function isSolvable(matrix) {
  const flat = matrix.flat();
  let inversions = 0;
  
  for (let i = 0; i < flat.length - 1; i++) {
    if (flat[i] === 0) continue;
    for (let j = i + 1; j < flat.length; j++) {
      if (flat[j] === 0) continue;
      if (flat[i] > flat[j]) inversions++;
    }
  }
  
  // For 3x3 puzzle, solvable if inversions are even
  return inversions % 2 === 0;
}

/**
 * Generate preset puzzle states
 */
export const PRESET_STATES = {
  solved: [[1,2,3],[4,5,6],[7,8,0]],
  easy: [[1,2,3],[4,5,6],[7,0,8]],
  medium: [[1,2,3],[4,0,6],[7,5,8]], 
  hard: [[7,2,4],[5,0,6],[8,3,1]],
  expert: [[8,6,7],[2,5,4],[3,0,1]]
};

/**
 * Convert matrix to string for display
 * @param {Array<Array<number>>} matrix - 3x3 puzzle state
 * @returns {string} - Formatted string representation
 */
export function matrixToString(matrix) {
  return matrix.map(row => row.join(' ')).join('\n');
}
