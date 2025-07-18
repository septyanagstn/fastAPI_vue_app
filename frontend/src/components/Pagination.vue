<template>
  <div class="clearfix btn-group col-md-2 offset-md-5">
    <button
      type="button"
      class="text-dark btn btn-sm btn-outline-secondary"
      @click="$emit('change', currentPage - 1)"
      :disabled="currentPage === 1"
    >
      <span class="ti-angle-double-left"></span>
    </button>

    <button
      v-for="n in computedPages"
      :key="n"
      class="text-dark btn btn-sm btn-outline-secondary"
      :class="{ active: currentPage === n }"
      @click="$emit('change', n)"
    >
      {{ n }}
    </button>

    <button
      type="button"
      class="text-dark btn btn-sm btn-outline-secondary"
      @click="$emit('change', currentPage + 1)"
      :disabled="currentPage === totalPages"
    >
      <span class="ti-angle-double-right"></span>
    </button>
  </div>
</template>

<script>
export default {
  props: {
    currentPage: {
      type: Number,
      required: true
    },
    totalPages: {
      type: Number,
      required: true
    }
  },
  computed: {
    computedPages() {
      const total = this.totalPages;
      const current = this.currentPage;
      const maxPagesToShow = 5;

      let start = Math.max(1, current - Math.floor(maxPagesToShow / 2));
      let end = start + maxPagesToShow - 1;

      if (end > total) {
        end = total;
        start = Math.max(1, end - maxPagesToShow + 1);
      }

      const pages = [];
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    }
  }
};
</script>
