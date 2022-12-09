import axios from 'axios'

const MovieRecommemder = axios.create({
    timeout: 50000,
    baseURL: 'http://localhost:8000/api'
    // baseURL: 'http://66.42.113.98/api'

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

export function getRecoVec(movie_id) {
    return MovieRecommemder({
        method: 'GET',
        url: `/vectordb/${movie_id}`
    })
}

export function getRecoVecPlot(plot) {
    return MovieRecommemder({
        method: 'POST',
        url: `/vectornew`,
        data: {
            movie_plot: plot,
        }
    })
}

export function getRecoPLSA(movie_id) {
    return MovieRecommemder({
        method: 'GET',
        url: `/plsa/${movie_id}`
    })
}