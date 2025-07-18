<template>
    <div class="modal fade show d-block" style="background-color: rgba(0, 0, 0, 0.5); z-index: 1050">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h4 class="modal-title">Tambah User</h4>
                </div>
                <div class="modal-body">
                    <form @submit.prevent>
                        <div class="form-group" v-for="field in fields" :key="field.name">
                            <label :for="field.name" class="form-label fw-bold fs-6">{{ field.label }}</label>
                            <input :type="field.type" class="form-control border" v-model="form[field.name]"
                                :name="field.name" :placeholder="field.placeholder" required />
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" @click="$emit('close')">Close</button>
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
                { name: 'username', label: 'Username', type: 'text', placeholder: 'Add a username' },
                { name: 'email', label: 'Email', type: 'email', placeholder: 'Add an email' },
                { name: 'full_name', label: 'Fullname', type: 'text', placeholder: 'Add a fullname' },
                { name: 'password', label: 'Password', type: 'password', placeholder: 'Add a password' },
            ]
        };
    }
}
</script>
