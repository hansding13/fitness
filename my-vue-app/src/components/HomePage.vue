<template>
  <div class="home-container">
    <h1>Welcome to the Home Page</h1>
    <!-- Add more content here as needed -->
  </div>
</template>

<script>
export default {
  name: 'HomePage', // Updated name
  // Other component logic
};
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f2f2f2;
  padding: 20px;
}

h1 {
  color: #333;
  font-family: 'Arial', sans-serif;
  text-align: center;
  margin-bottom: 20px;
  font-size: 2em;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}
</style>
