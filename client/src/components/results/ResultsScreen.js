import React, { useEffect } from "react"
import { useNavigate } from "react-router-dom"
import Header from "../common/Header"
import Arc from "./Arc"

export default function ResultsScreen(props) {
    const containerStyle = {
        borderRadius: '5px'
    }
    const scamTypeStyle = {
        color: '#bbb',
        fontWeight: 'lighter'
    }
    const scamDescStyle = {
        color: '#bbb'
    }
    const getPercentSpanStyle = score => {
        let hue = 150 - 150*(score/100)
        return {
            color: `hsl(${hue}, 100%, 50%)`
        }
    }
    const navigate = useNavigate()
    useEffect(() => {
        if(!props.results.score) {
            console.log('back')
            navigate('/')
        }
    })
    const getFraudString = (score) => {
        if(score == 0) return "legitimate"
        if(score < 10) return "most likely safe"
        if(score < 20) return "probably safe"
        if(score < 30) return "moderately safe"
        if(score < 40) return "somewhat safe"
        if(score < 50) return "questionable"
        if(score < 60) return "somewhat suspicious"
        if(score < 70) return "moderately suspicious"
        if(score < 80) return "suspicious"
        if(score < 90) return "very suspicious"
        if(score < 100) return "most likely a scam"
        return "definitely a scam"
    }
    return (
        <>
            <Header/>
            <div style={containerStyle} className="container mt-5 pt-3 pb-5 px-3 bg-dark text-white">
                <div className="text-center">
                    <h1 className="font-weight-light text-underline mb-4">Scan Results</h1>
                </div>
                <div className="d-flex flex-row mb-3">
                    <Arc score={props.results.score}/>
                    <div className="ml-3 d-flex flex-column">
                        <h2>Fraud risk: <span style={getPercentSpanStyle(props.results.score)}>{props.results.score}%</span></h2>
                        <h6 style={getPercentSpanStyle(props.results.score)}>This account is {getFraudString(props.results.score)}</h6>   
                    </div>
                </div>
                <h2 className="mt-5">Scam Type: <span style={scamTypeStyle}>{props.results.scamType}</span></h2>
                <p style={scamDescStyle} className='para__desc mt-4'>
                    {props.results.description}
                </p>
            </div>
        </>
    )
}