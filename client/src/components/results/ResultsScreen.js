import React from "react"
import Header from "../common/Header"

export default function ResultsScreen(props) {
    const getFraudString = (score) => {
        if(score < 25) {
            return "This account has a very low fraud risk"
        } 
        if(score < 50) {
            return "This account has a fairly low fraud risk"
        }
        if(score < 75) {
            return "This account has a moderate fraud risk"
        } 
        return "This account has a high fraud risk"
    }
    return (
        <>
            <Header/>
            <div className="container mt-5 pt-3 pb-5 bg-dark text-white">
                <div className="text-center">
                    <h1 className="font-weight-light text-underline mb-4">Scan Results</h1>
                </div>
                <h2>Fraud risk: {props.results.score}%</h2>
                <h6>{getFraudString(props.results.score)}</h6>
                <h2 className="mt-5">Scam Type: {props.results.scamType}</h2>
            </div>
        </>
    )
}