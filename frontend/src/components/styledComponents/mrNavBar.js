import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import styled from 'styled-components';
import {useLocation, useNavigate} from "react-router";

const MRNavBarStyled = styled(Navbar)`
  background-color: #002855;
`

const MRNavBarContainerStyled = styled(Container)`
  margin-left: 10vw;
`

const MRNavBarBrandStyled = styled(Navbar.Brand)`
  color: #FFFF;
`


const MRNavBarToggleStyled = styled(Navbar.Toggle)`

`

const MRNavBarCollapseStyled = styled(Navbar.Collapse)`
  width: 70vw;
  display: block;
`


const MRNavBarFormStyled = styled(Form)`
  margin-left: 35vw;
  //margin-right: 10vw;
  padding-right: 0;
  .me-2{
    min-width: 400px;
  }
`


export default function MRNavBar(props) {
    const navigate = useNavigate()
    const location = useLocation()
    let [movieName, setMovieName] = useState()

    React.useEffect(() => {
        if (props.movieName === undefined) {
            setMovieName("")
        } else {
            setMovieName(props.movieName)
        }
    }, [location]);

    function search(e) {
        e.preventDefault();
        navigate(`/search/${movieName}`)
        window.location.reload()
    }

    function onInput({target: {value}}) {
        setMovieName(value)
    }

    // prevent default query parsed to url when enter pressed
    function handleKeyPress(target) {
        if (target.charCode === 13) {
            target.preventDefault();
            navigate(`/search/${movieName}`)
            window.location.reload()
        }
    }

    return (
        <MRNavBarStyled expand="lg">
            <MRNavBarContainerStyled fluid>
                <MRNavBarBrandStyled href="/">Movie Recommender</MRNavBarBrandStyled>
                <MRNavBarToggleStyled aria-controls="navbarScroll" />
                <MRNavBarCollapseStyled id="navbarScroll">
                    <MRNavBarFormStyled className="d-flex">
                        <Form.Control
                            type="search"
                            placeholder="Search"
                            className="me-2"
                            aria-label="Search"
                            value={movieName}
                            onChange={onInput}
                            onKeyPress={handleKeyPress}
                        />
                        <Button variant="outline-success" onClick={search}>Search</Button>
                    </MRNavBarFormStyled>
                </MRNavBarCollapseStyled>
            </MRNavBarContainerStyled>
        </MRNavBarStyled>
    );
}