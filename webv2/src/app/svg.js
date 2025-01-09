import { NextResponse } from "next/server";
import React from "react";
import ReactDOMServer from "react-dom/server";
import MySvg from "@/components/MySvg";

export async function GET(request) {
  // Grab the URL from the request
  const { searchParams } = new URL(request.url);

  // Extract query parameters
  const backgroundColor = searchParams.get("backgroundColor") || "black";
  const title = searchParams.get("title") || "Hello World";
  const titleColor = searchParams.get("titleColor") || "white";
  const numFiles = searchParams.get("numFiles") || "1000";
  const totalLines = searchParams.get("totalLines") || "0";
  const textColor = searchParams.get("textColor") || "white";

  // Convert the component to static markup
  const svgString = ReactDOMServer.renderToStaticMarkup(
    <MySvg
      backgroundColor={backgroundColor}
      title={title}
      titleColor={titleColor}
      numFiles={numFiles}
      totalLines={totalLines}
      textColor={textColor}
    />
  );

  // Return it with correct Content-Type
  return new NextResponse(svgString, {
    status: 200,
    headers: {
      "Content-Type": "image/svg+xml",
    },
  });
}
