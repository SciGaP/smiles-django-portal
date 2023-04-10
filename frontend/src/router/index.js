import { createRouter, createWebHistory } from 'vue-router'
import DataProductUpload from '../components/DataProductUpload.vue'

const routes = [
  {
    path: '/smiles/upload-dps',
    name: 'data-product-upload',
    component: DataProductUpload
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
