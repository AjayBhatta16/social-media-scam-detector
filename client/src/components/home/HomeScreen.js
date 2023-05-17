import React, { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import Header from '../common/Header'

export default function HomeScreen(props) {
    const headStyle = {
        color: '#0fdce3',
    }
    const btnStyle = {
        color: '#222',
        backgroundColor: '#0fdce3',
        borderRadius: '20%/50%'
    }
    const [errTxt, setErrTxt] = useState('')
    const urlRef = useRef()
    const navigate = useNavigate()
    const handleClick = () => {
        if(!urlRef.current.value || urlRef.current.value.length == 0) {
            setErrTxt("Please enter a social media profile URL")
            return 
        }
        fetch('/scan', {
            method: "POST",
            headers: {'Content-Type': 'application/json'}, 
            body: JSON.stringify({url: urlRef.current.value})
        }).then(res => {
            return res.json()
        }).then(res => {
            console.log(res)
            if(res.status=="400") {
                setErrTxt(res.message)
            } else {
                props.setResults({
                    platform: res.platform,
                    username: res.username,
                    score: 75,
                    scamType: 'Account Recovery',
                    description: 'Tech support scams involve scammers posing as tech support professionals who claim to fix technical problems with a victim\'s computer or software. The scammers trick the victim into paying for the fake services or giving remote access to their device.'
                })
                navigate('results')
            }
        })
    }
    return (
        <>
            <Header/>
            <div className='container mt-5 pt-3 text-center'>
                <h1 className='mt-5' style={{...headStyle}}>Social Media Scam Detector</h1>
                <h6 className='mt-3 mb-3' style={{...headStyle, fontWeight: '100'}}>
                    Enter the URL of a social media profile to scan it for fraud
                </h6>
                <input ref={urlRef} className='mt-5 mb-3 w-75 p-2' placeholder='Profile URL' type="text" />
                <br/><small className='text-danger'>{errTxt}</small><br/>
                <button onClick={handleClick} className='btn px-3 py-2 mt-2 scan__button' style={btnStyle}>Scan Profile</button>
            </div>
        </>
    )
}