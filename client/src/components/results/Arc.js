import React from "react"

export default function Arc(props) {
    function polarToCartesian(centerX, centerY, radius, angleInDegrees) {
        const angleInRadians = (angleInDegrees-90) * Math.PI / 180.0
        return {
            x: centerX + (radius * Math.cos(angleInRadians)),
            y: centerY + (radius * Math.sin(angleInRadians))
        }
    }
    const getPercentSpanStyle = score => {
        let hue = 150 - 150*(score/100)
        return `hsl(${hue}, 100%, 50%)`
    }
    const startAngle = -90
    const endAngle = -90 + (180*props.score/100)
    const start = polarToCartesian(60, 60, 50, endAngle)
    const end = polarToCartesian(60, 60, 50, startAngle)
    const largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1"
    const d = [
        "M", start.x, start.y, 
        "A", 50, 50, 0, largeArcFlag, 0, end.x, end.y
    ].join(" ")
    return(
        <svg width="120" height="60">
            <path stroke={getPercentSpanStyle(props.score)} strokeWidth="15" d={d} fill="none" />
        </svg>
    )
}