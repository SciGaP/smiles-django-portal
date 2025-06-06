import Vue from "vue";
import {BootstrapVue} from "bootstrap-vue";
import router from './router'
import App from "./App.vue";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import "./assets/global.css"

import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";

Vue.config.productionTip = false;
Vue.use(BootstrapVue);
Vue.use(ElementUI);

new Vue({
    router,
    render: (h) => h(App)
}).$mount("#app");