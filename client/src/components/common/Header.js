import React from 'react'
import { Link } from 'react-router-dom'

export default function Header() {
    return (
        <>
            <nav className='navbar navbar-expand-md bg-dark navbar-dark shadow-md px-1 mb-5'>
                <Link to='/'>
                    <a href='#' className='navbar-brand py-0 px-0 mx-0'>
                        <img src='logo.png' alt='logo' height={40}/>
                    </a>
                </Link>
            </nav>
        </>
    )
}