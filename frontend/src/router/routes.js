import DashboardLayout from "@/layout/dashboard/DashboardLayout.vue";
// GeneralViews
import NotFound from "@/pages/NotFoundPage.vue";

// Admin pages
import Dashboard from "@/pages/Dashboard.vue";
import DetailArticle from "@/pages/DetailArticle.vue";
import UserProfile from "@/pages/UserProfile.vue";
import Notifications from "@/pages/Notifications.vue";
import Icons from "@/pages/Icons.vue";
import Maps from "@/pages/Maps.vue";
import Typography from "@/pages/Typography.vue";
import TableList from "@/pages/TableList.vue";

import Login from "@/pages/Authentication/Login.vue"
import Register from "@/pages/Authentication/Register.vue"
// import { component } from "vue/types/umd.js";

// const routes = [
  // {
  //   path: "/",
  //   // component: DashboardLayout,
  //   redirect: "/login",
  //   children: [
  //     {
  //       path: "login",
  //       name: "login",
  //       component: Login,
  //     },
  //     {
  //       path: "dashboard",
  //       name: "dashboard",
  //       component: Dashboard,
  //     },
  //     {
  //       path: "stats",
  //       name: "stats",
  //       component: UserProfile,
  //     },
  //     {
  //       path: "notifications",
  //       name: "notifications",
  //       component: Notifications,
  //     },
  //     {
  //       path: "icons",
  //       name: "icons",
  //       component: Icons,
  //     },
  //     {
  //       path: "maps",
  //       name: "maps",
  //       component: Maps,
  //     },
  //     {
  //       path: "typography",
  //       name: "typography",
  //       component: Typography,
  //     },
  //     {
  //       path: "table-list",
  //       name: "table-list",
  //       component: TableList,
  //     },
  //   ],
  // },
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
    children: [
      {
        path: "dashboard",
        name: "dashboard",
        component: Dashboard,
      },
      {
        path: "article-detail/:id",
        name: "article-detail",
        component: DetailArticle,
      },
      {
        path: "stats",
        name: "stats",
        component: UserProfile,
      },
      {
        path: "notifications",
        name: "notifications",
        component: Notifications,
      },
      {
        path: "icons",
        name: "icons",
        component: Icons,
      },
      {
        path: "maps",
        name: "maps",
        component: Maps,
      },
      {
        path: "typography",
        name: "typography",
        component: Typography,
      },
      {
        path: "table-list",
        name: "table-list",
        component: TableList,
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
