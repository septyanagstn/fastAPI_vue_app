<template>
  <div class="card text-center py-5">
    <div class="loader mx-auto">
      <div class="loader--dot" v-for="n in 6" :key="n" :class="`dot-${n}`"></div>
      <div class="loader--text mt-3 text-muted">Loading...</div>
    </div>
  </div>
</template>

<style scoped>
.loader {
  height: 20px;
  width: 250px;
  position: relative;
}

.loader--dot {
  animation-name: loader;
  animation-timing-function: ease-in-out;
  animation-duration: 3s;
  animation-iteration-count: infinite;
  height: 20px;
  width: 20px;
  border-radius: 100%;
  background-color: #222;
  position: absolute;
  border: 2px solid white;
}

/* Dot Colors (consistent with Vue Paper Dashboard colors) */
.dot-1 {
  background-color: #51cbce;
  animation-delay: 0.5s;
}
.dot-2 {
  background-color: #6bd098;
  animation-delay: 0.4s;
}
.dot-3 {
  background-color: #fbc658;
  animation-delay: 0.3s;
}
.dot-4 {
  background-color: #ef8157;
  animation-delay: 0.2s;
}
.dot-5 {
  background-color: #9368e9;
  animation-delay: 0.1s;
}
.dot-6 {
  background-color: #e3e3e3;
  animation-delay: 0s;
}

@keyframes loader {
  15% {
    transform: translateX(0);
  }
  45% {
    transform: translateX(230px);
  }
  65% {
    transform: translateX(230px);
  }
  95% {
    transform: translateX(0);
  }
}
</style>
