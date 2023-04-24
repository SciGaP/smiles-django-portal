import axios from "axios";

export const smilesDPService = {
  getSMILESDataProducts
};

function getSMILESDataProducts(params) {
  return axios
    .get(`http://127.0.0.1:8000/smiles_django/experimental-dps?${params}`, {})
    .then((response) => Promise.resolve(response))
    .catch((error) => Promise.reject(error.response));
}
