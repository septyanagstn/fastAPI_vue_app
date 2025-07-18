<template>
  <div class="modal fade show d-block" style="background-color: rgba(0, 0, 0, 0.5); z-index: 1050">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">Tambah Berita</h4>
        </div>
        <div class="modal-body">
          <form @submit.prevent>
            <div class="form-group" v-for="field in fields" :key="field.name">
              <label :for="field.name" class="form-label fw-bold fs-6">{{ field.label }}</label>
              <input :type="field.type" class="form-control border" v-model="form[field.name]" :name="field.name"
                :placeholder="field.placeholder" required />
            </div>
            <div class="form-group">
              <label for="content" class="form-label" style="font-weight: bold; font-size: large">Content</label>
              <textarea type="" v-model="form.content" class="form-control border" name="content"
                placeholder="Add a content" required></textarea>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="$emit('close')">
            Close
          </button>
          <button class="btn btn-success" @click="$emit('submit')">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    props: ['form'],
    emits: ['submit', 'close'],
    data() {
        return {
            fields: [
                { name: 'title', label: 'title', type: 'text', placeholder: 'Add a title' },
                { name: 'author', label: 'author', type: 'text', placeholder: 'Add an author' },
                { name: 'thumbnail', label: 'thumbnail', type: 'url', placeholder: 'Add a thumbnail url' },
            ]
        };
    }
}
</script>