<template>
  <div>
    <!-- Button to trigger the modal -->
    <button @click="showModal = true" class="btn btn-primary">Open Modal</button>
    
    <!-- Modal -->
    <div class="modal" tabindex="-1" role="dialog" v-show="showModal">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Modal title</h5>
            <button type="button" class="close" @click="showModal = false">
              <span>&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <p>Modal body text goes here.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showModal = false">Close</button>
            <button type="button" class="btn btn-primary">Save changes</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showModal: false
    };
  }
};
</script>

<style>
/* Add any custom styling here */
</style>
