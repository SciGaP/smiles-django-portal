// TODO const { utils } = AiravataAPI;
import axios from "axios";

export const smilesDPService = {
    getSMILESDataProduct,
    getSMILESDataProducts,
    deleteSMILESDataProduct
};

function getSMILESDataProduct(type, dp_id) {
    return axios
        .get(`http://127.0.0.1:8000/smiles_django/${type}-dp/${dp_id}`)
        .then((response) => Promise.resolve(response))
        .catch((error) => Promise.reject(error.response));
}

function getSMILESDataProducts(type, params) {
    return axios
        .get(`http://127.0.0.1:8000/smiles_django/${type}-dps?${params}`)
        .then((response) => Promise.resolve(response))
        .catch((error) => Promise.reject(error.response));
}

function deleteSMILESDataProduct(type, dp_id) {
    return axios.delete(`http://127.0.0.1:8000/smiles_django/${type}-dp/${dp_id}`)
}
