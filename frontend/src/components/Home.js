import React, {Fragment, useEffect, useState} from 'react';
import MRNavBar from "./styledComponents/mrNavBar";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import Badge from "react-bootstrap/Badge";
import styled from "styled-components";
import Button from "react-bootstrap/Button";
import Form from 'react-bootstrap/Form';
import {getMovieByID, getRecoVecPlot} from "../utils/api";
import Spinner from "react-bootstrap/Spinner";
import {useNavigate} from "react-router";

const MRHomwContainer = styled(Container)`
  margin-top: 50px;
  margin-bottom: 50px;
`

const MRHomeCard = styled(Card)`
  padding: 15px;
  display: flex;
  justify-content: space-around;
  
`

const MRHomeCardButton = styled(Button)`
  max-width: 240px;
  margin-top: 80px;
  margin-bottom: 60px;
  //margin-left: 50%;
  //transform: translate(-50%, 0)

`
const MRForm = styled(Form)`
  
`

const MRdetailCardTitle = styled(Card.Text)`
  margin-top: 15px;
  margin-bottom: 15px;
  font-size: xx-large;
`

const MRFormControl = styled(Form.Control)`
  height: 420px;
  width: 40vw;
`

const MRrecoResultContainerBM25 = styled(Container)`
  margin-bottom: 60px;
  width: 80vw;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-content: center;
`

const MRrecoResultContainer = styled(Container)`
  margin-top: 50px;
  margin-bottom: 50px;
`

const MRResultCard = styled(Card)`
  margin: 2em;
  padding: 5px;
`


export default function Home() {
    const navigate = useNavigate()
    const [plot, setPlot] = useState("");
    const [VecData, setVecData] = useState([]);
    const [pressedReco, setPressedReco] = useState(false);
    const [loadingVec, setLoadingVec] = useState(false);

    useState(() => {
        setPlot(" ")
    })

    function onInput({target: {value}}) {
        setPlot(value)
    }


    function getReco() {
        setPressedReco(true)
        setLoadingVec(true)
        getRecoVecPlot(plot).then(res => {
            // console.log(res.data)
            setVecData(res.data)
            setLoadingVec(false)
        })
    }

    function toDetail(movie_id) {
        navigate(`/detail/${movie_id}`)
        window.location.reload()
    }

    return (
        <div>
            <MRNavBar/>
            <MRHomwContainer>
                <MRHomeCard>
                    <MRForm>
                        <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                            <MRdetailCardTitle>Enter a plot of movie to search for similar movies in our Database</MRdetailCardTitle>
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
                            <MRFormControl
                                as="textarea"
                                rows={5}
                                value={plot}
                                onChange={onInput}
                                placeholder="Enter plot" />
                        </Form.Group>
                        <MRHomeCardButton variant="success" onClick={getReco}>Get Recommendation</MRHomeCardButton>
                    </MRForm>
                </MRHomeCard>
            </MRHomwContainer>

            {pressedReco &&
            (<MRrecoResultContainer>
                <h3>Recommendations By Word2Vec</h3>
                <hr/>
                {loadingVec ?
                    (<Spinner animation="border" />) :
                    (<MRrecoResultContainerBM25>

                        {VecData.map(movieData => (
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
                            </MRResultCard>))}
                    </MRrecoResultContainerBM25>)}
            </MRrecoResultContainer>)}
        </div>
    )
}