<template>
  <div class="modal fade show d-block" style="background-color: rgba(0, 0, 0, 0.5); z-index: 1050">
    <div class="modal-dialog modal-sm">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Hapus User</h5>
        </div>
        <div class="modal-body">
          <p>Apakah Anda yakin ingin menghapus user <span><strong class="text-danger">{{ user.username }}</strong></span>?</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="$emit('close')">Batal</button>
          <button class="btn btn-danger" @click="$emit('confirm')">Hapus</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    user: {
      type: String,
      required: true,
    }
  },
  emits: ['confirm', 'close'],
}
</script>
