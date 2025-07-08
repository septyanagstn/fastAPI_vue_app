<template>
  <card class="card-user">
    <div slot="image">
      <img src="@/assets/img/background.jpg" alt="..." />
    </div>
    <div>
      <div class="author">
        <img
          class="avatar border-white"
          src="@/assets/img/faces/face-2.jpg"
          alt="..."
        />
        <h4 class="title">
          {{ user.username }}
          <br />
          <a href="#">
            <small>{{ user.email }}</small>
          </a>
        </h4>
      </div>
      <p class="description text-center">
        {{ user.bio }}
      </p>
    </div>
    <hr />
    <div class="text-center">
      <div class="row">
        <div
          v-for="(info, index) in details"
          :key="index"
          :class="getClasses(index)"
        >
          <h5>
            {{ info.title }}
            <br />
            <small>{{ info.subTitle }}</small>
          </h5>
        </div>
      </div>
    </div>
  </card>
</template>

<script>
export default {
  data() {
    return {
      user: {
        username: "",
        email: "",
        bio: "Lorem Ipsum Dolor Sit Amet",

      }
    };
  },
  mounted() {
    const userData = localStorage.getItem("user");
    if (userData) {
      const parsed = JSON.parse(userData);
      this.user.username = parsed.username || "";
      this.user.email = parsed.email || "";
    }
  },
  methods: {
    getClasses(index) {
      const remainder = index % 3;
      if (remainder === 0) return "col-lg-3 offset-lg-1";
      if (remainder === 2) return "col-lg-4";
      return "col-lg-3";
    }
  }
};
</script>
