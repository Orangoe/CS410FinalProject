import axios from 'axios'

const MovieRecommemder = axios.create({
    timeout: 50000,
    // baseURL: 'http://localhost:8000'
    baseURL: 'http://66.42.113.98/api'
})

export function getMovieByID(movie_id) {
    return MovieRecommemder({
        method: 'GET',
        url: `/db_get_by_id/${movie_id}`
    })
}

export function searchMovieTitle(movie_title) {
    return MovieRecommemder({
        method: 'GET',
        url: `/db_get_by_title/${movie_title}`
    })
}

export function getRecoBM25(movie_id) {
    return MovieRecommemder({
        method: 'GET',
        url: `/bm25/${movie_id}`
    })
}