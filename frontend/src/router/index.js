import Vue from "vue";
import VueRouter from "vue-router";
import DataProductUpload from '../components/DataProductUploader.vue'
import DataProductTable from '../components/DataProductTable.vue'
import ExpDataProductDetails from '../components/ExpDataProductDetails.vue'
import CompDataProductDetails from '../components/CompDataProductDetails.vue'
import LitDataProductDetails from '../components/LitDataProductDetails.vue'

Vue.use(VueRouter);

const routes = [
    {
        path: '/upload-dps',
        name: 'data-product-upload',
        component: DataProductUpload
    },
    {
        path: '/dps',
        name: 'data-product-list',
        component: DataProductTable
    },
    {
        path: '/dp/exp/:id',
        name: 'exp-data-product-detailed',
        component: ExpDataProductDetails,
        props: true
    },
    {
        path: '/dp/comp/:id',
        name: 'comp-data-product-detailed',
        component: CompDataProductDetails,
        props: true
    },
    {
        path: '/dp/lit/:id',
        name: 'lit-data-product-detailed',
        component: LitDataProductDetails,
        props: true
    },
    {
        path: '/',
        name: 'data-product-list ',
        component: DataProductUpload
    },
]

const router = new VueRouter({
    mode: "history",
    base: "/smiles/home",
    routes,
});

export default router;

