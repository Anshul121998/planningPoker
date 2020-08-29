import Axios from 'axios'

let $axios = Axios.create({
  baseURL: '',
  timeout: 5000,
  headers: { 'Content-Type': 'application/json' }
})
// Request Interceptor
$axios.interceptors.request.use(function (config) {
  config.headers['Authorization'] = '3n3jkn3en3he42j3nh2n2jg32bn32ug3j2njg23i2n3jh2bv3iyb2h'
  return config
})
// Response Interceptor to handle and log errors
$axios.interceptors.response.use(function (response) {
  return response
}, function (error) {
  // Handle Error
  console.log(error)
  return Promise.reject(error)
})
export default {
  createRoom: (data) => {
    return new Promise((resolve, reject) => {
      Axios.post('/planningPoker/createRoom', data).then(
        (response) => {
          resolve(response.data)
        },
        (err) => {
          reject(err)
        }
      )
    })
  },
  togglePolling: (data) => {
    return new Promise((resolve, reject) => {
      Axios.post('/planningPoker/togglePolling', data).then(
        (response) => {
          resolve(response.data)
        },
        (err) => {
          reject(err)
        }
      )
    })
  },
  getCurrUsers: (data) => {
    return new Promise((resolve, reject) => {
      Axios.post('/planningPoker/checkParticipants', data).then(
        (response) => {
          resolve(response.data)
        },
        (err) => {
          reject(err)
        }
      )
    })
  }
}
