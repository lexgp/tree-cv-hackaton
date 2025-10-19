import { createPinia } from 'pinia';
import { createApp } from 'vue';

import App from '@/App.vue';
import { registerPlugins } from '@core/utils/plugins';
import { createYmaps } from 'vue-yandex-maps';

// Styles
import '@core/scss/template/index.scss';
import '@layouts/styles/index.scss';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

// создаём экземпляр плагина с настройками
const ymaps = createYmaps({
  apikey: 'cc66d141-4887-4c07-b184-a7a032b181ac',
  lang: 'ru_RU',
  // version: '3.0',
  initializeOn: 'onComponentMount',
})

// Create vue app
const app = createApp(App)

// Register plugins
registerPlugins(app)
app.use(createPinia());
app.use(ymaps)

// Mount vue app
app.mount('#app')
