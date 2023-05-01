import axios from "axios";

export const smilesDPService = {
    getSMILESDataProducts,
    getDisplayableColumns,
    deleteSMILESDataProduct
};

function getSMILESDataProducts(params) {
    return axios
        .get(`http://127.0.0.1:8000/smiles_django/exp-dps?${params}`, {})
        .then((response) => Promise.resolve(response))
        .catch((error) => Promise.reject(error.response));
}

function deleteSMILESDataProduct(type, dp_id) {
    return axios.delete(`http://127.0.0.1:8000/smiles_django/${type}-dp/${dp_id}`)
}

function getDisplayableColumns(type) {
    //TODO - These columns should be based on the user preferences
    if (type === "exp") {
        return [
            {key: "name", label: "Name", sortable: true},
            {key: "smiles", label: "Smiles String", sortable: true},
            {key: "emis_max", label: "Emission Max(nm)"},
            {key: "mol_id", label: "Molecular Id"},
            {key: 'actions', label: ''}
        ];
    } else if (type === "comp") {
        return [
            {key: "name", label: "Name", sortable: true},
            {key: 'actions', label: ''}
        ];
    } else if (type === "lit") {
        return [
            {key: "name", label: "Name", sortable: true},
            {key: "emis_max", label: "Emission Max(nm)"},
            {key: "mol_id", label: "Molecular Id"},
            {key: 'actions', label: ''}
        ];
    } else {
        return [
            {key: "data_product_id", label: "ID", sortable: true},
            {key: "name", label: "Name", sortable: true},
            {key: 'actions', label: ''}
        ];
    }
}
