
import { useState } from 'react';

export default function SVGComponent({backgroundColor,
    title,
    titleColor,
    numFiles,
    totalLines,
    textColor, ...props}) {
    return (
      <svg width={467} height={195}>
        <rect width={467} height={195} fill={backgroundColor} />
  
        <title>{title}</title>
        <desc></desc>
  
        <g>
          <text x={20} y={35} fontSize={20} fontWeight={300} fill={titleColor}>{title}</text>
          <text x={20} y={60} fontSize={14} fill={textColor} fontWeight={500}>Files: {numFiles}</text>
          <text x={55 + (numFiles.length * 7.5)} y={60} fontSize={14} fill={textColor} fontWeight={500}>Total Lines: {(totalLines)}</text>
        </g>
  
  
      </svg>
    );
}