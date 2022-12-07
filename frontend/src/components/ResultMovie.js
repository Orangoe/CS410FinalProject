import React, {useEffect, useState} from 'react';
import MRNavBar from "./styledComponents/mrNavBar";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import {useNavigate, useParams} from "react-router";
import {getMovieByID, searchMovieTitle} from "../utils/api";
import Badge from 'react-bootstrap/Badge';
import styled from 'styled-components';

const MRResultContainer = styled(Container)`
  
  //max-width: 1000px;
  margin-top: 40px;
  margin-bottom: 60px;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-content: center;
`

const MRResultCard = styled(Card)`
  margin: 15px;
  padding: 5px;
`




export default function ResultMovie() {
    const navigate = useNavigate()
    const {movieName} = useParams();
    const [rawData, setRawData] = useState();
    const [movieDataList, setMovieDataList] = useState([]);
    console.log(movieName)

    useState(() => {
        searchMovieTitle(movieName).then(res => {
            console.log(res.data)
            setRawData(res)
            setMovieDataList(res.data)
        })
    })

    function toDetail(movie_id) {
        navigate(`/detail/${movie_id}`)
        window.location.reload()
    }


    return (
        <div>
            <MRNavBar
                movieName={movieName}
            />
            <MRResultContainer>
                {rawData &&
                (movieDataList.map(movieData => (
                    <MRResultCard key={movieData.movie_id} style={{ width: '18rem' }} onClick={() => toDetail(movieData.movie_id)}>
                        <Card.Img variant="top" src={movieData.movie_poster} />
                        <Card.Body>
                            <Card.Title>{movieData.movie_title}</Card.Title>
                            <Card.Text>{movieData.movie_year}</Card.Text>
                            <Badge bg="secondary">
                                {movieData.movie_genres[0]}
                            </Badge>{' '}
                            <Badge bg="secondary">
                                {movieData.movie_genres[1]}
                            </Badge>{' '}
                            <Badge bg="secondary">
                                {movieData.movie_genres[2]}
                            </Badge>{' '}
                            {/*<Button variant="primary">Go somewhere</Button>*/}
                        </Card.Body>
                    </MRResultCard>)))
                }
            </MRResultContainer>
        </div>
    )
}