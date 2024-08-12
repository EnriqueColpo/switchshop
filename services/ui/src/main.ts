import { createApp } from 'vue';
import 'element-plus/dist/index.css';
import ElementPlus from 'element-plus';
import App from './App.vue';
import './global.css';
import '../dist/output.css'

import { Amplify } from 'aws-amplify';
import { awsExports } from './ aws-exports';
Amplify.configure(awsExports);

const app = createApp(App);

app.use(ElementPlus)

app.mount('#app');