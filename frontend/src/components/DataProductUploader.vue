<template>
  <div>
    <div style="height: 50px;">
      <b-alert
          :show="dismissCountDown"
          fade
          variant="info"
      >Upload Successful!
      </b-alert>
    </div>
    <b-container fluid class="container">
      <div class="content">
        <label class="upload__label" :class="{'upload__label--has-file': file, 'no-click': uploading}">
          <img class="upload-input__icon" src="../assets/icons/file-upload.svg"/>
          <span class="upload-input__text">{{ file ? file.name : 'Drag and drop your file or click to browse' }}</span>
          <span class="upload-size__text">Max. file size 2 GB</span>
          <input class="file-upload__input" type="file" @change="onFileSelected" ref="fileInput"/>

          <div class="progress-bar-wrapper">
            <b-progress v-if="progress !== 0" :value="progress" variant="dark" striped class="mt-2"></b-progress>
          </div>
        </label>

        <div style="display: flex; justify-content: center;">
          <div class="text-label">
            <span>Or</span>
          </div>
        </div>
        <label class="input__label">
        <span class="upload-input__text">
          <img class="upload-input__icon" src="../assets/icons/fill-up-form.svg"/>
          Fill up a form
        </span>
          <input class="file-upload__input" type="button" @click="fillUpForm"/>
        </label>
        <div class="upload-container">
          <div style="display: flex; justify-content: center;">
            <div class="text-label">
              <span>To</span>
            </div>
          </div>
          <div class="upload-checkboxes" :class="{ 'no-click': uploading}">
            <label>
              <input type="radio" v-model="selectedDatabase" value="Literature Database">
              <span class="checkbox-label" :class="{ 'checkbox-selected': selectedDatabase === 'Literature Database' }">Literature Database</span>
            </label>
            <label>
              <input type="radio" v-model="selectedDatabase" value="Computational Database">
              <span class="checkbox-label"
                    :class="{ 'checkbox-selected': selectedDatabase === 'Computational Database' }">Computational Database</span>
            </label>
            <label>
              <input type="radio" v-model="selectedDatabase" value="Experimental Database">
              <span class="checkbox-label"
                    :class="{ 'checkbox-selected': selectedDatabase === 'Experimental Database' }">Experimental Database</span>
            </label>
          </div>
        </div>
      </div>
      <div class="file-upload__footer">
        <div class="mr-3">
          <button class="discard_button" :class="{'discard_button--disabled' : !file || uploading}"
                  :disabled="!file || uploading" @click="discard">Discard
          </button>
          <button class="btn btn-primary" :disabled="!file || uploading" @click="uploadFile">Next</button>
        </div>
      </div>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default {
  name: "FileUpload",

  data() {
    return {
      file: null,
      uploading: false,
      selectedDatabase: 'Computational Database',
      formOpen: false,
      progress: 0,
      dismissCountDown: 0,
    };
  },

  computed: {
    uploadUrl() {
      if (this.selectedDatabase === 'Literature Database') {
        return '/smiles/lit-dp/upload';
      } else if (this.selectedDatabase === 'Experimental Database') {
        return '/smiles/exp-dp/upload';
      } else if (this.selectedDatabase === 'Computational Database') {
        return '/smiles/comp-dp/upload';
      } else {
        return '';
      }
    }
  },

  methods: {
    onFileSelected(e) {
      this.file = e.target.files[0];
    },
    fillUpForm() {
      alert("Not implemented yet!");
    },
    uploadFile() {
      if (!this.uploading && this.file) {
        this.uploading = true;
        const formData = new FormData();
        formData.append("file", this.file);
        axios
            .post(this.uploadUrl, formData, {
              onUploadProgress: (progressEvent) => {
                this.progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
              }
            })
            .then(response => {
              this.uploading = false;
              this.progress = 0;
              this.file = null;
              this.$refs.fileInput.value = '';
              this.dismissCountDown = 3;
              console.log(response)
            })
            .catch(error => {
              console.log(error);
              this.uploading = false;
              this.progress = 0;
              this.file = null;
              this.$refs.fileInput.value = '';
            });
      }
    },
    discard() {
      this.file = null;
      this.selectedDatabase = 'Computational Database';
    },
  }
};
</script>

<style scoped>

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  padding: 0;
}

.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 80vw;
  max-width: 600px;
  margin-bottom: 20vh;
}

.upload__label,
.input__label {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  font-size: 20px;
  text-align: center;
  padding: 10px;
  border: 2px dashed #ccc;
  border-radius: 10px;
  height: 250px;
  margin: 10px 0;
  background-color: white;
  width: 500px;
}

.input__label {
  height: 60px;
}

.upload__label:hover,
.input__label:hover,
.upload__label--has-file {
  background-color: #f8f8f8;
}

.file-upload__input {
  display: none;
}

.upload-input__text {
  margin: 10px 0;
}

.upload-size__text {
  font-size: 18px;
  color: #777;
}

.upload-checkboxes {
  display: flex;
  flex-direction: row;
  margin-bottom: 20px;
}

.upload-checkboxes label {
  display: flex;
  flex-direction: row;
  margin-right: 10px;
}

.upload-checkboxes input[type="checkbox"] {
  margin-right: 5px;
}

.progress-bar-wrapper {
  position: relative;
  height: 20px;
  width: 80%;
  margin-top: 10px;
}

.checkbox-label {
  display: inline-flex;
  align-items: center;
  margin-right: 25px;
  padding: 8px;
  border-radius: 8px;
  background-color: #f5f5f5;
  color: #333;
  cursor: pointer;
}

.checkbox-label:hover {
  background-color: #ebebeb;
}

input[type="radio"] {
  display: none;
}

input[type="radio"] + .checkbox-label::before {
  content: "";
  display: inline-block;
  width: 16px;
  height: 16px;
  margin-right: 10px;
  border-radius: 3px;
  border: 1px solid #ccc;
  vertical-align: middle;
}

input[type="radio"]:checked + .checkbox-label::before {
  background-color: #333;
  border-color: #333;
}

.upload-container {
  text-align: center;
  margin-top: 40px;
  height: 50%;
}

.text-label {
  font-size: 20px;
  color: #777;
  margin: 10px 0;
}

.no-click {
  pointer-events: none;
}

.file-upload__footer {
  position: fixed;
  bottom: 0;
  width: calc(100vw - 70px); /* subtract the width of the navbar from the viewport width */
  height: 60px;
  background-color: white;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 0 20px;
}

.discard_button {
  background: none;
  border: none;
  padding: 0;
  font: inherit;
  cursor: pointer;
  color: inherit;
  margin-right: 10px;
}

.discard_button:hover:not(.discard_button--disabled) {
  text-decoration: underline;
}

.discard_button--disabled {
  color: lightgray;
}

.upload-input__icon {
  margin: 10px;
}

</style>