import Axios from 'axios'

let authCode = {
  headers: {
    'Authorization': '1873_d1873ty1873t82y736uhdbuvgtvfh83g7f3bfyv'
  }
}

export default {
  enterRoom: (data) => {
    return new Promise((resolve, reject) => {
      Axios.post(`/api/planningPoker/enterRoom/zzz`, data, authCode).then(
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
