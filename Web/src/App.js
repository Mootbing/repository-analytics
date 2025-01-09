import logo from './logo.svg';
import './App.css';
import { useState } from 'react';

function App() {

  const urlParams = new URLSearchParams(window.location.search);

  const [backgroundColor, setBackgroundColor] = useState(
    urlParams.get('backgroundColor') || 'black'
  );

  const title = urlParams.get('title') || 'Hello World';
  const titleColor = urlParams.get('titleColor') || 'white';

  const numFiles = urlParams.get('numFiles') || "0";
  const totalLines = urlParams.get('totalLines') || "0";

  const textColor = urlParams.get('textColor') || 'white';

  return (
    <svg width={467} height={195}>
      <rect width={467} height={195} fill={backgroundColor} />

      <title>{title}</title>
      <desc></desc>

      <g>
        <text x={20} y={35} fontSize={20} fontWeight={700} fill={titleColor}>{title}</text>
        {/* code horizontal group of [# of files, total # of lines] */}
        <g>
          <text x={20} y={60} fontSize={14} fill={textColor}>Files: {numFiles}</text>
          <text x={numFiles.length*7.5 + 70} y={60} fontSize={14} fill={textColor}>Total Lines: {totalLines}</text>
        </g>
      </g>
    </svg>
  );
}

export default App;
