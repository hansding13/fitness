<template>
  <div>
    <button @click="loginWithGoogle">Login with Google</button>
  </div>
</template>

<script>
import { GoogleAuthProvider, signInWithPopup, getAuth } from 'firebase/auth';
import axios from 'axios';

export default {
  methods: {
    async loginWithGoogle() {
      try {
        const auth = getAuth();
        const provider = new GoogleAuthProvider();

        const result = await signInWithPopup(auth, provider);
        const user = result.user;

        // Verify if the user is correctly signed in
        if (user) {
          console.log('Logged in user:', user.displayName);
          // Obtain the Firebase ID token
          const idToken = await user.getIdToken();
          // Now, send this Firebase ID token to your Django backend
          console.log('before');
          const response = await this.sendTokenToDjango(idToken);
          console.log('after');

          // Redirect to Google OAuth if URL is provided
          if (response && response.data.google_oauth_url) {
            this.redirectToGoogleOAuth(response.data.google_oauth_url);
          } else {
            // Handle the case where Google OAuth URL is not provided
            console.log('Google OAuth URL not received');
            // You might want to redirect to a different page or show an error
          }
        }
      } catch (error) {
        console.error('Error logging in with Google:', error);
      }
    },
    async sendTokenToDjango(idToken) {
      try {
        await new Promise(resolve => setTimeout(resolve, 1000));
        const response = await axios.post('http://127.0.0.1:8000/api/send-token/', { firebaseIdToken: idToken });
        return response;
      } catch (error) {
        console.error('Error sending token to Django:', error.response);
      }
    },
    redirectToGoogleOAuth(url) {
      // Redirect the user to the Google OAuth URL
      window.location.href = url;
    },
  },
};
</script>
