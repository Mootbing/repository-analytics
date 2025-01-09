import logo from './logo.svg';
import './App.css';
import { useState } from 'react';

const beauitfyNumberString = (num) => {

  num = parseInt(num);

  //return k, m, b, t, etc
  if (num > 999999999) {
    return (num / 1000000000).toFixed(1) + "b";
  } else if (num > 999999) {
    return (num / 1000000).toFixed(1) + "m";
  } else if (num > 999) {
    return (num / 1000).toFixed(1) + "k";
  }
  return num;
}

function App() {

  const urlParams = new URLSearchParams(window.location.search);

  const [backgroundColor, setBackgroundColor] = useState(
    urlParams.get('backgroundColor') || 'black'
  );

  const title = urlParams.get('title') || 'Hello World';
  const titleColor = urlParams.get('titleColor') || 'white';

  const numFiles = beauitfyNumberString(urlParams.get('numFiles') || "1000");
  const totalLines = beauitfyNumberString(urlParams.get('totalLines') || "0");

  const textColor = urlParams.get('textColor') || 'white';

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

export default App;
