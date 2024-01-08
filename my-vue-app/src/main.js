import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBIfHz0h55IWw-tiSnyo-UNnZjNIO-PtMI",
  authDomain: "healthcare-408423.firebaseapp.com",
  projectId: "healthcare-408423",
  storageBucket: "healthcare-408423.appspot.com",
  messagingSenderId: "273340041825",
  appId: "1:273340041825:web:3ecb69e1229e421557b820",
  measurementId: "G-CM7GM94WKM"
};
initializeApp(firebaseConfig);
const auth = getAuth();

// Create and mount the Vue application
const app = createApp(App);

app.use(router);

// Provide the auth object to the application so it can be accessed in components
app.provide('auth', auth);

app.mount('#app');
