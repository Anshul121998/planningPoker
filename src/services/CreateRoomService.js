import Axios from 'axios'

let authCode = {
  headers: {
    'Authorization': '1873_d1873ty1873t82y736uhdbuvgtvfh83g7f3bfyv'
  }
}

export default {
  createRoom: (data) => {
    return new Promise((resolve, reject) => {
      Axios.post(`/api/planningPoker/createRoom/zzz`, data, authCode).then(
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
      Axios.post(`/api/planningPoker/togglePolling/zzz`, data, authCode).then(
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
      Axios.post(`/api/planningPoker/checkParticipants/zzz`, data, authCode).then(
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
