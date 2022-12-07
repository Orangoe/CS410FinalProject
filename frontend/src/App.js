import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './components/Home'
import ResultMovie from "./components/ResultMovie";
import MovieDetail from "./components/MovieDetail";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route exact path='/' element={<Home/>} />
          {/*<Route path='/data_vis' element={<DataVisualization/>} />*/}
          {/*<Route path='/data_vis/:docType/' element={<ErrorPage/>} />*/}
          {/*<Route path='/data_vis/:docType/:query' element={<DataVisualization/>} />*/}
          <Route path='/search' element={<ResultMovie/>} />
          <Route path='/search/:movieName' element={<ResultMovie/>} />
          {/*<Route path='/search/:docType/:query' element={<Results/>} />*/}
          <Route path='/detail/:movieID' element={<MovieDetail/>} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
