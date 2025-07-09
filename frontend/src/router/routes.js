import DashboardLayout from "@/layout/dashboard/DashboardLayout.vue";
// GeneralViews
import NotFound from "@/pages/NotFoundPage.vue";

// Admin pages
import Dashboard from "@/pages/Dashboard.vue";
import DetailArticle from "@/pages/DetailArticle.vue";
import UserProfile from "@/pages/UserProfile.vue";
import UserManagement from "@/pages/UserManagement.vue";
import ArticleManagement from "@/pages/ArticleManagement.vue";

import Login from "@/pages/Authentication/Login.vue"
import Register from "@/pages/Authentication/Register.vue"

const routes = [
  {
    path: "/",
    redirect: "/login"
  },
  {
    path: "/login",
    name: "login",
    component: Login
  },
  {
    path: "/register",
    name: "register",
    component: Register
  },
  {
    path: "/warta",
    component: DashboardLayout,
    redirect: "/warta/dashboard",
    meta: { requiresAuth: true },
    children: [
      {
        path: "dashboard",
        name: "dasbor",
        component: Dashboard,
      },
      {
        path: "article-detail/:id",
        name: "article detail",
        component: DetailArticle,
      },
      {
        path: "user-profile",
        name: "user profile",
        component: UserProfile,
      },
      {
        path: "user-management",
        name: "kelola user",
        component: UserManagement,
      },
      {
        path: "manage-articles",
        name: "kelola berita",
        component: ArticleManagement,
      },

    ]
  },
  {
    path: "*",
    component: NotFound
  }
];

/**
 * Asynchronously load view (Webpack Lazy loading compatible)
 * The specified component must be inside the Views folder
 * @param  {string} name  the filename (basename) of the view to load.
function view(name) {
   var res= require('../components/Dashboard/Views/' + name + '.vue');
   return res;
};**/

export default routes;
