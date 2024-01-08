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
        provider.addScope('https://www.googleapis.com/auth/fitness.activity.read');
        const result = await signInWithPopup(auth, provider);
        const user = result.user;

        // Verify if the user is correctly signed in
        if (user) {
          console.log('Logged in user:', user.displayName);

          // Obtain the Firebase ID token
          const idToken = await user.getIdToken();

          // Now, send this Firebase ID token to your Django backend
          await this.sendTokenToDjango(idToken);

          // Redirect to Google OAuth consent page
          this.redirectToGoogleOAuth();
        }
      } catch (error) {
        console.error('Error logging in with Google:', error);
      }
    },
    async sendTokenToDjango(idToken) {
      try {
        await axios.post('http://127.0.0.1:8000/api/send-token/', { firebaseIdToken: idToken });
      } catch (error) {
        console.error('Error sending token to Django:', error.response);
      }
    },
    redirectToGoogleOAuth() {
      const clientId =  '372844630330-o48sldf6qb0qf593eaea67he10n22nug.apps.googleusercontent.com';
      const redirectUri = encodeURIComponent('http://localhost:8000/google/callback/');
      const responseType = 'code';
      const scope = encodeURIComponent([
       'https://www.googleapis.com/auth/fitness.activity.read',
            ].join(' '));
      const authUrl = `https://accounts.google.com/o/oauth2/auth?response_type=${responseType}&client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scope}`;
      window.location.href = authUrl;
    }
  },
};
</script>