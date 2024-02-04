import axios from "axios";

export const endpoints = {
    
}

export const authAPI = (accessToken) => axios.create({
    baseURL: "",
    headers: {
        "Authorization" : `bearer ${accessToken}`
    }
})

export default axios.create({
    baseURL: ""
})