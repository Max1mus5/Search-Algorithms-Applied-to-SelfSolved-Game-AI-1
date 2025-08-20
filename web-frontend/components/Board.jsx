import React from "react";

/**
 * Board component - renders the 3x3 puzzle board
 * @param {Array<Array<number>>} board - 3x3 matrix representing the puzzle state
 */
export default function Board({ board = [[1,2,3],[4,5,6],[7,8,0]] }) {
  return (
    <div className="p-3 bg-card rounded-lg border">
      <div className="grid grid-cols-3 gap-2 w-[240px] sm:w-[300px]">
        {board.flat().map((value, idx) => {
          return (
            <div
              key={`${idx}-${value}`} // Use both index and value for better key stability
              className={`flex items-center justify-center h-16 sm:h-20 rounded-md text-lg font-semibold 
                ${value === 0 
                  ? "bg-transparent empty-tile" 
                  : "puzzle-tile"
                }`}
              aria-label={value === 0 ? "Empty tile" : `Tile ${value}`}
              role="img"
            >
              {value === 0 ? "" : value}
            </div>
          );
        })}
      </div>
    </div>
  );
}
