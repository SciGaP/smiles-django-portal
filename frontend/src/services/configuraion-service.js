export const configurationService = {
    getDisplayableColumns
};


function getDisplayableColumns(type) {
    if (type === "exp") {
        return JSON.parse(localStorage.getItem('exp-display-columns')) ||
            [
                {key: "name", label: "Name", sortable: true},
                {key: "smiles", label: "Smiles String", sortable: true},
                {key: "emis_max", label: "Emission Max(nm)"},
                {key: "mol_id", label: "Molecular Id"},
                {key: "mw", label: "MW"},
                {key: 'actions', label: ''}
            ];

    } else if (type === "comp") {
        return JSON.parse(localStorage.getItem('comp-display-columns')) ||
            [
                {key: "name", label: "Name", sortable: true},
                {key: 'actions', label: ''}
            ];
    } else if (type === "lit") {
        return JSON.parse(localStorage.getItem('lit-display-columns')) ||
            [
                {key: "name", label: "Name", sortable: true},
                {key: "emis_max", label: "Emission Max(nm)"},
                {key: "mol_id", label: "Molecular Id"},
                {key: 'actions', label: ''}
            ];
    } else {
        return JSON.parse(localStorage.getItem('default-display-columns')) ||
            [
                {key: "data_product_id", label: "ID", sortable: true},
                {key: "name", label: "Name", sortable: true},
                {key: 'actions', label: ''}
            ];
    }
}