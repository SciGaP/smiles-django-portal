export const configurationService = {
    getDisplayableColumns,
    getLitRecordDisplayableColumns
};


function getDisplayableColumns(type) {
    if (type === "exp") {
        return JSON.parse(localStorage.getItem('exp-display-columns')) ||
            [
                {key: "dye_family", label: "Family", sortable: true},
                {key: "structure", label: "Structure", thClass: 'centered-header'},
                {key: "name", label: "Name", sortable: true},
                {key: "structural_data.smiles", label: "Smiles String"},
                {key: "mol_id", label: "Molecular Id"},
                {key: "mw", label: "MW"},
                {key: 'actions', label: ''}
            ];

    } else if (type === "comp") {
        return JSON.parse(localStorage.getItem('comp-display-columns')) ||
            [
                {key: "dye_family", label: "Family", sortable: true},
                {key: "structure", label: "Structure", thClass: 'centered-header'},
                {key: "name", label: "Name", sortable: true},
                {key: "identifiers.smiles", label: "Smiles String"},
                {key: "molecule.formula", label: "Formula"},
                {key: "calculated_properties.homos", label: "Homos"},
                {key: 'actions', label: ''}
            ];
    } else if (type === "lit") {
        return JSON.parse(localStorage.getItem('lit-display-columns')) ||
            [
                {key: "dye_family", label: "Family", sortable: true},
                {key: "name", label: "Name", sortable: true},
                {key: "identifiers.smiles", label: "Smiles String"},
                {key: 'actions', label: ''}
            ];
    } else {
        return JSON.parse(localStorage.getItem('default-display-columns')) ||
            [
                {key: "data_product_id", label: "ID", sortable: true},
                {key: "name", label: "Name", sortable: true},
                {key: "redox_info", label: "Redox Info", sortable: true},
                {key: "search_keywords", label: "Search Keywords"},
                {key: 'actions', label: ''}
            ];
    }
}

function getLitRecordDisplayableColumns() {
    return JSON.parse(localStorage.getItem('lit-record-display-columns')) ||
        [
            {key: "dye_family", label: "Family"},
            {key: "structure", label: "Structure", thClass: 'centered-header'},
            {key: "smiles", label: "SMILES String"},
            {key: 'actions', label: ''}
        ];
}