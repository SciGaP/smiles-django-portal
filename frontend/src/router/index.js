import Vue from "vue";
import VueRouter from "vue-router";
import DataProductUpload from '../components/DataProductUploader.vue'
import DataProductTable from '../components/DataProductTable.vue'

Vue.use(VueRouter);

const routes = [
    {
        path: '/smiles/upload-dps',
        name: 'data-product-upload',
        component: DataProductUpload
    },
    {
        path: '/smiles/dps',
        name: 'data-product-list',
        component: DataProductTable
    }
]

const router = new VueRouter({
    mode: "history",
    base: "/smiles_django/build",
    routes,
});

export default router;

