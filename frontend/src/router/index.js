import Vue from "vue";
import VueRouter from "vue-router";
import routes from "./routes";
import { jwtDecode } from 'jwt-decode';

Vue.use(VueRouter);

// configure router
const router = new VueRouter({
  routes, // short for routes: routes
  linkActiveClass: "active",
});

// Route Guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access_token");

  console.log(token);

  // Jika ada token
  if (token) {
    try {
      const decoded = jwtDecode(token);
      // console.log("DECODED:", decoded);
      const now = Date.now() / 1000;

      // console.log(decoded.exp)
      // console.log(now)

      if (decoded.exp && decoded.exp < now) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");
        return next("/login");
      } else {
        return next();
      }
    } catch (err) {
      console.error("JWT decode error:", err.message);
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      return next("/login");
    }
  }
  
  if (to.matched.some(record => record.meta.requiresAuth) && !token) {
    return next("/login");
  }

  next();
});

export default router;
