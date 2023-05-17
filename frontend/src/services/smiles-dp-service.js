// TODO const { utils } = AiravataAPI;
import axios from "axios";

export const smilesDPService = {
    getSMILESDataProduct,
    getSMILESDataProducts,
    deleteSMILESDataProduct
};

function getSMILESDataProduct(type, dp_id) {
    return axios
        .get(`/smiles/${type}-dp/${dp_id}`)
        .then((response) => Promise.resolve(response))
        .catch((error) => Promise.reject(error.response));
}

function getSMILESDataProducts(type, params) {
    return axios
        .get(`/smiles/${type}-dps?${params}`)
        .then((response) => Promise.resolve(response))
        .catch((error) => Promise.reject(error.response));
}

function deleteSMILESDataProduct(type, dp_id) {
     return axios.delete(`/smiles/${type}-dp/${dp_id}`)
}
