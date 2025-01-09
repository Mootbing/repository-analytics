"use client";

import logo from './logo.svg';
import './App.css';
import SVGComponent from './SVGComponent';

function beauitfyNumberString(num) {
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

  const backgroundColor = urlParams.get('backgroundColor') || 'black';
  
  const title = urlParams.get('title') || 'Hello World';
  const titleColor = urlParams.get('titleColor') || 'white';

  const numFiles = beauitfyNumberString(urlParams.get('numFiles') || "1000");
  const totalLines = beauitfyNumberString(urlParams.get('totalLines') || "0");

  const textColor = urlParams.get('textColor') || 'white';

  return <SVGComponent 
    backgroundColor={backgroundColor}
    title={title}
    titleColor={titleColor}
    numFiles={numFiles}
    totalLines={totalLines}
    textColor={textColor}
  />;
}

export default App;
