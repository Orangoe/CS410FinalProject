import React,{useState, useEffect} from 'react'
import {useNavigate, useParams} from "react-router";
import {getMovieByID, getRecoBM25} from "../utils/api";
import MRNavBar from "./styledComponents/mrNavBar";
import Container from "react-bootstrap/Container";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import styled from 'styled-components';
import Card from "react-bootstrap/Card";
import Badge from "react-bootstrap/Badge";
import Button from 'react-bootstrap/Button';

const MRrecoResultContainer = styled(Container)`
  margin-top: 50px;
  margin-bottom: 50px;
`


const MRdetailCard = styled(Card)`
  padding: 15px;
  display: flex;
  justify-content: space-around;
  
`

const MRdetailCardTitle = styled(Card.Text)`
  margin-top: 15px;
  margin-bottom: 15px;
  font-size: xx-large;
`

const MRdetailCardButton = styled(Button)`
  max-width: 240px;
  margin-top: 80px;
  margin-bottom: 60px;
  margin-left: 50%;
  transform: translate(-50%, 0)

`

const MRrecoResultContainerBM25 = styled(Container)`
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




export default function MovieDetail() {
    const navigate = useNavigate()
    const {movieID} = useParams();
    console.log(movieID)

    const [movieData, setMovieData] = useState([]);
    const [BM25Data, setBM25Data] = useState([]);
    const [rawData, setRawData] = useState();
    const [rawReco, setRawReco] = useState();
    useState(() => {
        getMovieByID(movieID).then(res => {
            console.log(res.data)
            console.log(res.data[0]["movie_title"])
            setMovieData(res.data[0])
            setRawData(res.data)
        })
    })

    function getReco() {
        getRecoBM25(movieID).then(res => {
            console.log(res.data)
            setRawReco(res.data)
            setBM25Data(res.data)
        })
    }

    function toDetail(movie_id) {
        navigate(`/detail/${movie_id}`)
        window.location.reload()
    }

    return (
        <div>
            <MRNavBar/>
            {rawData && (<MRrecoResultContainer>
                <MRdetailCard>
                    <Container>
                        <Row>
                            <Col xs={4} md={3}>
                                <Card.Img src={movieData.movie_poster} />
                                <Badge bg="secondary">
                                    {movieData.movie_genres[0]}
                                </Badge>{' '}
                                <Badge bg="secondary">
                                    {movieData.movie_genres[1]}
                                </Badge>{' '}
                                <Badge bg="secondary">
                                    {movieData.movie_genres[2]}
                                </Badge>{' '}
                            </Col>
                            <Col xs={14} md={9}>
                                <MRdetailCardTitle>{movieData["movie_title"]}</MRdetailCardTitle>
                                <Card.Text>{movieData["movie_year"]}</Card.Text>
                                <Card.Text>Restricted Level: {movieData["movie_level"]} | Total Length: {movieData["movie_length"]} | IMBD rating: {movieData["movie_score"]}</Card.Text>
                                <hr/>
                                <Card.Text>{movieData.movie_plot}</Card.Text>
                            </Col>
                        </Row>
                    </Container>
                    <MRdetailCardButton variant="success" onClick={getReco}>Get Recommendation</MRdetailCardButton>
                </MRdetailCard>
            </MRrecoResultContainer>)}

            <MRrecoResultContainer>
                <h3>Recommendations By BM25 Okapi</h3>
                <hr/>
                <MRrecoResultContainerBM25>
                    {rawReco &&
                    (BM25Data.map(movieData => (
                        <MRResultCard key={movieData.movie_id} style={{ width: '12rem' }} onClick={() => toDetail(movieData.movie_id)}>
                            <Card.Img variant="left" src={movieData.movie_poster} />
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
                        </MRResultCard>)))}
                </MRrecoResultContainerBM25>
            </MRrecoResultContainer>

        </div>
    )
}