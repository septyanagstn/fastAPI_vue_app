<template>
  <div class="wrapper">
    <side-bar>
      <template slot="links">
        <sidebar-link to="/warta/dashboard" name="Dasbor" icon="ti-panel" />
        <sidebar-link to="/warta/manage-articles" name="Kelola Berita" icon="ti-view-list-alt"
        />
        <sidebar-link to="/warta/user-management" name="Kelola User" icon="ti-user" />
      </template>
    </side-bar>
    <div class="main-panel">
      <top-navbar></top-navbar>

      <dashboard-content @click.native="toggleSidebar"> </dashboard-content>

      <content-footer></content-footer>
    </div>
  </div>
</template>
<style lang="scss"></style>
<script>
import TopNavbar from "./TopNavbar.vue";
import ContentFooter from "./ContentFooter.vue";
import DashboardContent from "./Content.vue";
export default {
  components: {
    TopNavbar,
    ContentFooter,
    DashboardContent,
  },
  methods: {
    toggleSidebar() {
      if (this.$sidebar.showSidebar) {
        this.$sidebar.displaySidebar(false);
      }
    },
  },
};
</script>
