import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { useState } from 'react'

import DefaultContainer from './components/DefaultContainer'
import HomeScreen from './components/home/HomeScreen'
import ResultsScreen from './components/results/ResultsScreen'

function App() {
  const [results, setResults] = useState({})
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<DefaultContainer/>}>
          <Route index element={<HomeScreen setResults={setResults} />}/>
          <Route path='results' element={<ResultsScreen results={results} />}/>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
